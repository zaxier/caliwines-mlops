resource "databricks_directory" "cali_dev_dir" {
  path = "/Shared/cali_housing_mlops/dev"
}

resource "databricks_directory" "cali_staging_dir" {
    path = "/Shared/cali_housing_mlops/staging"
}

resource "databricks_directory" "cali_prod_dir" {
    path = "/Shared/cali_housing_mlops/prod"
}
