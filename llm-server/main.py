# this file will contain all the fastapi endpoints 

# FastAPI imports 
from fastapi import FastAPI 

from models import DataLoaderModel 
from models import GenerationContext
from models import StructuredJSONModel
from models import DataClassifierModel
from models import SummarizationInputModel
from models import SummarizationOutputModel
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
from models import ModificationInputModel 
from models import ModificationOutputModel 
from models import MetaDataEditModel 
from models import MetaDataEditResponseModel

from dotenv import load_dotenv # for the purposes of loading hidden environment variables
from typing import Dict, List 
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request 
from fastapi import HTTPException


from collections import defaultdict

import PIL 
import random 
import os 
import json
import time 
import tiktoken 
import fasttext

import pdf2image as p2i 

from openai import OpenAI 

# custom defined libraries 
from json_trees.generate import JSONParser 
from generation.generate import generate_response
from generation.prompts import (
    prompts, 
    qna_validation_prompt, 
    convert_to_html_prompt
) 

from summarizer.summarize import summarize_texts
from summarizer.prompts import summarization_prompt

from json_editor.editor import edit_metadata

from language_detection.detector import detect_language
from language_detection.prompts import text_extraction_prompt
from language_detection.format_converter import language_codes 

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
from synthesizers.prompts import strength_prompt 
from synthesizers.synthesize import synthesizer 

from segregator.segregation import segregator
from segregator.prompts import counting_prompt 
from segregator.modifier import get_relevant_count

# loads the variables in the .env file 
load_dotenv(override=True)

# environment variables: configured in .env file
# these variables will be instantiated once the server starts and 
# the value won't be updated until you restart the server 
# PROMPT_FILE_ID: str = os.getenv("FILE_ID", None) # file_id to fetch remote prompt design sheet
# GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", None) # gemini api key 
# OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", None) # openai api key 
# HF_TOKEN: str = os.getenv("HF_TOKEN", None) # Huggingface token 

question_type_map: Dict[str, str] = {
    "True/False": "trueFalse", 
    "Fill in the blanks": "fillInTheBlanks", 
    "Short Question Answer": "shortQuestionAnswer", 
    "Multiple Choice": "multipleChoice", 
    "Computational Questions": "computationQuestion", 
    "Software Code Questions": "softwareCodeQuestion", 
}


PROMPT_FILE_ID: str = os.environ.get("FILE_ID") 
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")
GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY")
HF_TOKEN: str = os.environ.get("HF_TOKEN")
BUCKET_NAME: str = os.environ.get("BUCKET_NAME")

# error directory 
ERROR_DIR: str = "error_dir"

gpt4o = OpenAI(api_key=OPENAI_API_KEY)
gpt4o_encoder = tiktoken.encoding_for_model("gpt-4o-mini")

#facebook nllb 
language_detection_model = fasttext.load_model("../bucket-gs/translation-model/model.bin")

# initalizing the bucket client  
gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

# testing phase therefore `debug=True`
app = FastAPI(debug=True, title="project-astra")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
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
async def convert_pdf(pdf_file: 
    ConvertPDFModel) -> ConvertPDFOutputModel : 
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
    try: 
        pdf_blob = bucket.blob(pdf_file.uri)
        
        with pdf_blob.open("rb") as f:   
            images: List[PIL.Image] = p2i.convert_from_bytes(
                f.read(), 
                dpi=200, 
                fmt="jpg", 
            )
        
        
    except Exception as err: 
        error_line: int = err.__traceback__.tb_lineno 
        error_name: str = type(err).__name__
        raise HTTPException(
            status_code=404, 
            detail = f"Error {error_name} at line {error_line}"
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

    try: 
        image_blob = bucket.blob(f"{lng_model.email_id}/processed_image/{lng_model.filename.split('.pdf')[0]}.json")
        with image_blob.open("r") as f: 
            images: List[Dict] = json.load(fp=f)
    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )

    if len(images) > 10:  
        chosen_images = random.sample(population=images, k=5)
    else: chosen_images = images 

    languages : List[str] = []
    for image in chosen_images: 
        encoded_image: str = image["img_b64"]
        language, token_count = detect_language(
            encoded_image, 
            language_codes, 
            messages, 
            text_extraction_prompt,
            language_detection_model,
            gpt4o_encoder, 
            gpt4o)

        languages.append(language) 
    
    duration = time.time() - start_time
    
    return DetectedLanguageModel(
        filename=lng_model.filename, 
        email_id=lng_model.email_id, 
        detected_language=max(languages, key=languages.count).lower(),
        time=duration, 
        token_count=token_count, 
    ) 

