cluster_name                    = "packaged-poc-terraform-all-purpose"
cluster_autotermination_minutes = 30
cluster_num_workers             = 1
cluster_data_security_mode      = "SINGLE_USER"

git_provider = "github"
repo_url = "https://github.com/Zaxier/packaged-poc-mlops"
branch   = "dev"

repo_root = "/Repos/${data.databricks_current_user.me.user_name}/packaged_poc_mlops"

project_name = "cali_housing_mlops"
