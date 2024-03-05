########################################
"""
Function was made to collect data from Teradata
and load it into Snowflake.
"""
########################################

from dotenv import load_dotenv
import os
import teradatasql
import pandas as pd

def teradata_connector(query):
    
    conn =  teradatasql.connect(host=os.getenv('TERADATA_URL'), user=os.getenv('TERADATA_USERNAME'), password=os.getenv('TERADATA_PASSWORD'))
    cursor = conn.cursor()
    df=pd.read_sql(query,conn)
    cursor.close()
    conn.close()

    return df

from snowflake.snowpark import Session

def snowflake_loader(df,database_name,schema_name,table_name):
    connection_parameters = {
        "account": os.getenv('SNOWFLAKE_ACCOUNT'),
        "user": os.getenv('SNOWFLAKE_USERNAME'),
        "password": os.getenv('SNOWFLAKE_PASSWORD'),
        "role": os.getenv('SNOWFLAKE_ROLE'),
        "warehouse": os.getenv('SNOWFLAKE_WAREHOUSE'),
        "database": database_name,
        "schema": schema_name
        }


    session = Session.builder.configs(connection_parameters).create()
    try:
        df = session.create_dataframe(df)
        df.write.mode("overwrite").save_as_table(table_name)
        return "Success" 
    except:
        return "Failed"


    