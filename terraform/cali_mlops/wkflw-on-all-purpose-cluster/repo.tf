
resource "databricks_repo" "cali_mlops" {
  url = "https://github.com/Zaxier/packaged-poc-mlops"
  path = "/Repos/${data.databricks_current_user.me.user_name}/cali_mlops"
  branch = var.branch
}