# the data loading endpoint 
@app.post("/data_loader")
async def data_loader(user_image_data: DataLoaderModel) -> StructuredJSONModel: 
    # reading the images from the bucket 
    start_time = time.time()
    try: 
        image_json_blob = bucket.blob(user_image_data.uri) 
        with image_json_blob.open("r") as img_json: 
            images: List[Dict[str, str]] = json.load(img_json)
    except Exception as err:
        error_count: int = err.__traceback__.tb_lineno
        error_name: str  = type(err).__name__
        raise HTTPException(
            status_code = 404, 
            details = f"Error: {error_name} at {error_count}"
        )

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
async def summarize(summarization: 
    SummarizationInputModel) -> SummarizationOutputModel: 

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
        blob_json_content, 
        generated_list, 
        text_message, 
        classification_prompt, 
        rewrite_target.language, 
        gpt4o, 
        gpt4o_encoder, 
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

# @app.post("/divider")
# async def json_divider(): 

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

@app.get("/reactFlow/{category}/{emailId}/{fileName}")
async def react_flow(category: str, emailId: str, fileName: str ) -> JSONResponse: 
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
        concept_tree = parser.to_tree(processed_json, category=category)
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
        json_content[content.branch_name], 
        json_content["text"],
        strength_prompt, 
        text_message, 
        gpt4o, 
        gpt4o_encoder, 
    )

    if not status: 
        score = 0
    
    json_content[f"{content.branch_name}_strength"] = score

    with intermediate_json_blob.open("w") as f: 
        json.dump(json_content, fp=f)
    
    duration = time.time() - starting_time
    
    return SynthesisContentOutputModel(
        filename=content.filename, 
        email_id=content.email_id, 
        node_id=content.node_id, 
        branch_name=content.branch_name, 
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
        json_content[content.branch_name], 
        json_content["text"],
        representation_strength_prompt, 
        text_message, 
        gpt4o, 
        gpt4o_encoder, 
    )

    if not status: 
        score = 0
    
    json_content[f"{content.branch_name}_representation_strength"] = score

    with intermediate_json_blob.open("w") as f: 
        json.dump(json_content, fp=f)
    
    duration = time.time() - starting_time
    
    return SynthesisContentOutputModel(
        filename=content.filename, 
        email_id=content.email_id, 
        node_id=content.node_id, 
        branch_name=content.branch_name, 
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
        json_content[content.branch_name], 
        json_content["text"],
        representation_depth_prompt, 
        text_message, 
        gpt4o, 
        gpt4o_encoder, 
    )

    if not status: 
        score = 0
    
    json_content[f"{content.branch_name}_representation_depth"] = score

    with intermediate_json_blob.open("w") as f: 
        json.dump(json_content, fp=f)
    
    duration = time.time() - starting_time
    
    return SynthesisContentOutputModel(
        filename=content.filename, 
        email_id=content.email_id, 
        branch_name=content.branch_name, 
        node_id=content.node_id, 
        time=duration, 
        token_count=token_count
    )



