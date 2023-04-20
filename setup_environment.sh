#!/bin/bash

# Set variables
echo -e "...setting variables \n"
project_dir='/Shared/packaged-poc'
dev_dir=$project_dir'/dev'
staging_dir=$project_dir'/staging'
prod_dir=$project_dir'/prod'

# Search for databricks profiles in the .databrickscfg file
echo -e "...searching for databricks profiles in the .databrickscfg file \n"
profiles=$(cat ~/.databrickscfg | grep -E '^\[' | sed 's/\[ //')
# Check if any profiles were found
if [ -z "$profiles" ]; then
  echo "No profiles found."
  exit 1
fi

# Extract hosts and tokens from .databrickscfg file corresponding to the profiles
hosts=$(cat ~/.databrickscfg | grep host | sed 's/.*https:\/\///' | cut -d '/' -f 1)
tokens=$(cat ~/.databrickscfg | grep token | sed 's/.*token = //')

# Print out the list of profiles found
echo "I found the following profiles:"
echo "$profiles" | nl
echo ""

# Prompt the user to select a profile for each environment
echo -n "Enter the number of the profile you want to use for dev: "
read dev_profile_number
echo -n "Enter the number of the profile you want to use for staging: "
read staging_profile_number
echo -n "Enter the number of the profile you want to use for prod: "
read prod_profile_number
echo ""

# Get the profile, host and token for each environment
dev_profile=$(echo "$profiles" | sed -n "${dev_profile_number}p")
staging_profile=$(echo "$profiles" | sed -n "${staging_profile_number}p")
prod_profile=$(echo "$profiles" | sed -n "${prod_profile_number}p")

dev_host=$(echo "$hosts" | sed -n "${dev_profile_number}p")
staging_host=$(echo "$hosts" | sed -n "${staging_profile_number}p")
prod_host=$(echo "$hosts" | sed -n "${prod_profile_number}p")

dev_token=$(echo "$tokens" | sed -n "${dev_profile_number}p")
staging_token=$(echo "$tokens" | sed -n "${staging_profile_number}p")
prod_token=$(echo "$tokens" | sed -n "${prod_profile_number}p")

echo "Using " $dev_profile " as dev profile on host:" $dev_host
echo "Using " $staging_profile " as staging profile on host:" $staging_host
echo "Using " $prod_profile " as prod profile on host:" $prod_host
echo ""

# Create a .netrc file for each environment that will be used to authenticate with each workspace 
#   environment (for curl commands)
function create_netrc_file() {
  local host=$1
  local token=$2
  local netrc_file_path=$3

  echo "Creating .netrc file for $host"
  echo "machine $host" > $netrc_file_path
  echo "login token" >> $netrc_file_path
  echo "password $token" >> $netrc_file_path
}

create_netrc_file $dev_host $dev_token ~/.netrc_databricks_dev
create_netrc_file $staging_host $staging_token ~/.netrc_databricks_staging
create_netrc_file $prod_host $prod_token ~/.netrc_databricks_prod
echo ""

# Create the workspace folders in each environment
function create_workspace_dir() {
  local host=$1
  local dir=$2
  local netrc_file=$3

  echo "Creating workspace directory '$dir' in workspace shard: https://$host"
  curl --netrc-file $netrc_file --request POST \
      https://$host/api/2.0/workspace/mkdirs \
      --header 'Accept: application/json' \
      --data "{\"path\": \"$dir\"}" 
}

create_workspace_dir $dev_host $dev_dir ~/.netrc_databricks_dev
create_workspace_dir $staging_host $staging_dir ~/.netrc_databricks_staging
create_workspace_dir $prod_host $prod_dir ~/.netrc_databricks_prod
echo ""

# Function to remove the square brackets from the profile name
function clean_profile_name() {
  local input_string=$1
  local result=$(echo "$input_string" | sed 's/\[//g; s/\]//g')
  echo "$result"
}

# Configure dbx for use in each environment
function configure_dbx_environment() {
  local env=$1
  local dir=$2
  local profile=$3

  echo "Configuring $env environment"
  dbx configure -e $env \
      --workspace-dir $dir \
      --artifact-location dbfs:$dir/dbx/artifacts \
      --profile $profile
}

configure_dbx_environment dev $dev_dir $(clean_profile_name $dev_profile)
configure_dbx_environment staging $staging_dir $(clean_profile_name $staging_profile)
configure_dbx_environment prod $prod_dir $(clean_profile_name $prod_profile)

# TODO: Add code to create cluster or update deployment file with cluster id