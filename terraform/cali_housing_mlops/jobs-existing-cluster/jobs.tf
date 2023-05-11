variable "project_name" {}
variable "branch" {}
variable "repo_url" {}
variable "git_provider" {}
variable "env" {}

resource "databricks_job" "data_setup" {
  name = "${var.project_name}-data_setup_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_housing_mlops/data_setup"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "model_train" {
  name = "${var.project_name}-model_train_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_housing_mlops/model_train"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "model_deployment" {
  name = "${var.project_name}-model_deployment_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_housing_mlops/model_deployment"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "model_inference_batch" {
  name = "${var.project_name}-model_inference_batch_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_housing_mlops/model_inference_batch"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

# resource "databricks_job" "<template>" {
#   name = "${var.project_name}-<template>_job-${var.env}"
#   existing_cluster_id = databricks_cluster.all_purpose_cluster.id

#   git_source {
#     provider = var.git_provider
#     url = var.repo_url
#     branch = var.branch
#   }

#   notebook_task {
#     notebook_path = "notebooks/cali_housing_mlops/<template>"
#     base_parameters = tomap({
#         env = var.env
#     })
#   }
  
#   email_notifications {
#     on_success = [data.databricks_current_user.me.user_name]
#     on_failure = [data.databricks_current_user.me.user_name]
#   }

# }