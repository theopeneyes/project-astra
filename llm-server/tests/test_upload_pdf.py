from dotenv import load_dotenv
from google.cloud import storage
from pdfreader import PDFDocument
from typing import Dict 
import pyrebase 


from fastapi import HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
# from models import PDFUploadResponseModel 
from fastapi.testclient import TestClient
from main import app 
client = TestClient(app)

import os 
import json 
import requests 
import pytest

BASE_PATH: str = "./"
load_dotenv(os.path.join(
    BASE_PATH, 
    ".env"
))

URL: str = os.getenv("LLM_API_URL") 
EMAIL_ID: str = "test.third@yahoo.com"
BUCKET_NAME: str = os.getenv("BUCKET_NAME")
SAMPLE_PDF: str = "" 
TEST_BOOKS: str = os.path.join(
    "..", 
    "streamlit-app", 
    "test_books", 
)

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

# Firebase configuration
FIREBASE_CONFIG: Dict[str, str] = json.loads(os.getenv("FIREBASE_CLIENT")) 
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()

# def test_empty_pdf(): 

#     filename: str = "empty.pdf"
#     filepath: str = os.path.join(
#         SAMPLE_PDF, 
#         filename, 
#     )

#     with open(filepath, "w") as fp: 
#         fp.write("")

#     with open(filepath, "rb") as fp: 
#         response = requests.post(
#             URL + "/upload_pdf", 
#             data = {
#                 "filename": filename,  
#                 "email_id": EMAIL_ID, 
#             }, 
#             files= {
#                 "pdf": fp, 
#             }
#         )
    
#         assert response.status_code == 404
#         response_dict: dict[str, str] = response.json()
#         exception: str = response_dict.get("detail").split(":")[0].strip()
#         assert exception == "EmptyPDFException"

# test_empty_pdf()
# def test_unsupported_pdf():
#     filename: str = "testsample.pdf"
  
#     with open(filename, "rb") as fp:

#         response = requests.post(
#             URL + "/upload_pdf", 
#             data = {
#                 "filename": filename, 
#                 "email_id": EMAIL_ID, 
#             }, 

#             files = {
#                 "pdf": fp, 
#             }

#         )

        

#         response = requests.post(
#             URL + "/convert_pdf",  
#             json={
#                 "filename": filename,
#                 "email_id": EMAIL_ID,  
#                 "uri": f"{EMAIL_ID}/uploaded_document/{filename}"
#             }
#         )

#         assert response.status_code == 404
#         response_dict: dict = response.json()
#         exception = response_dict.get("detail").split(":")[0].strip()
#         assert exception == "UnsupportedPDFException"

# def test_saving_pdf(): 

#     filename: str = "sample.pdf"
#     filepath: str = os.path.join(
#         SAMPLE_PDF, 
#         filename, 
#     )

#     with open(filepath, "wb") as fp: 
#         fp.write(b"Hello lol")

#     with open("./sample.pdf", "rb") as fp: 
#         response = requests.post(
#             URL + "/upload_pdf", 
#             data = {
#                 "filename": filename,  
#                 "email_id": EMAIL_ID, 
#             }, 
#             files= {
#                 "pdf": fp, 
#             }
#         )
    
#         assert response.status_code == 200 
#         response_dict: dict[str, str] = response.json()
#         assert EMAIL_ID == response_dict.get("email_id")
#         assert filename == response_dict.get("filename") 
#         assert isinstance(response_dict.get("time"), float)

#         blob = bucket.blob(os.path.join(
#             EMAIL_ID, 
#             "uploaded_document", 
#             filename, 
#         ))

#         assert blob.exists()
    
# def test_measure_pages(): 
#     filenames_being_processed: Dict[str, int] = {
#         "Machine-Learning-For-Absolute-Beginners.pdf": 128, 
#         "lbdl.pdf": 185, 
#     } 

#     # Functionality test
#     for filename, pages in filenames_being_processed.items(): 
#         filepath: str = os.path.join(
#             TEST_BOOKS, 
#             filename, 
#         )

