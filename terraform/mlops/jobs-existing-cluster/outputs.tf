output "data_setup" {
  value = databricks_job.data_setup.url
}

output "model_train_git" {
  value = databricks_job.model_train_git
}

output "model_train_repos" {
  value = databricks_job.model_train_repos
}
  

# TODO: 

# output "model_deployment" {
#   value = databricks_job.model_deployment
# }

# output "model_inference_batch" {
#   value = databricks_job.model_inference_batch
# }

