variable "cluster_name" {}
variable "cluster_autotermination_minutes" {}
variable "cluster_num_workers" {}
variable "cluster_data_security_mode" {}

# Create the cluster with the "smallest" amount
# of resources allowed.
data "databricks_node_type" "smallest" {
  local_disk = true
}

# Use the latest Databricks Runtime
data "databricks_spark_version" "ml-latest" {
  latest = true
  long_term_support = false
  ml = true
}

resource "databricks_cluster" "zaxier-ml" {
  cluster_name = "zaxier-ml-compute"
  spark_version = data.databricks_spark_version.ml-latest.id
  autotermination_minutes = 444
  num_workers = 2
  node_type_id = "i3.xlarge"
  data_security_mode = "SINGLE_USER"
}

resource "databricks_cluster" "this" {
  cluster_name            = var.cluster_name
  node_type_id            = data.databricks_node_type.smallest.id
  spark_version           = data.databricks_spark_version.ml-latest.id
  autotermination_minutes = var.cluster_autotermination_minutes
  num_workers             = var.cluster_num_workers
  data_security_mode      = var.cluster_data_security_mode
}

output "cluster_url" {
 value = databricks_cluster.this.url
}

output "zaxier-ml-cluster-url" {
  value = databricks_cluster.zaxier-ml.url
}