#         with open(filepath, "rb") as fp: 
#             response = requests.post(
#                 URL + "/upload_pdf", 
#                 data = {
#                     "filename": filename,  
#                     "email_id": EMAIL_ID, 
#                 }, 
#                 files = {
#                     "pdf": fp,            
#                 }
#             )

#             if response.status_code == 200: 
#                 response_dict: dict = response.json()

#                 # test the response 
#                 assert response_dict.get("filename") == filename
#                 assert response_dict.get("email_id") == EMAIL_ID

#                 try: 
#                     blob = bucket.blob(os.path.join(
#                         EMAIL_ID, 
#                         "uploaded_document", 
#                         filename, 
#                     ))

#                     with blob.open("rb") as f:
#                         pdf_book = PDFDocument(f)                     
#                         page_read_count = len(list(pdf_book.pages()))  
#                     assert page_read_count == pages

#                 except Exception as err: 
#                     error_name: str = type(err).__name__
#                     error_at: int = err.__traceback__.tb_lineno
#                     assert f"Error by name: {error_name} at line {error_at}." 
#                     assert "Unexpected result since the response is 200"

#             else: 
#                 assert response.status_code == 404 
                

    






    
# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import patch, MagicMock
# from main import app  # Assuming your FastAPI app is in main.py
# client = TestClient(app)
# @pytest.fixture
# def mock_gcp_bucket():
#     """Mock GCP bucket and its blob behavior."""
#     with patch("main.storage.Client") as mock_storage_client:
#         mock_bucket = MagicMock()
#         mock_blob = MagicMock()
#         # Mock blob behavior for fetching and uploading rate-limit metadata
#         def mock_blob_download_as_text():
#             return '{"count": 4, "reset_time": 2147483647}'
#         mock_blob.download_as_text = MagicMock(side_effect=mock_blob_download_as_text)
#         mock_blob.upload_from_string = MagicMock()
#         mock_bucket.blob = MagicMock(return_value=mock_blob)
#         mock_storage_client.return_value.bucket.return_value = mock_bucket
#         yield mock_bucket, mock_blob
# def test_rate_limit_exceeded(mock_gcp_bucket):
#     email_id = "test@example.com"
#     filename = "test.pdf"
#     file_content = b"%PDF-1.4 Test content"
#     files = {"pdf": ("test.pdf", file_content, "application/pdf")}
#     data = {"email_id": email_id, "filename": filename}
#     # Simulate 5 successful requests within the allowed rate limit
#     for _ in range(5):
#         response = client.post("/upload_pdf", data=data, files=files)
#         assert response.status_code == 200
#         assert "email_id" in response.json()
#         assert "filename" in response.json()
#         assert "time" in response.json()
#     # Mock rate-limit metadata for the 6th request
#     mock_gcp_bucket[1].download_as_text.side_effect = lambda: '{"count": 5, "reset_time": 2147483647}'
#     # 6th request should trigger rate limit
#     response = client.post("/upload_pdf", data=data, files=files)
#     assert response.status_code == 429
#     assert "detail" in response.json()
#     assert "Rate limit exceeded" in response.json()["detail"]


load_dotenv()

# BUCKET_NAME: str = os.getenv("BUCKET_NAME") # name of the bucket 
# PROMPT_FILE_ID: str =  os.getenv("FILE_ID") # file_id to fetch remote prompt design sheet
# GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") # gemini api key 
# OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") # openai api key 
# HF_TOKEN: str = os.getenv("HF_TOKEN") # huggingface token 
# NODE_SERVER_URL: str = "http://127.0.0.1:5173"
# URL: str = "http://127.0.0.1:8000"

# gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
# # bucket 
# bucket = gcs_client.bucket(BUCKET_NAME)

# # firebase login 
# FIREBASE_CONFIG: Dict[str, str] = json.loads(os.getenv("FIREBASE_CLIENT")) 

# # firebase config 
# firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
# auth = firebase.auth()


# # Mock user credentials for testing (you can mock user login for test purposes)
# def get_mock_user_token():
#     user = auth.sign_in_with_email_and_password("test@example.com", "password")
#     return user['idToken']


