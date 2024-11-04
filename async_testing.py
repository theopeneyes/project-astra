# testing of the api 
import requests 
import random 
import time 
import asyncio
import aiohttp 
import os 
import json 

from typing import List, Dict 
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

# defined variables 
BUCKET_NAME: str = os.getenv("BUCKET_NAME")
EMAIL_ID: str = "prat16here@gmail.com"
BLOB_BASE_PATH: str = f"{EMAIL_ID}/uploaded_document"
URL = "http://127.0.0.1:8000"

gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

BASE_DIR: str = "pdfs"

# uploading these test pdfs to the bucket 
pdf_names: List[str] = os.listdir(BASE_DIR)
blob_paths: List[str] = []

# sync vs async uploads of pdf 
def upload_pdf(
        pdf_dir: str, 
        pdf_name: str, 
        blob_path: str, 
        blob_paths: List[str]
    ) -> None : 
    with open(os.path.join(pdf_dir, pdf_name), "rb") as f: 
        content = f.read()

        pdf_document_blob = bucket.blob(
            os.path.join(
                blob_path, 
                pdf_name 
            ) 
        )
        
        # storing the base paths 
        blob_paths.append(
            os.path.join(
                blob_path, 
                pdf_name 
            ) 
        )

        pdf_document_blob.open("wb").write(content)
async def async_upload_pdf(
        pdf_dir: str, 
        pdf_name: str, 
        blob_path: str, 
        blob_paths: List[str]
    ) -> None : 
    with open(os.path.join(pdf_dir, pdf_name), "rb") as f: 
        content = f.read()

        pdf_document_blob = bucket.blob(
            os.path.join(
                blob_path, 
                pdf_name.split(".pdf")[0] + "_test.pdf" 
            ) 
        )
        
        # storing the base paths 
        blob_paths.append(
            os.path.join(
                blob_path, 
                pdf_name.split(".pdf")[0] + "_test.pdf" 
            ) 
        )

        pdf_document_blob.open("wb").write(content)

# sync vs async transforming pdf to images
def transform_pdf(url: str, input_json: Dict[str, str]) -> Dict[str, str]:
    response = requests.post(url, json=input_json) 
    return response.json()
async def async_transform_pdf(url: str, input_json: Dict[str, str]) -> Dict[str, str]: 
    async with aiohttp.ClientSession() as session: 
        async with session.post(url, json=input_json) as response:
            return await response.json()
   
# sync vs async image to html 
def structure_pages(url: str, converter_response: Dict[str, str]) -> Dict[str, str]:  
    response = requests.post(url, json=converter_response)
    return response.json()
async def async_structure_pages(url: str, converter_response: Dict[str, str]) -> Dict[str, str]: 
    async with aiohttp.ClientSession() as session: 
        async with session.post(url, json=converter_response) as response: 
            return await response.json()

# synchronous classification 
def classify(
        url: str, 
        page_number: int, 
        pdf_name: str, 
        email_id=EMAIL_ID
    ) -> Dict[str, str]: 

    response = requests.post(
        url, 
        json = {
            "email_id": email_id, 
            "page_number": page_number, 
            "filename": pdf_name
        }
    )
    return response.json() 

# asynchronous classification 
async def async_classify(
        url: str, 
        page_number: int, 
        pdf_name: str, 
        email_id=EMAIL_ID
) -> Dict[str, str]: 
    
    async with aiohttp.ClientSession() as session: 
        async with session.post(url, json={
            "email_id": email_id, 
            "filename": pdf_name, 
            "page_number": page_number
        }) as response: 
            return await response.json()

# async entire pipeline 
async def pipeline(
    url: str, pdf_dir: str, 
    pdf_name: str, blob_path: str, 
    blob_paths: List[str]) -> List:

    await async_upload_pdf(pdf_dir, pdf_name, blob_path, blob_paths)
    input_json: Dict[str, str] = {
        "email_id": EMAIL_ID, 
        "filename": pdf_name, 
        "uri": os.path.join(blob_path, pdf_name) 
    }
    converted_response = await async_transform_pdf(url + "/convert_pdf", input_json)
    structured_pages_response = await async_structure_pages(
        url + "/data_loader", converted_response)
    results: List = [] 
    for idx in range(structured_pages_response["page_count"]): 
        results.append(
            await async_classify(url + "/data_classifier", idx, pdf_name))    

    return results  

