variable "project_name" {}
variable "branch" {}
variable "repo_url" {}
variable "git_provider" {}
variable "env" {}

# resource "databricks_job" "data_setup_depr" {
#   name = "${var.project_name}-data_setup_job-${var.env}"
#   existing_cluster_id = databricks_cluster.all_purpose_cluster.id

#   git_source {
#     provider = var.git_provider
#     url = var.repo_url
#     branch = var.branch
#   }

#   notebook_task {
#     notebook_path = "notebooks/cali_housing_project/data_setup"
#     base_parameters = tomap({
#         env = var.env
#     })
#   } 
#   email_notifications {
#     on_success = [data.databricks_current_user.me.user_name]
#     on_failure = [data.databricks_current_user.me.user_name]
#   }
# }


resource "databricks_repo" "packaged_poc_mlops" {
  url = "https://github.com/Zaxier/packaged-poc-mlops"
  path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops"
  branch = var.branch
}

resource "databricks_job" "model_train_git" {
  name = "${var.project_name}-model_train_git_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_housing_project/model_train"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "model_train_repos" {
  name = "${var.project_name}-model_train_repos_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  notebook_task {
    notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/cali_housing_project/model_train"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "model_deployment_git" {
  name = "${var.project_name}-model_deployment_git_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_housing_project/model_deployment"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "model_deployment_repos" {
  name = "${var.project_name}-model_deployment_repos_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  notebook_task {
    notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/cali_housing_project/model_deployment"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "model_inference_batch_git" {
  name = "${var.project_name}-model_inference_batch_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  notebook_task {
    notebook_path = "notebooks/cali_housing_project/model_inference_batch"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}

resource "databricks_job" "model_inference_batch_repos" {
  name = "${var.project_name}-model_inference_batch_job-${var.env}"
  existing_cluster_id = databricks_cluster.all_purpose_cluster.id
  
  notebook_task {
    notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/cali_housing_project/model_inference_batch"
    base_parameters = tomap({
        env = var.env
    })
  }
  
  email_notifications {
    on_success = [data.databricks_current_user.me.user_name]
    on_failure = [data.databricks_current_user.me.user_name]
  }

}


resource "databricks_job" "data_setup_git" {
  name = "${var.project_name}-data_setup_job-${var.env}"

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  task {
    task_key = "taskA-data_cleanup"
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id


    notebook_task {
      notebook_path = "notebooks/_mlops_data_generator/data_cleanup"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskB-data_setup"
    depends_on {
      task_key = "taskA-data_cleanup"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "notebooks/_mlops_data_generator/data_setup"
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
  name = "${var.project_name}-data_setup_job-${var.env}"

  task {
    task_key = "taskA-data_cleanup"
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/_mlops_data_generator/data_cleanup"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskB-data_setup"
    depends_on {
      task_key = "taskA-data_cleanup"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/_mlops_data_generator/data_setup"
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

resource "databricks_job" "test_job_git" {
  name = "${var.project_name}-test_job-${var.env}"

  git_source {
    provider = var.git_provider
    url = var.repo_url
    branch = var.branch
  }

  task {
    task_key = "taskA-data_cleanup"
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id


    notebook_task {
      notebook_path = "notebooks/_mlops_data_generator/data_cleanup"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskB-data_setup"
    depends_on {
      task_key = "taskA-data_cleanup"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "notebooks/_mlops_data_generator/data_setup"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskC-model_train"
    depends_on {
      task_key = "taskB-data_setup"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "notebooks/cali_housing_project/model_train"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskD-model_deployment"
    depends_on {
      task_key = "taskC-model_train"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "notebooks/cali_housing_project/model_deployment"
      base_parameters = tomap({
          env = var.env
      })
    }
  } 

  task {
    task_key = "taskE-model_inference_batch"
    depends_on {
      task_key = "taskD-model_deployment"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "notebooks/cali_housing_project/model_inference_batch"
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

resource "databricks_job" "test_job_repos" {
  name = "${var.project_name}-test_job-${var.env}"

  task {
    task_key = "taskA-data_cleanup"
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id


    notebook_task {
      notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/_mlops_data_generator/data_cleanup"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskB-data_setup"
    depends_on {
      task_key = "taskA-data_cleanup"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/_mlops_data_generator/data_setup"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskC-model_train"
    depends_on {
      task_key = "taskB-data_setup"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/_mlops_data_generator/model_train"
      base_parameters = tomap({
          env = var.env
      })
    }
  }

  task {
    task_key = "taskD-model_deployment"
    depends_on {
      task_key = "taskC-model_train"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/_mlops_data_generator/model_deployment"
      base_parameters = tomap({
          env = var.env
      })
    }
  } 

  task {
    task_key = "taskE-model_inference_batch"
    depends_on {
      task_key = "taskD-model_deployment"
    }
    existing_cluster_id = databricks_cluster.all_purpose_cluster.id

    notebook_task {
      notebook_path = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops/notebooks/_mlops_data_generator/model_inference_batch"
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

