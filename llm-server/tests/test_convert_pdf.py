from dotenv import load_dotenv
from google.cloud import storage
from typing import Dict , List

import os 
import json 
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

# # The endpoint is algorithmic and therefore no quality tests assigned. 
# def test_convert_pdf_function(): 
#     filenames_being_processed: Dict[str, int] = {
#         "Machine-Learning-For-Absolute-Beginners.pdf": 128, 
#         "algorithms.pdf": 100, 
#         "gujaratibook.pdf": 50, 
#         "lbdl.pdf": 185, 
#         "hindibook.pdf": 50, 
#         "lmao.pdf": 0, 
#     } 

#     # Functionality test
#     for filename, pages in filenames_being_processed.items(): 
#         uri : str = os.path.join(
#             EMAIL_ID, 
#             "uploaded_document", 
#             filename, 
#         ) 

#         response = requests.post(
#             URL + "/convert_pdf", 
#             json = {
#                 "filename": filename,  
#                 "email_id": EMAIL_ID, 
#                 "uri":uri,              }
#         )

#         if response.status_code == 200: 
#             response_dict = response.json()

#             # test the response 
#             assert response_dict.get("filename") == filename
#             assert response_dict.get("email_id") == EMAIL_ID

#             # testing if the number of images generated is the same as the number of pages within the book 
#             response_uri: str = response_dict.get("uri")
#             try: 
#                 image_blob = bucket.blob(response_uri)
#                 with image_blob.open("r") as f: 
#                     image_json: List = json.load(fp=f)
                
#                 assert len(image_json) == pages

#             except Exception as err: 
#                 error_name: str = type(err).__name__
#                 error_at: int = err.__traceback__.tb_lineno
#                 assert f"Error by name: {error_name} at line {error_at}." 
#                 assert "Unexpected result since the response is 200"

#         else: 
#             assert response.status_code == 404 



import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is in main.py

client = TestClient(app)

def test_missing_images_in_conversion():
    # Simulate a PDF file with missing images (or a test case where conversion fails for some pages)
    pdf_file = {
        "filename": "",
        "email_id": "test@example.com",
        "uri": "uploaded_document/test_book.pdf"
    }

    response = client.post("/convert_pdf", json=pdf_file)
    
    # Assuming missing pages are detected
    assert response.status_code == 404
    assert "Missing images for pages" in response.json()["detail"]
            