def run_sync(pdf_names: List[str]): 
    for pdf_name in pdf_names: 
        upload_pdf(BASE_DIR, pdf_name, BLOB_BASE_PATH, blob_paths)

        input_json: Dict[str, str] = dict(
            email_id=EMAIL_ID, 
            uri=os.path.join(BLOB_BASE_PATH, pdf_name), 
            filename=pdf_name, 
        ) 

        sync_result = transform_pdf(URL + "/convert_pdf", input_json) 
        html_json_sync: Dict = structure_pages(URL + "/data_loader", sync_result) 
        

        responses = []
        for i in range(html_json_sync["page_count"]): 
            responses.append(classify(
                URL + "/data_classifier", 
                i, pdf_name, 
                EMAIL_ID
            )) 

async def run_async(pdf_names): 
    await asyncio.gather(
        *[asyncio.create_task(async_upload_pdf(BASE_DIR, 
            pdf_name, BLOB_BASE_PATH, blob_paths))  
            for pdf_name in pdf_names]
    )

    async_results = await asyncio.gather(
        *[asyncio.create_task(async_transform_pdf(
            URL + "/convert_pdf", {
                "email_id": EMAIL_ID, 
                "uri":os.path.join(BLOB_BASE_PATH, pdf_name), 
                "filename": pdf_name, 
            } 
        )) for pdf_name in pdf_names]
    )

    html_json_async: List[Dict] = await asyncio.gather(
        *[asyncio.create_task(async_structure_pages(
            URL + "/data_loader", async_result)) 
            for async_result in async_results]
    )

    for async_html in html_json_async: 
        classified_output: List[Dict] = await asyncio.gather(
            *[asyncio.create_task(async_classify(
                URL + "/data_classifier", 
                page_number, 
                async_html["filename"], 
                async_html["email_id"], 
            )) for page_number in range(async_html["page_count"])]
        )
async def run_async_at_once(pdf_names): 

    pipeline_output = await asyncio.gather(
        *[asyncio.create_task(
            pipeline(URL, BASE_DIR, pdf_name, BLOB_BASE_PATH, blob_paths)
        ) for pdf_name in pdf_names]
    )
    
async def stats() -> Dict[str, int]: 
    # running pdf uploads synchronously 
    stat: Dict[str, int] = {}
    elems: int = random.randint(1, len(os.listdir(BASE_DIR)))

    pdf_names: List[str] = random.sample(os.listdir(BASE_DIR), elems) 

    init = time.time()
    run_sync(pdf_names)
    duration = time.time() - init 
    stat["sync"] = duration

    # running pdf uploads asynchronously  
    init = time.time()
    blob_paths.clear() 
    await run_async(pdf_names)
    duration = time.time() - init 

    stat["async"] = duration 
    
    blob_paths.clear()
    init = time.time()
    await run_async_at_once(pdf_names)
    duration = time.time() - init 
    stat["at_once"] = duration 

    return stats

async def main(): 
    result : List[Dict[str, str]] = await asyncio.gather(
        *[asyncio.create_task(
            stats()
        ) for _ in range(30)]
    )
    
    with open(".test_result/result.json", "w") as json_fp: 
        json.dump(result, fp=json_fp)

def func(): 
    blobs = gcs_client.list_blobs(BUCKET_NAME)
    for blob in blobs: 
        print(blob.name)

if __name__ == '__main__': 
    func()
    

# next is converting this pdf by making a request to the conversion model 
# for path, pdf_name in zip(blob_paths, pdf_names):  
#     requests.post(
#         url = URL + "/convert_pdf", 
#         json = {
#             "email_id": EMAIL_ID, 
#             "uri": path,  
#             "filename": pdf_name,  
#         }
#     )


