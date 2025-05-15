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

print("Code is working") 

filename: str = sys.argv[1]
email_id : str = sys.argv[2]

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

def process_topics(request):
    try:
        final_json_blob = bucket.blob(f"{request.email_id}/final_json/{request.filename.split('.')[0]}.json")
        with final_json_blob.open("r") as blb:
            json_qna: list[dict] = json.load(blb)
        
        df = pd.DataFrame(json_qna)
        all_data = []
        
        status_blob = bucket.blob(f"{request.email_id}/status/{request.filename.split('.')[0]}_status.txt")
        status_blob.upload_from_string("Processing started", content_type="text/plain")
        
        for topic_name, topic_df in df.groupby("topic"):
            topic_texts = topic_df["text"].tolist()
            topic_name, topic_result, _, _ = generate_qna_for_topic_sync(topic_name, topic_texts, gpt4o, gpt4o_encoder)
            
            output_path = f"{request.email_id}/excel_output/{topic_name}_{request.filename.split('.')[0]}.json"
            json_blob = bucket.blob(output_path)
            
            # Save topic-specific results as JSON
            json_blob.upload_from_string(
                json.dumps(topic_result, indent=2),
                content_type='application/json'
            )
            
            status_blob.upload_from_string(f"Completed: {topic_name}\n", content_type="text/plain")
            print(f"Topic {topic_name} Done")
            
            for row in topic_result:
                row["topic"] = topic_name
                all_data.append(row)
        
        final_json_path = f"{request.email_id}/excel_output/{request.filename.split('.')[0]}_qna.json"
        final_json_blob = bucket.blob(final_json_path)
        
        # Save all results as JSON
        final_json_blob.upload_from_string(
            json.dumps(all_data, indent=2),
            content_type='application/json'
        )
        
        send_email_notification(request.email_id)
        status_blob.upload_from_string("Processing completed", content_type="text/plain")
        
    except Exception as err:
        logger.error(f"Error generating JSON: {str(err)}")
        status_blob = bucket.blob(f"{request.email_id}/status/{request.filename.split('.')[0]}_status.txt")
        status_blob.upload_from_string(f"Error: {str(err)}", content_type="text/plain")
        
process_topics(request)