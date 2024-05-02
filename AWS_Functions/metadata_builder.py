########################################
"""
Function to test and view prompt results on a single document (view_test_function). Once prompt is approved, use metadata_function to build for all withint a document store.
"""
########################################


import requests
import boto3
import json
import pprint
import os

#### LLM call to build data
def secret_sauce(document,query):
    prompt_data = f"""
Human:
{query}

<transcript>
{document}
</transcript>

<format>
Y
N
</format>

Return only one answer that is displayed in the <format> xml tag. No other text. Return only one character with no whitespace.
Assistant:
"""
    body = json.dumps({"prompt": prompt_data,
                 "max_tokens_to_sample":1000,
                 "temperature":0,
                 "top_k":250,
                 "top_p":0.5,
                 "stop_sequences":[]
                  }) 
    

        #Run Inference
    modelId = "anthropic.claude-instant-v1"  # change this to use a different version from the model provider if you want to switch 
    accept = "application/json"
    contentType = "application/json"

    bedrock = boto3.client('bedrock-runtime','us-west-2',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    
    
    return response_body.get('completion').strip(' ')

def metadata_function(documents,query,metadata_name):
    for i, doc in enumerate(documents):
        documents[i].metadata[metadata_name] = secret_sauce(documents[i].page_content,query)
        test = documents[i].metadata
        #print(f"Processing document {i}: {test}")
            # Your processing logic here
            
#### Use function to test and view prompt results on a single document
def view_test_function(x,documents,query,name):
    pprint.pprint(f'''SCRIPT:{documents[x].page_content}
--------------------------------------
METADATA:{documents[x].metadata}''')

####Testing functions

    prompt_data = f"""
Human:
{query}

<transcript>
{documents[x].page_content}
</transcript>

<format>
Y
N
</format>

Return only one answer that is displayed in the <format> xml tag. No other text. Return only one character with no whitespace.
Assistant:
"""
    
    body = json.dumps({"prompt": prompt_data,
                 "max_tokens_to_sample":1000,
                 "temperature":0,
                 "top_k":250,
                 "top_p":0.5,
                 "stop_sequences":[]
                  }) 
    

        #Run Inference    
    modelId = "anthropic.claude-instant-v1"  # change this to use a different version from the model provider if you want to switch 
    accept = "application/json"
    contentType = "application/json"

    bedrock = boto3.client('bedrock-runtime','us-west-2',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    
    
    print(f'''Test Function Result
--------------------------------------
{name}:{response_body.get('completion').strip(' ')}''')