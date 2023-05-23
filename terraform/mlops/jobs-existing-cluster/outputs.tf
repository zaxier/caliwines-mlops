output "data_setup" {
  value = databricks_job.data_setup.url
}

output "model_train" {
  value = databricks_job.model_train
}

output "model_deployment" {
  value = databricks_job.model_deployment
}

output "model_inference_batch" {
  value = databricks_job.model_inference_batch
}