@app.post("/segregate")
async def segregate_json(uploaded_file: AbsoluteBaseModel) -> AbsoluteBaseModel: 
    final_json_blob = bucket.blob(os.path.join(
        uploaded_file.email_id, 
        "final_json", 
        f"{uploaded_file.filename}.json"
    ))

    with final_json_blob.open("r") as f: 
        final_json = json.load(fp=f)
    
    topics, concepts, headings = segregator(final_json)
    
    topic_blob = bucket.blob(os.path.join(
        uploaded_file.email_id, 
        "books", 
        uploaded_file.filename, 
        "topic.json"
    ))


    concept_blob = bucket.blob(os.path.join(
        uploaded_file.email_id, 
        "books", 
        uploaded_file.filename, 
        "concept.json"
    ))


    headings_blob = bucket.blob(os.path.join(
        uploaded_file.email_id, 
        "books", 
        uploaded_file.filename, 
        "heading_text.json"
    ))

    with topic_blob.open("w") as f: 
        json.dump(topics, fp=f)

    
    with headings_blob.open("w") as f: 
        json.dump(headings, fp=f)


    with concept_blob.open("w") as f: 
        json.dump(concepts, fp=f)
    
    return uploaded_file 

@app.post("/modify_branch") 
async def modify_branch(branch_data: ModificationInputModel) -> ModificationOutputModel: 
    start_time = time.time()
    branch_blob = bucket.blob(os.path.join(
        branch_data.email_id, 
        "books", 
        branch_data.filename, 
        f"{branch_data.branch_name}.json", 
    ))

    with branch_blob.open("r") as f:
        js_object = json.load(fp=f)
    
    branch_modified, token_count = get_relevant_count(
        js_object, [text_message[1]], 
        counting_prompt, gpt4o, gpt4o_encoder
    )

    with branch_blob.open("w") as f: 
        json.dump(branch_modified, fp=f)
    
    return ModificationOutputModel(
        filename=branch_data.filename, 
        email_id=branch_data.email_id, 
        branch_name=branch_data.branch_name, 
        time=time.time() - start_time, 
        token_count=token_count, 
    )

@app.post("/add_word_count") 
async def add_word_count(edit_metadata_request: MetaDataEditModel) -> MetaDataEditResponseModel: 
    start_time = time.time()
    final_json_blob = bucket.blob(os.path.join(
        edit_metadata_request.email_id, 
        "final_json", 
        f"{edit_metadata_request.filename}.json", 
    ))

    with final_json_blob.open("r") as f:
        final_json = json.load(fp=f)
    
    concept_blob = bucket.blob(os.path.join(
        edit_metadata_request.email_id, 
        "books", 
        edit_metadata_request.filename, 
        "concept.json"
    ))

    topic_blob = bucket.blob(os.path.join(
        edit_metadata_request.email_id, 
        "books", 
        edit_metadata_request.filename, 
        "topic.json"
    ))

    heading_text_blob = bucket.blob(os.path.join(
        edit_metadata_request.email_id, 
        "books", 
        edit_metadata_request.filename, 
        "heading_text.json"
    ))

    with concept_blob.open("r") as f: 
        concept_json = json.load(fp=f) 

    with topic_blob.open("r") as f: 
        topic_json = json.load(fp=f) 

    with heading_text_blob.open("r") as f: 
        heading_json = json.load(fp=f)
        
    metadata_edited_final: List = edit_metadata(final_json, heading_json, concept_json, topic_json)
    with final_json_blob.open("w") as f: 
        json.dump(metadata_edited_final, fp=f)
    
    return MetaDataEditResponseModel(
        filename=edit_metadata_request.filename, 
        email_id=edit_metadata_request.email_id, 
        time=time.time() - start_time, 
    )

