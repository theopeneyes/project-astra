# this file will contain all the fastapi endpoints 

# FastAPI imports 
from fastapi import FastAPI 

from models import DataLoaderModel 
from models import GenerationContext
from models import StructuredJSONModel
from models import DataClassifierModel
from models import SummarizationInputModel
from models import SummarizationOutputModel
from models import GeneratedImageModel 
from models import DataMapPlotInputModel 
from models import DetectedLanguageModel
from models import AbsoluteBaseModel
from models import RewriteJSONFileModel
from models import SummaryChapterModel

from dotenv import load_dotenv # for the purposes of loading hidden environment variables
from typing import Dict, List 
from fastapi.responses import HTMLResponse

import PIL 
import random 
import os 
import json
import logging  
import pdf2image as p2i 
import numpy as np 
import datamapplot
import tempfile 

from google import generativeai as genai
from openai import OpenAI 

# generation model 
from generation.generate import generate_response
from generation.prompts import prompts 

from summarizer.summarize import summarize_texts

from language_detection.detector import detect_language
from language_detection.prompts import language_detection_prompt

from data_loader.image_parser import parse_images 
from data_loader.structure import structure_html 
from data_loader.prompts import prompt, clause_prompt 
from data_loader.opeanai_formatters import messages 

from data_classifier.classification_pipeline import get_json
from google.cloud import storage 
from image_utils.encoder import encode_image 

from metadata_producers.generate_list import generateList
from metadata_producers.prompts import about_list_generation_prompt, depth_list_generation_prompt

from metadata_producers.append_about_data import classify_about
from metadata_producers.prompts import classification_prompt

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

# # login trigger 
# @app.post("/trigger")
# async def login_trigger()


@app.post("/convert_pdf")
async def convert_pdf(pdf_file: DataLoaderModel) -> DataLoaderModel: 
    """
    Input: {
        filename: name of the book 
        email_id: email id of the user used as a unique identified 
        uri: uri of the located file within uploaded_document
    }

    Function: 
    Disintegrates the pdf into a set of images to be stored within processed_image directory  
    """
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
        

@app.post("/detect_lang") 
async def detect_lang(lng_model: AbsoluteBaseModel) -> DetectedLanguageModel: 
    """
    Input: {
        filename: Name of the file to detect the language of 
        email_id: Email id of the user 
    }

    Function: 
    Detects the language of the pdf by sampling a few pages from within it. 
    """

    image_blob = bucket.blob(f"{lng_model.email_id}/processed_image/{lng_model.filename.split('.pdf')[0]}.json")
    with image_blob.open("r") as f: 
        images: List[Dict] = json.load(fp=f)

    if len(images) > 5:  
        chosen_images = random.sample(population=images, k=5)
    else: chosen_images = images 

    languages : List[str] = []
    for image in chosen_images: 
        encoded_image: str = image["img_b64"]
        languages.append(detect_language(encoded_image,  messages, language_detection_prompt, gpt4o)) 
    
    return DetectedLanguageModel(
        filename=lng_model.filename, 
        email_id=lng_model.email_id, 
        detected_language=max(languages, key=languages.count)
    ) 

# the data loading endpoint 
@app.post("/data_loader")
async def data_loader(user_image_data: DataLoaderModel) -> StructuredJSONModel: 
    # reading the images from the bucket 
    image_json_blob = bucket.blob(user_image_data.uri) 
    with image_json_blob.open("r") as img_json: 
        images: List[Dict[str, str]] = json.load(img_json)

    print(f"processing step here for pdf {user_image_data.filename}...")
    # sending images to the images function 
    html_pages: List[str] = parse_images(
        models=[gemini, gpt4o], 
        config=config, 
        images=images, 
        prompt=prompt, 
        clause_prompt=clause_prompt, 
        messages=messages,  
    )

    print(f"processing step is done for filename {user_image_data.filename}...")

    structured_json: List[Dict[str, str|int]] = structure_html(html_pages) 
    # writing data from each page into a json file to paralellize the rest of the code from out here 
    title: str | None = None 
    chapter_texts : List[str] = []

    # creating a folder with the name of the pdf file in the summaries directory  
    (bucket
        .blob(f'{user_image_data.email_id}/summaries/{user_image_data.filename}/')
        .upload_from_string(''))

    for idx, json_page in enumerate(structured_json):
        blob_path: str = f"{user_image_data.email_id}/text_extract/{user_image_data.filename}_{idx}.json"
        # if title is None or if it is unequal to json_page != title  
        if title and title != json_page["heading_identifier"]: 

            content_blob = (bucket
                            .blob(
                f"{user_image_data.email_id}/summaries/{user_image_data.filename}/{title}_content.txt")
            )

            with content_blob.open("w") as f:
                f.write(" ".join(chapter_texts).strip())

            chapter_texts.clear()

        title = json_page["heading_identifier"]

        json_blob = bucket.blob(blob_path)
        with json_blob.open("w") as f:
            json.dump(json_page, fp=f)
            chapter_texts.append(json_page["text"])
    
    if chapter_texts: 
        content_blob = (bucket
                        .blob(
            f"{user_image_data.email_id}/summaries/{user_image_data.filename}/{title}_content.txt")
        )

        with content_blob.open("w") as f:
            f.write(" ".join(chapter_texts).strip())

        chapter_texts.clear()
    
            
    return StructuredJSONModel(
        email_id=user_image_data.email_id, 
        filename=user_image_data.filename, 
        page_count=len(structured_json), 
    ) 


