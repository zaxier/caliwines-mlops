terraform -chdir=terraform/all-purpose-compute init
terraform -chdir=terraform/all-purpose-compute apply -auto-approve -var="env=dev"
