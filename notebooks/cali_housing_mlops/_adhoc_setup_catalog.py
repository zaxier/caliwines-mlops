# Databricks notebook source

from packaged_poc.common import MetastoreTable, MetastoreCatalog, MetastoreSchema

# COMMAND ----------
dev_catalog = MetastoreCatalog("zaxier_dev")
staging_catalog = MetastoreCatalog("zaxier_staging")
prod_catalog = MetastoreCatalog("zaxier_prod")

# COMMAND ----------
dev_catalog.demo_create_managed_external_catalog()
staging_catalog.demo_create_managed_external_catalog()
prod_catalog.demo_create_managed_external_catalog()


# COMMAND ----------
dev_landing_schema = MetastoreSchema(catalog="zaxier_dev", name="landing")
dev_landing_schema.create_if_not_exists()
