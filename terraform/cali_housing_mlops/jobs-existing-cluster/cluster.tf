variable "cluster_name" {}
variable "cluster_autotermination_minutes" {}
variable "cluster_num_workers" {}
variable "cluster_data_security_mode" {}

data "databricks_spark_version" "ml-latest" {
  latest = true
  long_term_support = false
  ml = true
}

data "databricks_node_type" "smallest" {
  local_disk = true
}

resource "databricks_cluster" "all_purpose_cluster" {
  cluster_name            = var.cluster_name
  node_type_id            = data.databricks_node_type.smallest.id
  spark_version           = data.databricks_spark_version.ml-latest.id
  autotermination_minutes = var.cluster_autotermination_minutes
  num_workers             = var.cluster_num_workers
  data_security_mode      = var.cluster_data_security_mode
}
