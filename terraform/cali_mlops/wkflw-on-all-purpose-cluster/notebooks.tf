
# resource "databricks_notebook" "data_cleanup" {
#   path = "/Repos/{data.databricks_current_user.me.user_name}/packaged-poc-mlops/_cali_mlops_data_generator/data_cleanup"
# }

# resource "databricks_notebook" "data_setup" {
#   path = "/Repos/{data.databricks_current_user.me.user_name}/packaged-poc-mlops/_cali_mlops_data_generator/data_setup"
# }
  
# resource "databricks_notebook" "model_train" {
#   path = "/Repos/{data.databricks_current_user.me.user_name}/packaged-poc-mlops/cali_mlops/model_train"
# }

  
# resource "databricks_notebook" "model_inference_batch" {
#   path = "/Repos/{data.databricks_current_user.me.user_name}/packaged-poc-mlops/cali_mlops/model_inference_batch"
# }

# resource "databricks_notebook" "model_deployment" {
#   path = "/Repos/{data.databricks_current_user.me.user_name}/packaged-poc-mlops/cali_mlops/model_deployment"
# }
  
# resource "databricks_notebook" "model_inference_stream" {
#   path = "/Repos/{data.databricks_current_user.me.user_name}/packaged-poc-mlops/cali_mlops/model_inference_stream"
# }