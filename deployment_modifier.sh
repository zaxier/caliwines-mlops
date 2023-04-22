#!/bin/bash
# deployment_modifier.sh


function configure_deployment_file_for_all_purpose_cluster () {
  # Ask the user if they have an existing all-purpose cluster running for development work
  read -p "Do you have an existing all-purpose cluster running for development work? (y/n): " has_cluster

  if [[ $has_cluster == "y" ]]; then
    # Ask the user to input the cluster ID
    read -p "Please enter the cluster ID: " cluster_id

    # Store the cluster ID as a variable
    existing_cluster_id=$cluster_id
    # Replace all occurrences of the string '<existing_cluster_id>' with the new cluster ID variable in a specified file
    sed -i'.bak' "s/<existing_cluster_id>/$existing_cluster_id/g" conf/deployment.yml
  else
    # If the user does not have an existing cluster, set the cluster ID to an empty string
    existing_cluster_id=""
  fi

}

# Ask the user if they have an existing all-purpose cluster running for development work
read -p "Do you have an existing all-purpose cluster running for development work? (y/n): " has_cluster

if [[ $has_cluster == "y" ]]; then
  # Ask the user to input the cluster ID
  read -p "Please enter the cluster ID: " cluster_id

  # Store the cluster ID as a variable
  existing_cluster_id=$cluster_id
  # Replace all occurrences of the string '<existing_cluster_id>' with the new cluster ID variable in a specified file
  sed -i "s/<existing_cluster_id>/$existing_cluster_id/g" conf/deployment.yml
else
  # If the user does not have an existing cluster, set the cluster ID to an empty string
  existing_cluster_id=""
fi

