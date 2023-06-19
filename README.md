# Packaged POC

1. Clone the repo and open IDE

```
$ git clone git@github.com:Zaxier/packaged-poc-mlops.git
...
$ cd packaged-poc-mlops
...
$ code .
...
```

```
python -m venv dbx
source dbx/bin/activate
```

```
cd terraform/cali_mlops/jobs-existing-cluster
terraform init
terraform plan
terraform apply

```

Must have configured databricks cli already


# TODO Add feature importance to model training