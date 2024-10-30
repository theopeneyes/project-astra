# this file will contain all the fastapi endpoints 

# FastAPI imports 
from fastapi import FastAPI 

from models import DataLoaderModel 
from models import GenerationContext
from models import StructuredJSONModel
from models import DataClassifierModel

from dotenv import load_dotenv # for the purposes of loading hidden environment variables
from typing import Dict, List 

import PIL 
import os 
import json 
import pdf2image as p2i 

from google import generativeai as genai
from openai import OpenAI 

# generation model 
from generation.generate import generate_response
from generation.prompts import prompts 

from data_loader.image_parser import parse_images 
from data_loader.structure import structure_html 
from data_loader.prompts import prompt, clause_prompt 
from data_loader.opeanai_formatters import messages 

from data_classifier.classification_pipeline import get_json
from google.cloud import storage 
from image_utils.encoder import encode_image 

# loads the variables in the .env file 
load_dotenv()

# environment variables: configured in .env file
# these variables will be instantiated once the server starts and 
# the value won't be updated until you restart the server 
# PROMPT_FILE_ID: str = os.getenv("FILE_ID", None) # file_id to fetch remote prompt design sheet
# GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", None) # gemini api key 
# OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", None) # openai api key 
# HF_TOKEN: str = os.getenv("HF_TOKEN", None) # Huggingface token 

PROMPT_FILE_ID: str = os.environ.get("FILE_ID") 
GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY") 
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")
HF_TOKEN: str = os.environ.get("HF_TOKEN")
BUCKET_NAME: str = os.environ.get("BUCKET_NAME")

# error directory 
ERROR_DIR: str = "error_dir"

genai.configure(api_key=GEMINI_API_KEY)

config = genai.GenerationConfig(
    temperature=0,
    top_p = 0.98,
    top_k = 5,
)

# initializing the model clients 
gemini = genai.GenerativeModel(model_name="gemini-1.5-flash-001")
gpt4o = OpenAI(api_key=OPENAI_API_KEY)

# initalizing the bucket client  
gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

# testing phase therefore `debug=True`
app = FastAPI(debug=True, title="project-astra")

# logger 
# def logger(response: Dict[str, str] | Exception):
#     # posts this response or exception to a database that is meant to store logs 
#     pass 

#Endpoints 
@app.get("/")
async def home() -> Dict[str, str]: 
    return {"home": "page"}
    
@app.post("/convert_pdf")
async def convert_pdf(pdf_file: DataLoaderModel) -> DataLoaderModel: 
    # accessing the file blob from the URI 
    pdf_blob = bucket.blob(pdf_file.uri)
    
    images: List[PIL.Image] = p2i.convert_from_bytes(
        pdf_blob.open("rb").read(), 
        dpi=200, 
        fmt="jpg", 
    )

    # encoding the images and saving the encoded json to a directory  
    encoded_images: List[Dict[str, str]] = []
    for img in images: 
        encoded_image: str = encode_image(img) 
        image: Dict[str, str] = {
            "img_name": pdf_file.filename, 
            "img_b64": encoded_image, 
        }

        # formatting it as json 
        encoded_images.append(image)

    json_path: str = f"{pdf_file.email_id}/processed_image/{pdf_file.filename.split('.pdf')[0]}.json"
    json_blob = bucket.blob(json_path)
    
    with json_blob.open("w") as f: 
        f.write(
            json.dumps(encoded_images, ensure_ascii=True)
        )

    return DataLoaderModel(
        filename=pdf_file.filename, 
        email_id=pdf_file.email_id, 
        uri=json_path, 
    ) 
        

# the data loading endpoint 
@app.post("/data_loader")
async def data_loader(user_image_data: DataLoaderModel) -> StructuredJSONModel: 
    # reading the images from the bucket 
    image_json_blob = bucket.blob(user_image_data.uri) 
    with image_json_blob.open("r") as img_json: 
        images: List[Dict[str, str]] = json.load(img_json)

    # sending images to the images function 
    html_pages: List[str] = parse_images(
        models=[gemini, gpt4o], 
        config=config, 
        images=images, 
        prompt=prompt, 
        clause_prompt=clause_prompt, 
        messages=messages,  
    )

    structured_json: List[Dict[str, str|int]] = structure_html(html_pages) 
    
    # writing data from each page into a json file to paralellize the rest of the code from out here 
    for idx, json_page in enumerate(structured_json):
        blob_path: str = f"{user_image_data.email_id}/text_extract/{user_image_data.filename}_{idx}.json"
        json_blob = bucket.blob(blob_path)
        with json_blob.open("w") as f:
            json.dump(json_page, fp=f)
            
    return StructuredJSONModel(
        email_id =user_image_data.email_id, 
        filename=user_image_data.filename, 
        page_count=len(structured_json), 
    ) 
    

# data classifier endpoint  
@app.post("/data_classifier")
async def data_classifier(text_json: DataClassifierModel) -> DataClassifierModel: 
    # getting the specific page data from the classifier model 
    json_path: str = f"{text_json.email_id}/text_extract/{text_json.filename}_{text_json.page_number}.json"
    blob_path = bucket.blob(json_path) 
    with blob_path.open("r") as f: 
        t_json = json.load(f)

    op: Dict[str, Dict|str|None|int|List[str]]|str = get_json(t_json, HF_TOKEN) 
    if op != "": 
       
       # write into gcp 
        classified_blob_path: str = f"{text_json.email_id}/json_data/{text_json.filename}_{text_json.page_number}.json" 
        cls_blob = bucket.blob(classified_blob_path)
        with cls_blob.open("w") as f:
            json.dump(op, fp=f)
       
    return text_json

@app.post("/generate")
async def generate(context: GenerationContext) -> Dict[str, str]:
    qna_prompt: str = prompts[context.question_type]
    qna: str = generate_response(
       prompt=qna_prompt, 
       context=context.context, 
       hf_token=HF_TOKEN, 
       model="mistral",  
       topics=context.topics, 
    )
    
    return {"output": qna}
     