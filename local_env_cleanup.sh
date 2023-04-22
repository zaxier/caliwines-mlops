# TODO

# Clean up workspace folders
function remove_workspace_dir() {
  local host=$1
  local dir=$2
  local netrc_file=$3

  echo "Removing workspace directory '$dir' in workspace shard: https://$host"
  curl --netrc-file $netrc_file --request POST \
      https://$host/api/2.0/workspace/delete \
      --header 'Accept: application/json' \
      --data "{\"path\": \"$dir\", \"recursive\": true}" 
}

remove_workspace_dir $dev_host $dev_dir ~/.netrc_databricks_dev
remove_workspace_dir $staging_host $staging_dir ~/.netrc_databricks_staging
remove_workspace_dir $prod_host $prod_dir ~/.netrc_databricks_prod


# Clean up .netrc files
rm ~/.netrc_databricks_dev
rm ~/.netrc_databricks_staging
rm ~/.netrc_databricks_prod

# Clean up environment variables
unset dev_profile_number
unset staging_profile_number
unset prod_profile_number
unset dev_profile
unset staging_profile
unset prod_profile
unset dev_host
unset staging_host
unset prod_host
unset dev_token
unset staging_token
unset prod_token


# Clean up models


# Clean up jobs
dbx destroy

# Clean up data