@app.post("/generation_data")
async def generation_data(request: Request) -> JSONResponse: 
    data = await request.json() 
    emailId = data["emailId"]
    fileName = data["fileName"]
    category = data["category"] if data["category"] != "heading" else "heading_text"
    print(category)

    degree_weights: Dict = {
       5: 1, 
       4: 0.8, 
       3: 0.6, 
       2: 0.4, 
       1: 0.2,  
    }
    
    assign_value_weights : Dict = {
        1: 1, 
        2: 0.5, 
        3: 0.25, 
    }

    depth_value_weights: Dict = degree_weights.copy()

    preference_weights = {
        "High": 1, 
        "Medium": 0.5, 
        "Low": 0.25, 
        "Ignore": 0, 
    }

    generation_config: Dict = data["generationData"]
    
    qna_book_level_data = generation_config["book"][0]["nodeContent"]

    mi = defaultdict(lambda: defaultdict(int))
    for question_type, question_count in qna_book_level_data.items():
        for chapter_node in generation_config["chapters"]:
            mi[question_type][chapter_node["nodeName"]]= int((chapter_node["nodeContent"]["gliderValue"]  / 100) * question_count)

    ms = defaultdict(lambda: defaultdict(list))
    mj = defaultdict(lambda: defaultdict(str))
    for topic_node in generation_config["topics"]:
        question_type_key = question_type_map[topic_node["nodeContent"]["questionType"]]
        mj[question_type_key][topic_node["chapterName"]] = {
            "topic": topic_node["nodeName"],
            "preferenceLevel": topic_node["nodeContent"]["preferenceLevel"]
        }
        
        ms[question_type_key][topic_node["chapterName"]].append({
            "topic": topic_node["nodeName"],
            "preferenceLevel": topic_node["nodeContent"]["preferenceLevel"]
        })

    mk = defaultdict(lambda: defaultdict(int))
    for question_type, question_count in qna_book_level_data.items():
        weights = 0

        for chapter_name in mj[question_type]:
            weights += mi[question_type][chapter_name]

        for chapter_name in mj[question_type]:
            if weights != 0: 
                mk[question_type][chapter_name] = int((mi[question_type][chapter_name] / weights) * question_count)

    # now getting the topic weights 
    preference_weights = {
        "High": 1, 
        "Medium": 0.5, 
        "Low": 0.25, 
        "Ignore": 0, 
    }

    question_distribution: Dict = defaultdict(
        lambda : defaultdict(
            lambda : defaultdict(int)
        )
    ) 

    for question_type, associated_chapters in mk.items(): 

        for chapter_name, chapter_question_count in associated_chapters.items(): 
            net_weights = 0  
            
            for topic_data in ms[question_type][chapter_name]:
                net_weights += preference_weights[topic_data["preferenceLevel"]]

            for topic_node in ms[question_type][chapter_name]:
                question_distribution[question_type][chapter_name][topic_node['topic']] = int(round(
                    chapter_question_count * 
                    (preference_weights[topic_node["preferenceLevel"]] / net_weights) 
                , 0))

    modified_final_json : List = []

    try: 
        final_json_blob = bucket.blob(os.path.join(
            emailId, 
            "final_json", 
            f"{fileName}.json", 
        ))

        with final_json_blob.open("r") as f: 
            final_json = json.load(fp=f)
        
        didnt_enter_count = 0  
        for _, js_object in enumerate(final_json) :
            if ("topic_strength" in js_object 
                and "topic_representation_depth" in js_object 
                and "topic_representation_strength" in js_object): 

                # print(degree_weights[js_object["topic_strength"]])
                # print(depth_value_weights[js_object["topic_representation_depth"]])
                # print(js_object["topic_representation_strength"])
                # print(json.dumps(assign_value_weights, indent=4))

                js_object["cumulative_strength"] = (degree_weights[js_object["topic_strength"]] + 
                                depth_value_weights[js_object["topic_representation_depth"]] +
                                assign_value_weights[js_object["topic_representation_strength"]]) 

                modified_final_json.append(js_object)
            else: 
                js_object["cumulative_strength"] = 0
                didnt_enter_count += 1
                # print(json.dumps(js_object, indent=4))
            
        print("Error count ", didnt_enter_count) 
        print("Net length ", len(final_json)) 
        # modified_final_json = sorted(modified_final_json, key = lambda x: x["cumulative_strength"], reverse=True)
        
        # with final_json_blob.open("w") as f: 
        #     json.dump(modified_final_json, fp=f)

    except Exception as err: 
        print("Error occured!")
        print("error: %s at line %s" % (type(err).__name__, err.__traceback__.tb_lineno))
    
    question_list: Dict = defaultdict(
        lambda : defaultdict(
            lambda : defaultdict(lambda : {
                "topic_question_count": 0, 
                "topic_json": [] 
            })
        )
    ) 

    if modified_final_json:
        for question_type, chapter_map in question_distribution.items(): 
            for chapter_name, topic_nodes in chapter_map.items(): 
                for topic_name, question_count in topic_nodes.items(): 
                    question_list[question_type][chapter_name][topic_name]["topic_question_count"] = question_count
                    question_list[question_type][chapter_name][topic_name]["topic_json"] = (
                        sorted(list(filter(lambda mp: mp["topic"] == topic_name, modified_final_json)),
                        key = lambda x: x["cumulative_strength"], reverse=True) 
                    )       

        
        qd_dict = {} 
        for key, value in dict(question_list).items():
            qd_dict[key] = dict(value)
            for k, v in value.items():
                qd_dict[key][k] = dict(v)
         
        try: 
            generation_data_blob = bucket.blob(os.path.join(
                emailId, 
                "generation_data", 
                f"{fileName}.json", 
            ))

            with generation_data_blob.open("w") as f: 
                json.dump(qd_dict, fp=f)

        except Exception as err: 
            print("No such object found")
            print("error: %s at line %s" % (type(err).__name__, err.__traceback__.tb_lineno))

    else: 
        print("The list was empty ")

    return {"email_id": emailId, "filename": fileName, "computed_question_data": mk} 


