cluster_name                    = "packaged-poc-terraform-all-purpose"
cluster_autotermination_minutes = 30
cluster_num_workers             = 1
cluster_data_security_mode      = "SINGLE_USER"

git_provider = "github"
repo_url = "https://github.com/Zaxier/packaged-poc-mlops"
branch   = "gen-dev"

project_name = "mlops"
