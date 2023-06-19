resource "databricks_job" "data_setup_git" {
  name = "${var.project_name}--data_setup_job--${var.env}"

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  task {
    task_key = "taskA--data_cleanup"
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id


    notebook_task {
      notebook_path = "notebooks/_cali_mlops_data_generatorator/data_cleanup"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskB--data_setup"
    depends_on {
      task_key = "taskA--data_cleanup"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "notebooks/_cali_mlops_data_generatorator/data_setup"
      base_parameters = tomap({
          env = var.env
      })
    }

  }

  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }


}


resource "databricks_job" "data_setup_repos" {
  name = "${var.project_name}--data_setup_job--${var.env}"

  task {
    task_key = "taskA--data_cleanup"
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/cali_mlops/notebooks/_cali_mlops_data_generatorator/data_cleanup"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskB--data_setup"
    depends_on {
      task_key = "taskA--data_cleanup"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/cali_mlops/notebooks/_cali_mlops_data_generatorator/data_setup"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }


}

