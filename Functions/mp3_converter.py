###
## NOTES
"""
Functions to batch extract a regular expression, download and convert files to mp3 format.
"""

###
import re

def extract_value(text):
    pattern = r'transcripts_(.+)\.txt'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

# Assuming df is your DataFrame and you want to apply the function to a specific column
df['extracted_value'] = df['source'].apply(lambda x: extract_value(x))


# Need a function that will download a file from an s3 bucket
import boto3
import os
from dotenv import load_dotenv

load_dotenv('../env.env')


def download_file(bucket, key):
    s3 = boto3.client('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    s3.download_file(bucket, key, key)


from moviepy.editor import AudioFileClip

def convert_webm_to_mp3(input_file, output_file):
    try:
        # Load the .webm file
        clip = AudioFileClip(input_file)
        
        # Write the audio to .mp3 format
        clip.write_audiofile(output_file)
        
        print("Conversion successful.")
    except Exception as e:
        print("Error:", e)