@app.post("/generate")
async def generate(context: GenerationContext) -> Dict[str, str | int| float]:
    start_time: float = time.time()

    try: 
        generation_metadata_blob = bucket.blob(os.path.join(
            context.email_id, 
            "generation_data", 
            f"{context.filename}.json", 
        ))
    except Exception as e: 
        print(f"The file {context.filename} has not been processed")
        print(e)

    with generation_metadata_blob.open("r") as f: 
        generation_data = json.load(fp=f)

    associated_json: Dict = generation_data[context.question_type][context.chapter_name][context.topic_name]
    question_count = associated_json["topic_question_count"] 
    text = ""

    for paragraph_node in associated_json["topic_json"]: 
        text += paragraph_node["text"]

    qna_prompt: str = prompts[context.question_type]

    qna, token_count = generate_response(
        messages=text_message, 
        prompt=qna_prompt, 
        validation_prompt=qna_validation_prompt, 
        convert_to_html_prompt=convert_to_html_prompt, 
        context=text,  
        question_count=question_count, 
        language=context.language, 
        gpt4o_encoder=gpt4o_encoder, 
        gpt4o=gpt4o, 
    )

    # dump the output to gcp 
    try: 
        generated_dump_blob = bucket.blob(os.path.join(
            context.email_id, 
            "generated_content", 
            context.filename, 
            f"{context.question_type}_{context.chapter_name}_{context.topic_name}.html", 
        ))

        with generated_dump_blob.open("w") as f: 
            f.write(qna)

    except Exception as err: 
        print(err)
    
    return {"output": qna, "time": time.time() - start_time, "token_count": token_count}
     
@app.get("/generation_output/{email_id}/{filename}/{question_type}/{chapter_name}/{topic_name}")
async def generated_output(email_id: str, filename: str, question_type: str, chapter_name: str, topic_name: str) -> HTMLResponse:  
    chapter_name = chapter_name.replace("_", " ")
    topic_name = topic_name.replace("_", " ")
    topic_name = topic_name if topic_name.endswith(".html") else f"{topic_name}.html"

    try: 
        html_blob = bucket.blob(os.path.join(
            email_id, 
            "generated_content", 
            filename, 
            f"{question_type}_{chapter_name}_{topic_name}"
        ))

        with html_blob.open("r") as f: 
            html_qna : str = f.read()
        
        return HTMLResponse(content = html_qna)

    except Exception as e: 
        print(e)
        return HTMLResponse(
            content = "<h1> No such file exists! Go back and select question types </h1>", 
            status_code=404, 
        )
