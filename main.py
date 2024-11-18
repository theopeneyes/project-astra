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
from models import ConvertPDFModel
from models import ConvertPDFOutputModel
from models import SummaryChapterOutputModel
from models import RewriteJSONFileOutputModel 
from models import PushToJSONModel
from models import SynthesisContentInputModel 
from models import SynthesisContentOutputModel 

from dotenv import load_dotenv # for the purposes of loading hidden environment variables
from typing import Dict, List 
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from transformers import AutoTokenizer

import PIL 
import random 
import os 
import json
import time 
import tiktoken 

import pdf2image as p2i 
import numpy as np 
import datamapplot
import tempfile 

from google import generativeai as genai
from openai import OpenAI 

# custom defined libraries 
from json_trees.generate import JSONParser 
from generation.generate import generate_response
from generation.prompts import prompts, qna_validation_prompt

from summarizer.summarize import summarize_texts
from summarizer.prompts import summarization_prompt

from language_detection.detector import detect_language
from language_detection.prompts import language_detection_prompt

from data_loader.image_parser import parse_images 
from data_loader.structure import structure_html 
from data_loader.prompts import generation_prompt, clause_prompt, validation_prompt 
from data_loader.opeanai_formatters import image_message as messages, text_message  

from data_classifier.classification_pipeline import get_json
from google.cloud import storage 
from image_utils.encoder import encode_image 

from metadata_producers.generate_list import generateList
from metadata_producers.prompts import about_list_generation_prompt, depth_list_generation_prompt
from metadata_producers.append_about_data import classify_about
from metadata_producers.prompts import classification_prompt

from synthesizers.prompts import representation_depth_prompt
from synthesizers.prompts import representation_strength_prompt 
from synthesizers.prompts import topic_strength_prompt 
from synthesizers.synthesize import synthesizer 

# loads the variables in the .env file 
load_dotenv(override=True)

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
GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY")
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

gpt4o = OpenAI(api_key=OPENAI_API_KEY)
gpt4o_encoder = tiktoken.encoding_for_model("gpt-4o-mini")
phi_encoder = AutoTokenizer.from_pretrained("microsoft/Phi-3.5-mini-instruct")

# initalizing the bucket client  
gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

# testing phase therefore `debug=True`
app = FastAPI(debug=True, title="project-astra")

origins = [
    "http://localhost:5174",  
    "http://localhost:5173", 
    "http://127.0.0.1:5173", 
    "http://127.0.0.1:5174", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],              
)
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


