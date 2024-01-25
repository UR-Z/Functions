###################
'''
Final call should look like: snowflake_connect(sql_syntax_correction(secret_sauce(INPUT,table_info(DATABASE,TABLE))))
'''
####################
import boto3
import json
from snowflake.snowpark import Session
import re
from sqlalchemy import create_engine, inspect
import pandas as pd
import os

# Function to pass table info into LLM
def table_info(database_name,table_name):
    db_path = database_name
    engine = create_engine(f'sqlite:///{db_path}')
    
    conn = engine.connect()
    inspector = inspect(engine)
    
    return inspector.get_columns(table_name)
# SQL Syntax correction, adding quotes for string values in where clause
def add_quotes_to_equipment_code(expression):
            # Define the regular expression pattern
            pattern = re.compile(r'(EQUIPMENT_CODE\s*=\s*)([^\s;]+)')

            # Use a lambda function as the replacement to add single quotes around the value
            result = pattern.sub(lambda match: f"{match.group(1)}'{match.group(2)}'", expression)

            return result
# SQL correction, convert double quotes to single or add single quotes to string values        
def sql_syntax_correction(original_query):
        
    pattern = re.compile(r'FROM(.*?)WHERE', re.DOTALL)

        # Find the match in the modified response
    match = pattern.search(original_query)

    if match:
        # Get the content between FROM and WHERE
        content_between_from_and_where = match.group(1).strip()

            # Replace the content with your desired table name
        new_content = "FOOBAR"
        new_response = original_query.replace(content_between_from_and_where, new_content)
        if new_response.find('"') != -1:
            new_response = new_response.replace('"',"'")
            return new_response
        else:
            new_response = add_quotes_to_equipment_code(new_response)
            return new_response

def snowflake_connect(query):
    connection_parameters = {
          "account": os.getenv("SNOWFLAKE_ACCOUNT"),
          "user": os.getenv("SNOWFLAKE_USERNAME"),
          "password": os.getenv("SNOWFLAKE_PASSWORD"),
          "role": "ANALYST",
          "warehouse": "WH_ADHOC"
            }
    session = Session.builder.configs(connection_parameters).create()

    df = session.sql(query)

    df = pd.DataFrame(df.collect())
    
    if df.empty:
        
        results = f'''
        -----------------------------------------------------------
        Query
        {query.upper()}
        -----------------------------------------------------------
        SQL Statement Failed: No results from Snowflake
        '''
        return results
    else:
        
        results = f'''
        -----------------------------------------------------------
        Query
        {query.upper()}
        -----------------------------------------------------------
        Table Results
        {df.to_string(index=False)}
        '''
        return results

# Bedrock LLM call 
def secret_sauce(question,table_info):
    prompt_data = f"""
Human: You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery

Only use the following tables:
{table_info}

Adding additional instructions and information about what to output.

A data dictionary of the table columns are provided in the <Table Data Dictionary> xml tag. The format of the data dictionary is the description of the field, an equal sign and then the actual column name.
You should infer this provided data dictionary as column name synonyms.


<Table Data Dictionary>


</Table Data Dictionary>

<Question>
{question}
</Question>

Assistant:
"""
    body = json.dumps({"inputText": prompt_data,
                 "textGenerationConfig": {
      "maxTokenCount": 4096,
      "stopSequences": [],
      "temperature":0,
      "topP":1
                 }
                  }) 
    

    modelId="amazon.titan-text-express-v1"
    accept = "application/json"
    contentType = "application/json"

    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    
    
    return response_body.get('results')[0]['outputText']


