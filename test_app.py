import streamlit as st 
import os 

from google.cloud import storage

BUCKET_NAME: str = os.getenv("BUCKET_NAME") # name of the bucket 
PROMPT_FILE_ID: str =  os.getenv("FILE_ID") # file_id to fetch remote prompt design sheet
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") # gemini api key 
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") # openai api key 
HF_TOKEN: str = os.getenv("HF_TOKEN") # huggingface token 
EMAIL_ID: str = "test.final@gmail.com"

# client 
gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
# bucket 
bucket = gcs_client.bucket(BUCKET_NAME)

with st.sidebar:
    book_name = st.selectbox(
        label="Select one of the following pdfs...",
        options=[blob.name.split("/")[-1] for blob in gcs_client.list_blobs(
            BUCKET_NAME, 
            prefix=f"{EMAIL_ID}/uploaded_document/", 
            delimiter="/"
        )]
    )

    
    