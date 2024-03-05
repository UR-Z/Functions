########################################
"""
Claude 3 function set up as a single use, 
can be applied to other functions such as metadata_builder but note the difference in the body variable.

Claude 3 with image modality added as cluade_3_image function. Encode in base64.
"""
########################################

import os
import boto3
import json
def claude_3(prompt):

    body = json.dumps({
                "max_tokens": 256,
                "messages": [{"role": "user", "content": prompt}],
                "anthropic_version": "bedrock-2023-05-31"
                })

    
        #Run Inference
    modelId = "anthropic.claude-3-sonnet-20240229-v1:0"  # change this to use a different version from the model provider if you want to switch 
    accept = "application/json"
    contentType = "application/json"

    bedrock = boto3.client(service_name='bedrock-runtime',region_name='us-west-2',
                           aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    
    
    return response_body.get('content')[0]['text']



def claude_3_image(prompt,image):

    body = json.dumps({
            "max_tokens": 256,
            "messages": [{"role": "user", "content":
                          [
                           {
                               "type":"image",
                               "source":{
                                   "type":"base64",
                                   "media_type":"image/jpeg",
                                   "data":image,
                               }
                           },
                           {"type":"text","text":prompt}   
                          ]
                          }],
            "anthropic_version": "bedrock-2023-05-31"
            })


        #Run Inference
    modelId = "anthropic.claude-3-sonnet-20240229-v1:0"  # change this to use a different version from the model provider if you want to switch 
    accept = "application/json"
    contentType = "application/json"

    bedrock = boto3.client(service_name='bedrock-runtime',region_name='us-west-2',
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    
    
    return response_body.get('content')[0]['text']