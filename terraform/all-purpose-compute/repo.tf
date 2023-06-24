
resource "databricks_repo" "cali_mlops" {
  url = "https://github.com/Zaxier/poc-accelerate-mlops"
  path = "/Repos/${data.databricks_current_user.me.user_name}/poc-accelerate-mlops"
  branch = var.git_branch
}