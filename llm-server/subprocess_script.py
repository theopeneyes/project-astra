import pandas as pd 
from io import BytesIO
import os 
import requests
import json 
import sys
from google.cloud import storage
from openai import OpenAI 
from dotenv import load_dotenv
import tiktoken 
from generate_qna.generator import generate_qna_for_topic_sync
import logging 
logger = logging.getLogger(__name__)

filename: str = sys.argv[1]
email_id : str = sys.arg[2]

class ProcessRequest: 
    filename: str 
    email_id: str

load_dotenv(override=True)

BUCKET_NAME: str = os.environ.get("BUCKET_NAME")
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY") 

gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

gpt4o = OpenAI(api_key=OPENAI_API_KEY)
gpt4o_encoder = tiktoken.encoding_for_model("gpt-4o-mini")

request = ProcessRequest()
request.filename = filename 
request.email_id = email_id

def process_topics():
    try:
        final_json_blob = bucket.blob(f"{request.email_id}/final_json/{request.filename.split('.')[0]}.json")
        with final_json_blob.open("r") as blb:
            json_qna: list[dict] = json.load(blb)
        
        df = pd.DataFrame(json_qna)
        all_data = []
        
        for topic_name, topic_df in df.groupby("topic"):
            topic_texts = topic_df["text"].tolist()
            topic_result = generate_qna_for_topic_sync(topic_name, topic_texts, gpt4o, gpt4o_encoder)
            
            output_path = f"{request.email_id}/excel_output/{topic_name}_{request.filename.split('.')[0]}.csv"
            csv_blob = bucket.blob(output_path)
            
            topic_df = pd.DataFrame(topic_result)
            
            with BytesIO() as output:
                topic_df.to_csv(output, index=False)
                csv_blob.upload_from_string(output.getvalue(), content_type='text/csv')
            
            for row in topic_result:
                row["topic"] = topic_name
                all_data.append(row)
        
        final_csv_path = f"{request.email_id}/excel_output/{request.filename.split('.')[0]}_qna.csv"
        csv_blob = bucket.blob(final_csv_path)
        final_df = pd.DataFrame(all_data)

        send_email_notification(request.email_id)
        with BytesIO() as output:
            final_df.to_csv(output, index=False)
            csv_blob.upload_from_string(output.getvalue(), content_type='text/csv')
        
    except Exception as err:
        logger.error(f"Error generating CSV: {str(err)}")

def send_email_notification(email: str):
    payload = {
        "request_key": "OpenEyes_1224EzZykXxo",
        "email_key": "RequestComplated",
        "request_emails": [email],
        "dynamic_data": {"current_year": "2025"}
    }
    
    try:
        response = requests.post("https://oeservices.uatbyopeneyes.com/api/v1/sendMailWithOpenEyesMT", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error sending email: {str(e)}")