# this file will contain all the fastapi endpoints 

# FastAPI imports 
from fastapi import FastAPI 
from fastapi import UploadFile 
from fastapi import HTTPException 
from models import GenerationContext
from models import EncodedImages

from dotenv import load_dotenv # for the purposes of loading hidden environment variables
from typing import Dict, List 

import tempfile 
import PIL 
import os 
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
async def convert_pdf(pdf_file: UploadFile) -> EncodedImages: 
    if pdf_file.content_type != "application/pdf": 
        raise HTTPException(status_code=400, detail="Please upload a pdf file!")

    with tempfile.TemporaryDirectory() as temp_dir: 

        temp_path: str = os.path.join(temp_dir, pdf_file.filename)
        with open(temp_path, "wb") as f: 
            # storing the pdf in a temporary file 
            f.write(await pdf_file.read())
        
        images: List[PIL.Image] = p2i.convert_from_path(
            temp_path, 
            dpi=200, 
            fmt="jpg", 
        )
    
    images = [encode_image(img) for img in images]
    return EncodedImages(images=images) 
        

# the data loading endpoint 
@app.post("/data_loader")
async def data_loader(encoded_images: EncodedImages) -> List[Dict[str, str| int| None]]: 
    # sending images to the images function 
    html_pages: List[str] = parse_images(
        models=[gemini, gpt4o], 
        config=config, 
        images=encoded_images.images, 
        prompt=prompt, 
        clause_prompt=clause_prompt, 
        messages=messages,  
    )

    strucuted_json: List[Dict[str, str|int]] = structure_html(html_pages) 
    return strucuted_json    

# data classifier endpoint  
@app.post("/data_classifier")
async def data_classifier(text_json: List[Dict[str, str|int|None]]
                          ) -> List[Dict[str, Dict|str|None|int|List[str]] | str]: 
    
    output_json: List = []
    for t_json in text_json: 
        op: Dict[str, Dict|str|None|int|List[str]]|str = get_json(t_json, HF_TOKEN) 
        # if llm output is not faulty 
        if op != "": 
            output_json.append(op)

    return output_json

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
     