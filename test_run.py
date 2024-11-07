from google.cloud import storage 
from typing import List, Dict 
from dotenv import load_dotenv

import requests 
import os 

load_dotenv()


def process_pdf(pdf_name: str, user_email: str, gcs_client): 
    with open(os.path.join(PDF_DIR, pdf_name), "rb") as fr: 
        pdf_blob = bucket.blob(f"{EMAIL_ID}/uploaded_document/{pdf_name}")
        with pdf_blob.open("wb") as f:
            f.write(fr.read())

    # Asking the endpoint to convert the pdf
    print(f"Currently at converting stage for pdf {pdf_name}...")
    convert_response = requests.post(
        URL + "/convert_pdf", json = {
            "email_id": user_email, 
            "uri": f"{user_email}/uploaded_document/{pdf_name}", 
            "filename": pdf_name,  
        })
    
    convert_output : Dict = convert_response.json()
    
    print(f"Currently at data_loading and processing state for {pdf_name}...") 
    data_loader_response = requests.post(
        URL + "/data_loader", 
        json = convert_output, 
    )

    print(f"Currently at summarizing stage for pdf {pdf_name}...")
    data_loader_output: Dict = data_loader_response.json()

    # generating summary 
    summarized_blob_path: str = f"{user_email}/summaries/{pdf_name}/" 

    # could cause a problem if the pdf already exists 
    blobs = gcs_client.list_blobs(
        BUCKET_NAME, 
        prefix=summarized_blob_path, 
        delimiter="/", 
    )

    print(f"Storing summary blobs for pdf {pdf_name}...")
    for blob in blobs: 
        if blob.name.endswith("_content.txt"):
            requests.post(
                URL + "/summarize", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "chapter_title": blob.name.split("/")[3], 
                }
            )
    

    print(f"Generating a classified output for pdf {pdf_name}...")
    for idx in range(data_loader_output["page_count"]):  
        requests.post(
            URL + "/data_classifier", 
            json = {
                "filename": pdf_name, 
                "email_id": user_email, 
                "page_number": idx,  
            }
        )

 
PORT: str = "4000"
URL: str = f"http://127.0.0.1:{PORT}"
PDF_DIR: str = "test_books"

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


def main():
    for pdf_name in os.listdir(PDF_DIR): 
        process_pdf(pdf_name, EMAIL_ID, gcs_client)

if __name__ == "__main__": 
    main()

    # classifier_blobs = gcs_client.list_blobs(
    #     BUCKET_NAME, 
    #     prefix=f"{user_email}/json_data/", 
    #     delimiter="/", 
    # )

    # json_outputs : List[Dict] = [] 
    # for blob in classifier_blobs: 
    #     if blob.name.contains(pdf_name): 
    #         f = blob.open("r")
    #         json_outputs.append(f.read())
    #         f.close()
    
        
    
    
    
    


    
    
    