# def test_upload_pdf_authenticated():
#     email_id = "test@example.com"
#     filename = "test.pdf"
#     file_content = b"%PDF-1.4 Test content"
#     files = {"pdf": ("test.pdf", file_content, "application/pdf")}
#     data = {"email_id": email_id, "filename": filename}
#     # Get the valid Firebase ID token for the mock user
#     id_token = get_mock_user_token()
#     data["id_token"] = id_token
#     # Simulate the request to upload PDF
#     response = client.post("/upload_pdf", data=data, files=files)
#     assert response.status_code == 200
#     assert response.json() == {
#         "email_id": email_id,
#         "filename": filename,
#         "time": pytest.approx(response.json()['time'], rel=1e-2)
#     }
# def test_upload_pdf_unauthenticated():
#     email_id = "test@example.com"
#     filename = "test.pdf"
#     file_content = b"%PDF-1.4 Test content"
#     files = {"pdf": ("test.pdf", file_content, "application/pdf")}
#     data = {"email_id": email_id, "filename": filename}
#     # Simulate the request without Firebase ID token (unauthenticated user)
#     response = client.post("/upload_pdf", data=data, files=files)
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Invalid Firebase ID token. Please log in again."}
    
# def test_rate_limit_exceeded():
#     email_id = "test@example.com"
#     filename = "test.pdf"
#     file_content = b"%PDF-1.4 Test content"
#     files = {"pdf": ("test.pdf", file_content, "application/pdf")}
#     data = {"email_id": email_id, "filename": filename}
#     # Get the valid Firebase ID token for the mock user
#     id_token = get_mock_user_token()
#     data["id_token"] = id_token
#     # Simulate 5 successful requests within the allowed rate limit
#     for _ in range(5):
#         response = client.post("/upload_pdf", data=data, files=files)
#         assert response.status_code == 200
#     # 6th request should trigger rate limit
#     response = client.post("/upload_pdf", data=data, files=files)
#     assert response.status_code == 429
#     assert "Rate limit exceeded" in response.json()['detail']



# import pytest
# from fastapi.testclient import TestClient
# from main import app  # Assuming your FastAPI app is in main.py

# client = TestClient(app)

# def test_invalid_pdf():
#     # Simulate an invalid PDF (e.g., corrupted or unreadable)
#     invalid_pdf_content = b"%PDF-1.4 corrupted data"  # Simulating a corrupt PDF
#     files = {"pdf": ("corrupted_book.pdf", invalid_pdf_content, "application/pdf")}
#     data = {"email_id": "test@example.com", "filename": "corrupted_book.pdf"}

#     # Send the invalid PDF to the /upload_pdf endpoint
#     response = client.post("/upload_pdf", data=data, files=files)

#     # Assert the response indicates an invalid PDF error
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Invalid PDF: Unable to read or parse the PDF file."



import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is in main.py
from reportlab.pdfgen import canvas
import io

client = TestClient(app)

    # Generate a valid PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "This is a valid PDF document.")
    c.save()
    buffer.seek(0)  # Go back to the beginning of the BytesIO buffer
    return buffer

def create_invalid_pdf():
    # Generate an invalid PDF (simulating corrupted data)
    return b"%PDF-1.4 corrupted data"

def test_upload_valid_pdf():
    # Create a valid PDF dynamically
    valid_pdf_buffer = create_valid_pdf()
    files = {"pdf": ("valid_sample.pdf", valid_pdf_buffer, "application/pdf")}
    data = {"email_id": "test@example.com", "filename": "valid_sample.pdf"}

    # Send the valid PDF to the /upload_pdf endpoint
    response = client.post("/upload_pdf", data=data, files=files)

    # Assert the response is successful (200 OK)
    assert response.status_code == 200
    assert response.json()["filename"] == "valid_sample.pdf"
    assert "time" in response.json()


def test_upload_invalid_pdf():
    invalid_pdf_content = create_invalid_pdf()
    files = {"pdf": ("corrupted_book.pdf", invalid_pdf_content, "application/pdf")}
    data = {"email_id": "test@example.com", "filename": "corrupted_book.pdf"}

    response = client.post("/upload_pdf", data=data, files=files)

    assert response.status_code == 404 
    assert response.json()["detail"] == "Invalid PDF: Unable to read or parse the PDF file."
