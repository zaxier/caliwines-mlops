resource "databricks_directory" "cali_dev_dir" {
  path = "/Shared/poc-accelerate-mlops/dev"
}

resource "databricks_directory" "cali_staging_dir" {
    path = "/Shared/poc-accelerate-mlops/staging"
}

resource "databricks_directory" "cali_prod_dir" {
    path = "/Shared/poc-accelerate-mlops/prod"
}
