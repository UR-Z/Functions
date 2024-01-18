import requests
import boto3
import json

#### Main function, will batch label
def metadata_function(documents,query,metadata_name):
    for i, doc in enumerate(documents):
        documents[i].metadata[metadata_name] = secret_sauce(documents[i].page_content,query)
        test = documents[i].metadata
############# Use one of the two secret_sauce functions with metadata_function to batch label. Use view_test_function first to view one document output.

### AWS COMPREHEND (This calls sentiment but can be adjusted for other functions)
def secret_sauce(document):
    try:
        client = boto3.client('comprehend')
        response = client.detect_sentiment(
            Text=document[:4997], #5000 bytes max limit
            LanguageCode='en'
        )
        return response['Sentiment']
    except Exception as e:
        #print(f"An error occurred: {e}")
        return 'BAD_DATA_INPUT'

### LLM Handler, input prompts to be used for labelling needs
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

    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    
    
    return response_body.get('completion').strip(' ')

            
#### Use function to test and view prompt results on a single document
def view_test_function(x,documents,query,name):
    print(f'''
#########################################
SCRIPT:
    {documents[x].page_content}
#########################################
METADATA:
    {documents[x].metadata}
''')

####Testing functions

    prompt_data = f"""
Human:
{query}

<transcript>
{sample[x].page_content}
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

    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    
    
    print(f''' Test Function Result
{function_name}:{response_body.get('completion').strip(' ')}''')
