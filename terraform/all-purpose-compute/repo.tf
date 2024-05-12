
resource "databricks_repo" "cali_mlops" {
  url = var.repo_url
  path = "/Repos/${data.databricks_current_user.me.user_name}/poc-accelerate-mlops"
  branch = var.git_branch
}