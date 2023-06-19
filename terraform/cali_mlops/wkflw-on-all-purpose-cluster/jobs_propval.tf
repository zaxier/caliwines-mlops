resource "databricks_job" "propval_model_train_git" {
  name = "${var.project_name}--propval_model_train_git_job--${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_mlops/propval_model_train"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "propval_model_train_repos" {
  name = "${var.project_name}--propval_model_train_repos_job--${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  notebook_task {
    notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/cali_mlops/notebooks/cali_mlops/propval_model_train"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "propval_model_deployment_git" {
  name = "${var.project_name}--propval_model_deployment_git_job--${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_mlops/propval_model_deployment"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "propval_model_deployment_repos" {
  name = "${var.project_name}--propval_model_deployment_repos_job--${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  notebook_task {
    notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/poc-accelerate-mlops/notebooks/cali_mlops/propval_model_deployment"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "propval_model_inference_batch_git" {
  name = "${var.project_name}--model_inference_batch_job--${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_mlops/propval_model_inference_batch"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "propval_model_inference_batch_repos" {
  name = "${var.project_name}--propval_model_inference_batch_job--${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id
  
  notebook_task {
    notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/cali_mlops/notebooks/cali_mlops/propval_model_inference_batch"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}
