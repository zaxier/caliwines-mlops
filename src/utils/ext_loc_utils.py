
from utils.get_spark import spark

def get_container_uri_for_ext_loc(ext_loc_name: str = "xavierarmitage-container") -> str:
    try:
        uri = spark.sql(f"describe external location `{ext_loc_name}`").select("url").collect()[0][0]
    except:
        uri = "abfss://xavierarmitage-container@oneenvadls.dfs.core.windows.net"

    # print(f"External location {ext_loc_name} is located at url: {url}" )
    return uri
