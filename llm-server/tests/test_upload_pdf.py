from dotenv import load_dotenv
from google.cloud import storage
from pdfreader import PDFDocument
from typing import Dict 

import os 
import json 
import requests 

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

def test_empty_pdf(): 

    filename: str = "empty.pdf"
    filepath: str = os.path.join(
        SAMPLE_PDF, 
        filename, 
    )

    with open(filepath, "w") as fp: 
        fp.write("")

    with open(filepath, "rb") as fp: 
        response = requests.post(
            URL + "/upload_pdf", 
            data = {
                "filename": filename,  
                "email_id": EMAIL_ID, 
            }, 
            files= {
                "pdf": fp, 
            }
        )
    
        assert response.status_code == 404
        response_dict: dict[str, str] = response.json()
        exception: str = response_dict.get("detail").split(":")[0].strip()
        assert exception == "EmptyPDFException"

def test_saving_pdf(): 

    filename: str = "sample.pdf"
    filepath: str = os.path.join(
        SAMPLE_PDF, 
        filename, 
    )

    with open(filepath, "wb") as fp: 
        fp.write(b"Hello lol")

    with open("./sample.pdf", "rb") as fp: 
        response = requests.post(
            URL + "/upload_pdf", 
            data = {
                "filename": filename,  
                "email_id": EMAIL_ID, 
            }, 
            files= {
                "pdf": fp, 
            }
        )
    
        assert response.status_code == 200 
        response_dict: dict[str, str] = response.json()
        assert EMAIL_ID == response_dict.get("email_id")
        assert filename == response_dict.get("filename") 
        assert isinstance(response_dict.get("time"), float)

        blob = bucket.blob(os.path.join(
            EMAIL_ID, 
            "uploaded_document", 
            filename, 
        ))

        assert blob.exists()
    
def test_measure_pages(): 
    filenames_being_processed: Dict[str, int] = {
        "Machine-Learning-For-Absolute-Beginners.pdf": 128, 
        "lbdl.pdf": 185, 
    } 

    # Functionality test
    for filename, pages in filenames_being_processed.items(): 
        filepath: str = os.path.join(
            TEST_BOOKS, 
            filename, 
        )

        with open(filepath, "rb") as fp: 
            response = requests.post(
                URL + "/upload_pdf", 
                data = {
                    "filename": filename,  
                    "email_id": EMAIL_ID, 
                }, 
                files = {
                    "pdf": fp,            
                }
            )

            if response.status_code == 200: 
                response_dict: dict = response.json()

                # test the response 
                assert response_dict.get("filename") == filename
                assert response_dict.get("email_id") == EMAIL_ID

                try: 
                    blob = bucket.blob(os.path.join(
                        EMAIL_ID, 
                        "uploaded_document", 
                        filename, 
                    ))

                    with blob.open("rb") as f:
                        pdf_book = PDFDocument(f)                     
                        page_read_count = len(list(pdf_book.pages()))  
                    assert page_read_count == pages

                except Exception as err: 
                    error_name: str = type(err).__name__
                    error_at: int = err.__traceback__.tb_lineno
                    assert f"Error by name: {error_name} at line {error_at}." 
                    assert "Unexpected result since the response is 200"

            else: 
                assert response.status_code == 404 
                

    






    