# No LLM is used in this step. SO we are not charging tokens. 
# we are however computing the amount of time this endpoint takes to run 
@app.post("/convert_pdf")
async def convert_pdf(pdf_file: ConvertPDFModel) -> ConvertPDFOutputModel: 
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
    start_time = time.time()
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
    
    duration = time.time() - start_time

    return ConvertPDFOutputModel(
        filename=pdf_file.filename, 
        email_id=pdf_file.email_id, 
        uri=json_path, 
        time=duration,  
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
    
    start_time = time.time()  
    image_blob = bucket.blob(f"{lng_model.email_id}/processed_image/{lng_model.filename.split('.pdf')[0]}.json")
    with image_blob.open("r") as f: 
        images: List[Dict] = json.load(fp=f)

    if len(images) > 5:  
        chosen_images = random.sample(population=images, k=5)
    else: chosen_images = images 

    languages : List[str] = []
    for image in chosen_images: 
        encoded_image: str = image["img_b64"]
        language, token_count = detect_language(
            encoded_image, 
            messages, 
            language_detection_prompt,
            gpt4o_encoder, 
            gpt4o)

        languages.append(language) 
    
    duration = time.time() - start_time
    
    return DetectedLanguageModel(
        filename=lng_model.filename, 
        email_id=lng_model.email_id, 
        detected_language=max(languages, key=languages.count),
        time=duration, 
        token_count=token_count, 
    ) 

# the data loading endpoint 
@app.post("/data_loader")
async def data_loader(user_image_data: DataLoaderModel) -> StructuredJSONModel: 
    # reading the images from the bucket 
    start_time = time.time()
    image_json_blob = bucket.blob(user_image_data.uri) 
    with image_json_blob.open("r") as img_json: 
        images: List[Dict[str, str]] = json.load(img_json)

    print(f"processing step here for pdf {user_image_data.filename}...")
    # sending images to the images function 
    html_pages, token_count = parse_images(
        gpt4o, 
        images=images, 
        prompt=generation_prompt, 
        clause_prompt=clause_prompt, 
        validation_prompt=validation_prompt, 
        messages=messages,  
        text_messages=text_message, 
        gpt4o_encoder=gpt4o_encoder, 
        language=user_image_data.language, 
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
    
    duration = time.time() - start_time
    
    return StructuredJSONModel(
        email_id=user_image_data.email_id, 
        filename=user_image_data.filename, 
        page_count=len(structured_json), 
        time=duration, 
        token_count=token_count, 
    ) 


# segerates via chapter and summarizes the chapter  
@app.post("/summarize")
async def summarize(summarization: SummarizationInputModel) -> SummarizationOutputModel: 
    start_time = time.time()
    chapter_path : str =  f"{summarization.email_id}/summaries/{summarization.filename}"
    chapter_name: str = summarization.chapter_title.split("_content")[0]
    chapter_blob = bucket.blob(f"{chapter_path}/{summarization.chapter_title}_content.txt") 
    summary_blob = bucket.blob(f"{chapter_path}/{chapter_name}_summary.txt")
    with chapter_blob.open("r") as f: 
        content = f.read()
    
    if content:  
        status, summary, token_count = summarize_texts(
            content, 
            summarization.language, 
            summarization_prompt, 
            text_message, gpt4o_encoder, gpt4o)

        if status: 
            with summary_blob.open("w") as f: 
                f.write(summary)
        else: 
            print("Empty summary here. Bad summarization output from llm")
            print(summary)
    else: 
        print(f"Empty text in chapter identified! content: {content}")

    duration = time.time() - start_time 
    return SummarizationOutputModel(
        filename=summarization.filename, 
        email_id=summarization.email_id, 
        time=duration, 
        token_count=token_count, 
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
        classified_blob_path: str = f"{text_json.email_id}/final_json/{text_json.filename}_{text_json.page_number}.json" 
        cls_blob = bucket.blob(classified_blob_path)
        with cls_blob.open("w") as f:
            json.dump(op, fp=f)
       
    return text_json

@app.post("/summary_classifier")
async def classify_summary(summ_input: SummaryChapterModel) -> SummaryChapterOutputModel: 
    start_time = time.time()
    summary_path: str = f"{summ_input.email_id}/summaries/{summ_input.filename}/{summ_input.chapter_name}_summary.txt"
    summary_blob = bucket.blob(summary_path)
    with summary_blob.open("r") as f: 
        summary_content: str = f.read()
    
    content, token_count = generateList(summary_content, 
                           about_list_generation_prompt, 
                           depth_list_generation_prompt, 
                           summ_input.language, 
                           text_message, 
                           gpt4o_encoder, 
                           gpt4o)

    classified_summary_path: str = f"{summ_input.email_id}/summaries/{summ_input.filename}/{summ_input.chapter_name}_classified_summary.json"
    classified_summary_blob = bucket.blob(classified_summary_path)
    with classified_summary_blob.open("w") as f: 
        f.write(json.dumps(content))
    
    duration = float(time.time() - start_time) 

    return SummaryChapterOutputModel(
        filename=summ_input.filename, 
        email_id=summ_input.email_id, 
        chapter_name=summ_input.chapter_name, 
        language=summ_input.language, 
        time=duration, 
        token_count = token_count
    ) 

# always executed after the summary has been classified 
# the input is a rewrite_target which is a paragraph node to be rewritten with more attributes  
@app.post("/rewrite_json")
async def rewrite_json(rewrite_target: RewriteJSONFileModel) -> RewriteJSONFileOutputModel: 
    start_time = time.time()
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
    comprehensive_node, token_count = classify_about(
        HF_TOKEN, 
        blob_json_content, 
        generated_list, 
        classification_prompt, 
        rewrite_target.language, 
        phi_encoder,  
    )

    # write this onto intermediate_json directory 
    intermediate_json_blob = bucket.blob(os.path.join(
        rewrite_target.email_id, 
        "intermediate_json", 
        f"{rewrite_target.filename}_{rewrite_target.node_id}.json"
    ))

    with intermediate_json_blob.open("w") as f: 
        json.dump(comprehensive_node, fp = f) 
    
    duration = time.time() - start_time
    # process complete 
    return RewriteJSONFileOutputModel(
        filename=rewrite_target.filename, 
        email_id=rewrite_target.email_id, 
        node_id=rewrite_target.node_id, 
        language=rewrite_target.language, 
        time=duration, 
        token_count=token_count, 
    )

@app.post("/preprocess_for_graph")
async def push_to_json(base_model: AbsoluteBaseModel) -> PushToJSONModel: 
    start_time: float = time.time()
    blobs = gcs_client.list_blobs(
        BUCKET_NAME, 
        prefix=os.path.join(
            base_model.email_id, 
            "intermediate_json/", 
        ), 
        delimiter="/"
    )

    json_blob = bucket.blob(os.path.join(
        base_model.email_id, 
        "final_json", 
        f"{base_model.filename}.json", 
    ))

    all_jsons: List = []
    for blob in blobs: 
        if base_model.filename in blob.name: 
            with blob.open("r") as jason: 
                all_jsons.append(json.load(fp=jason)) 
    
    with json_blob.open("w") as all_in_one: 
        json.dump(all_jsons, fp=all_in_one)
    
    return PushToJSONModel(
        filename=base_model.filename, 
        email_id=base_model.email_id, 
        time=time.time() - start_time
    ) 

@app.post("/create_img")
async def create_image(img_model: DataMapPlotInputModel) -> GeneratedImageModel: 
    start_time: float = time.time()
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
            encoded_image=encode_image(matplotlib_fig), 
            time=time.time() - start_time
        )

@app.get("/interactive_plot/{email_id}/{filename}")
async def interactive_plot(email_id: str, filename: str) -> HTMLResponse:
    blob_path: str = f"{email_id}/rendered_html/{filename}.html"  
    blob = bucket.blob(blob_path)
    with blob.open("r") as html: 
        content = html.read()
    with blob.open("r") as html: 
        content = html.read()

    return HTMLResponse(
        content = content 
    ) 

@app.get("/reactFlow/{emailId}/{fileName}")
async def react_flow(emailId: str, fileName: str ) -> JSONResponse: 
    try: 
        processed_json_blob = bucket.blob(os.path.join(
            emailId, 
            "final_json", 
            f"{fileName}.json", 
        ))
        
    except Exception as _: 
        print("Exception occured")
        print("The blob does not exist")
        print(_)

    with processed_json_blob.open("r") as processed_json_fp: 
        processed_json = json.load(fp=processed_json_fp) 

        parser = JSONParser(book_name=fileName) 
        concept_tree = parser.to_tree(processed_json)
        nodes, edges = parser.parse_tree(concept_tree)

    return JSONResponse(content = [nodes, edges])  

@app.post("/synthesize/strength/relational")
async def synthesize_relative_strength(content: SynthesisContentInputModel) -> SynthesisContentOutputModel: 
    starting_time: float = time.time()
    intermediate_json_blob = bucket.blob(os.path.join(
        content.email_id, 
        "intermediate_json", 
        f"{content.filename}_{content.node_id}.json"
    ))

    with intermediate_json_blob.open("r") as f: 
        json_content = json.load(fp=f)

    status, score, token_count = synthesizer(
        json_content["topic"], 
        json_content["text"],
        topic_strength_prompt, 
        text_message, 
        gpt4o, 
        gpt4o_encoder, 
    )

    if not status: 
        score = 0
    
    json_content["topic_strength"] = score

    with intermediate_json_blob.open("w") as f: 
        json.dump(json_content, fp=f)
    
    duration = time.time() - starting_time
    
    return SynthesisContentOutputModel(
        filename=content.filename, 
        email_id=content.email_id, 
        node_id=content.node_id, 
        time=duration, 
        token_count=token_count
    )


@app.post("/synthesize/strength/representational")
async def synthesize_relative_strength(content: SynthesisContentInputModel) -> SynthesisContentOutputModel: 
    starting_time: float = time.time()
    intermediate_json_blob = bucket.blob(os.path.join(
        content.email_id, 
        "intermediate_json", 
        f"{content.filename}_{content.node_id}.json"
    ))

    with intermediate_json_blob.open("r") as f: 
        json_content = json.load(fp=f)

    status, score, token_count = synthesizer(
        json_content["topic"], 
        json_content["text"],
        representation_strength_prompt, 
        text_message, 
        gpt4o, 
        gpt4o_encoder, 
    )

    if not status: 
        score = 0
    
    json_content["representation_strength"] = score

    with intermediate_json_blob.open("w") as f: 
        json.dump(json_content, fp=f)
    
    duration = time.time() - starting_time
    
    return SynthesisContentOutputModel(
        filename=content.filename, 
        email_id=content.email_id, 
        node_id=content.node_id, 
        time=duration, 
        token_count=token_count
    )


@app.post("/synthesize/depth/representational")
async def synthesize_relative_strength(content: SynthesisContentInputModel) -> SynthesisContentOutputModel: 
    starting_time: float = time.time()
    intermediate_json_blob = bucket.blob(os.path.join(
        content.email_id, 
        "intermediate_json", 
        f"{content.filename}_{content.node_id}.json"
    ))

    with intermediate_json_blob.open("r") as f: 
        json_content = json.load(fp=f)

    status, score, token_count = synthesizer(
        json_content["topic"], 
        json_content["text"],
        representation_depth_prompt, 
        text_message, 
        gpt4o, 
        gpt4o_encoder, 
    )

    if not status: 
        score = 0
    
    json_content["representation_depth"] = score

    with intermediate_json_blob.open("w") as f: 
        json.dump(json_content, fp=f)
    
    duration = time.time() - starting_time
    
    return SynthesisContentOutputModel(
        filename=content.filename, 
        email_id=content.email_id, 
        node_id=content.node_id, 
        time=duration, 
        token_count=token_count
    )


@app.post("/generate")
async def generate(context: GenerationContext) -> Dict[str, str | int| float]:
    start_time: float = time.time()
    qna_prompt: str = prompts[context.question_type]
    qna, token_count = generate_response(
        messages=text_message, 
        prompt=qna_prompt, 
        validation_prompt=qna_validation_prompt, 
        context=context.context, 
        topics=context.topics, 
        language=context.language, 
        gpt4o_encoder=gpt4o_encoder, 
        gpt4o=gpt4o, 
    )
    
    return {"output": qna, "time": time.time() - start_time, "token_count": token_count}
     
