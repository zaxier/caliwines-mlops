variable "job_name" {
  description = "A name for the job."
  type        = string
  default     = "My Job"
}

resource "databricks_job" "data_setup" {
  name = var.job_name
  existing_cluster_id = databricks_cluster.zaxier-ml.id

  git_source {
    provider = "github"
    url = "https://github.com/Zaxier/packaged-poc-mlops"
    branch = "gen-master"
  }

  notebook_task {
    notebook_path = "notebooks/cali_housing_mlops/data_setup"
    base_parameters = tomap({
      env = "dev"
    })

  }

  email_notifications {
    on_success = [ data.databricks_current_user.me.user_name ]
    on_failure = [ data.databricks_current_user.me.user_name ]
  }
}

output "job_url" {
  value = databricks_job.data_setup.url
}