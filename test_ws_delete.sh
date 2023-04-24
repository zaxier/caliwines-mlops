#!/bin/bash

# Set variables
project_dir='/Shared/packaged_poc'

dev_ws_dir=$project_dir'/dev/dbx/cali_housing_mlops_dev'
dev_artifacts=$project_dir'/dev/dbx/projects/cali_housing_mlops_dev'

staging_ws_dir=$project_dir'/staging/dbx/cali_housing_mlops_staging'
staging_artifacts=$project_dir'/staging/dbx/projects/cali_housing_mlops_staging'

prod_ws_dir=$project_dir'/prod/dbx/cali_housing_mlops_prod'
prod_artifacts=$project_dir'/prod/dbx/projects/cali_housing_mlops_prod'

# Search for databricks profiles in the .databrickscfg file
echo -e "Searching for databricks profiles in the .databrickscfg file... \n"
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

# Cleanup directories
function cleanup_ws_dir() {
  local host=$1
  local dir=$2
  local netrc_file=$3

  echo "Deleting workspace directory '$dir' in workspace shard: https://$host"
  curl --netrc-file $netrc_file --request POST \
      https://$host/api/2.0/workspace/delete \
      --header 'Accept: application/json' \
      --data "{\"path\": \"$dir\", \"recursive\": true}"
  echo ""
}

# Check if the user wants to clean up the workspace directories
echo -n "Do you want to clean up the workspace directories? (y/n): "
read cleanup
echo ""

if [ "$cleanup" == "y" ]; then
  cleanup_ws_dir $dev_host $project_dir ~/.netrc_databricks_dev
  cleanup_ws_dir $staging_host $project_dir ~/.netrc_databricks_staging
  cleanup_ws_dir $prod_host $project_dir ~/.netrc_databricks_prod
  echo ""
fi

function cleanup_artifacts() {
  local host=$1
  local artifact_loc=$2
  local netrc_file=$3

  echo "Deleting dbfs dir '$dir' in workspace shard: https://$host"
  curl --netrc-file $netrc_file --request POST \
      https://$host/api/2.0/dbfs/delete \
      --data "{\"path\": \"$artifact_loc\", \"recursive\": true}" 
  echo ""
}

# Check if the user wants to clean up the artifact directories
echo -n "Do you want to clean up the artifact directories? (y/n): "
read cleanup
echo ""

if [ "$cleanup" == "y" ]; then
  cleanup_artifacts $dev_host $dev_artifacts ~/.netrc_databricks_dev
  cleanup_artifacts $staging_host $staging_artifacts ~/.netrc_databricks_staging
  cleanup_artifacts $prod_host $prod_artifacts ~/.netrc_databricks_prod
  echo ""
fi