# segerates via chapter and summarizes the chapter  
@app.post("/summarize")
async def summarize(summarization: SummarizationInputModel) -> SummarizationOutputModel: 
    chapter_path : str =  f"{summarization.email_id}/summaries/{summarization.filename}"
    chapter_name: str = summarization.chapter_title.split("_content")[0]
    chapter_blob = bucket.blob(f"{chapter_path}/{summarization.chapter_title}") 
    summary_blob = bucket.blob(f"{chapter_path}/{chapter_name}_summary.txt")
    with chapter_blob.open("r") as f: 
        content = f.read()
    
    if content:  
        summary: str = summarize_texts(content, HF_TOKEN)
        with summary_blob.open("w") as f: 
            f.write(summary)
    else: 
        logging.info("Empty text in chapter identified! content: {content}")

    return SummarizationOutputModel(
        filename=summarization.filename, 
        email_id=summarization.email_id, 
        status=True
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

@app.post("/create_img")
async def create_image(img_model: DataMapPlotInputModel) -> GeneratedImageModel: 
    with tempfile.TemporaryDirectory() as tmp_dir: 
        data = np.hstack((np.array(img_model.X_col).reshape(-1, 1), 
                   np.array(img_model.Y_col).reshape(-1, 1)))  

        # scaling the data 
        data = data * 50 
        labels = np.array(img_model.labels).reshape(-1,)

        fig, _ = datamapplot.create_plot(
            data, labels, 
            noise_label="Unimportant topics", 
            title="Topic Map", 
            sub_title="Visual representation of topics found within the book", 
            label_font_size=11, 
        )

        fig.savefig(f"{tmp_dir}/saved_img.jpg")
        matplotlib_fig = PIL.Image.open(f"{tmp_dir}/saved_img.jpg") 

        return GeneratedImageModel(
            encoded_image=encode_image(matplotlib_fig)
        )

@app.get("/interactive_plot/{email_id}/{filename}")
async def interactive_plot(email_id: str, filename: str) -> HTMLResponse:
    blob_path: str = f"{email_id}/rendered_html/{filename}.html"  
    blob = bucket.blob(blob_path)
    with blob.open("r") as html: 
        content = html.read()

    return HTMLResponse(
        content = content 
    ) 

@app.post("/summary_classifier")
async def classify_summary(summ_input: SummaryChapterModel) -> SummaryChapterModel: 
    summary_path: str = f"{summ_input.email_id}/summaries/{summ_input.filename}/{summ_input.chapter_name}_summary.txt"
    summary_blob = bucket.blob(summary_path)
    with summary_blob.open("r") as f: 
        summary_content: str = f.read()
    
    content = generateList(summary_content, 
                           about_list_generation_prompt, 
                           depth_list_generation_prompt, 
                           HF_TOKEN)

    classified_summary_path: str = f"{summ_input.email_id}/summaries/{summ_input.filename}/{summ_input.chapter_name}_classified_summary.json"
    classified_summary_blob = bucket.blob(classified_summary_path)
    with classified_summary_blob.open("w") as f: 
        f.write(json.dumps(content))

    return SummaryChapterModel(
        filename=summ_input.filename, 
        email_id=summ_input.email_id, 
        chapter_name=summ_input.chapter_name, 
    ) 

# always executed after the summary has been classified 
# the input is a rewrite_target which is a paragraph node to be rewritten with more attributes  
@app.get("/rewrite_json")
async def rewrite_json(rewrite_target: RewriteJSONFileModel) -> RewriteJSONFileModel: 
    # picking the relevant book 
    blob = bucket.blob(os.path.join(
        rewrite_target.email_id, 
        "text_extract", 
        f"{rewrite_target.filename}_{rewrite_target.node_id}.json"
    ))
    
    # after reading this json content you process it with the metadata_generators
    with blob.open("r") as f:  
        blob_json_content = json.load(fp=f)

    # open the classified summary blob from the summaries section 
    classified_summary_blob = bucket.blob(os.path.join(
        rewrite_target.email_id, 
        "summaries", 
        rewrite_target.filename, 
        f"{blob_json_content['heading_identifier']}_classified_summary.json"
    )) 

    with classified_summary_blob.open("r") as f:   
        generated_list = json.load(fp=f)

    # classify the prompt 
    comprehensive_node = classify_about(
        HF_TOKEN, 
        blob_json_content, 
        generated_list, 
        classification_prompt
    )

    # write this onto intermediate_json directory 
    intermediate_json_blob = bucket.blob(os.path.join(
        rewrite_target.email_id, 
        "intermediate_json", 
        f"{rewrite_target.filename}_{rewrite_target.node_id}.json"
    ))

    with intermediate_json_blob.open("w") as f: 
        json.dump(comprehensive_node, fp = f) 
    
    # process complete 
    return rewrite_target

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
     