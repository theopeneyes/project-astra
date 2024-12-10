from dotenv import load_dotenv
from google.cloud import storage
from typing import Dict 

import os 
import requests 

# This file tests the convert_pdf endpoint 
BASE_PATH: str = "./"

# loading the environment variables 
load_dotenv(os.path.join(
    BASE_PATH, 
    ".env"
))

URL: str = os.getenv("LLM_API_URL") 
EMAIL_ID: str = "test.third@yahoo.com"
BUCKET_NAME: str = os.getenv("BUCKET_NAME")

# setting up a client 
gcs_client = (storage.Client
        .from_service_account_json(
                os.path.join(
                   BASE_PATH, 
                   ".secrets", 
                   "gcp_bucket.json"
                )
)) 

bucket = gcs_client.bucket(BUCKET_NAME)

def test_data_loader_function(): 

    filenames_being_processed: Dict[str, int] = {
        "Machine-Learning-For-Absolute-Beginners.pdf": 128, 
        "algorithms.pdf": 100, 
        "gujaratibook.pdf": 50, 
        "lbdl.pdf": 185, 
        "hindibook.pdf": 50, 
        "lmao.pdf": 0, 
    } 

    for filename, page_count in filenames_being_processed.items():   
        response = requests.post(
            URL + "/data_loader", 
            json = {
                "filename": filename,  
                "email_id": EMAIL_ID, 
            }
        )