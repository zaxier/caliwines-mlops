variable "cluster_name" {}
variable "cluster_autotermination_minutes" {}
variable "cluster_num_workers" {}
variable "cluster_data_security_mode" {}


data "databricks_spark_version" "ml-latest" {
  latest = true
  long_term_support = false
  ml = true
}

data "databricks_node_type" "node_type" {
  local_disk = true
  min_cores = 16
}

resource "databricks_cluster" "all_purpose_cluster" {
  cluster_name            = var.cluster_name
  node_type_id            = data.databricks_node_type.node_type.id
  spark_version           = data.databricks_spark_version.ml-latest.id
  autotermination_minutes = var.cluster_autotermination_minutes
  num_workers             = var.cluster_num_workers
  data_security_mode      = var.cluster_data_security_mode
  single_user_name        = data.databricks_current_user.me.user_name
}

resource "databricks_library" "pyyaml" {
  cluster_id = databricks_cluster.all_purpose_cluster.id
  pypi {
    package = "pyyaml==6.0"
  }
}

resource "databricks_library" "python_dotenv" {
  cluster_id = databricks_cluster.all_purpose_cluster.id
  pypi {
    package = "python-dotenv==0.21.1"
  }
}
