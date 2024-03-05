########################################
"""
Function Library
Example Usage:
from pa_common.Functions.snowflake_logger import snowflake_logger
"""
########################################


from dotenv import load_dotenv
import os
import pandas as pd
from snowflake.snowpark import Session
from datetime import datetime



class snowflake_logger():
    def __init__(self, env_filepath, app_type, app_link, app_version):
        self.env_filepath = env_filepath
        self.app_type = app_type
        self.app_link = app_link
        self.app_version = app_version
        self.logtime = datetime.now()
        self.logtime = self.logtime.strftime("%Y-%m-%d %H:%M:%S")

        self.snowflake_connector()

    def snowflake_connector(self):
        load_dotenv(self.env_filepath)
        connection_parameters = {
        "account": os.getenv('SNOWFLAKE_ACCOUNT'),
        "user": os.getenv('SNOWFLAKE_USERNAME'),
        "password": os.getenv('SNOWFLAKE_PASSWORD'),
        "role": "ANALYST",
        "warehouse": "WH_ADHOC",
        # OPTIONAL "database": os.getenv('DATABASE'),
        # OPTIONAL "schema": os.getenv('SCHEMA')
        }

        try:
            session = Session.builder.configs(connection_parameters).create()
            session.sql(
            "insert into discovery.dla_a_25195.application_logs (log_time, application_type, application_link, application_version) values (?,?,?,?);"
            ,params=[self.logtime,self.app_type,self.app_link,self.app_version]).collect()
            print("Connected to Snowflake")
        except:
            print("Error connecting to Snowflake")





  



   
