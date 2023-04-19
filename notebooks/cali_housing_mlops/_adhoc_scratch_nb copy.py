from packaged_poc.common import MetastoreTable, MetastoreCatalog, MetastoreSchema

# COMMAND ----------
dev_catalog = MetastoreCatalog("zaxier_dev")
staging_catalog = MetastoreCatalog("zaxier_staging")
# prod_catalog = MetastoreCatalog("zaxier_prod")
dev_catalog.check_exists()

# COMMAND ----------
customer_table = MetastoreTable(
    catalog="zaxier_dev", schema="default", table="customer"
)
customer_table.drop()
customer_table.check_exists()

# COMMAND ----------
customer_table._create_basic_table()

# COMMAND ----------
# customer_table.describe_history()

# COMMAND ----------
customer_table.describe()

# COMMAND ----------
# customer_table.describe_extended()
