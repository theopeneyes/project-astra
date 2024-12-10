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

def test_detect_lang_function(): 
    filenames_being_processed: Dict[str, str| None] ={ 
        "Machine-Learning-For-Absolute-Beginners.pdf": "english", 
        "algorithms.pdf": "english", 
        "lbdl.pdf": "english", 
        "gujaratibook.pdf": "gujarati", 
        "hindibook.pdf": "hindi", 
        "lmao.pdf": None,  
    } 

    # Functionality test
    for filename, language in filenames_being_processed.items(): 
        response = requests.post(
            URL + "/detect_lang", 
            json = {
                "filename": filename, 
                "email_id": EMAIL_ID, 
            }
        )

        if response.status_code == 200: 
            response_dict = response.json()
            assert response_dict.get("filename") == filename
            assert response_dict.get("email_id") == EMAIL_ID

            # Quality test 
            assert response_dict.get("detected_language") == language
        