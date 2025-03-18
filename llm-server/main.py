# this file will contain all the fastapi endpoints 

# FastAPI imports 
from fastapi import FastAPI 
from fastapi import Form 
from fastapi import UploadFile
from fastapi import File 

from models import RunSubprocessRequest 
from models import QNATopicWiseRequest 
from models import EmailRequest
from models import FinalBookListRequest
from models import FinalBookListResponse
from models import SubprocessInitiatedResponse
from models import PdfPageCountRequestModel
from models import PdfPageCountResponseModel
from models import RectificationRequestModel
from models import RectificationResponseModel
from models import TextNodeRequestModel
from models import TextNodeResponseModel
from models import JSONEditorRequestModel
from models import JSONEditorResponseModel
from models import StatusRequestModel
from models import FontForChapterDetectionRequestModel
from models import FontForChapterDetectionResponseModel
from models import ChapterLoaderRequestModel
from models import ChapterLoaderResponseModel
from models import GenerationContext
from models import SummarizationRequestModel 
from models import SummarizationResponseModel 
from models import DetectedLanguageResponseModel
from models import RequestModel 
from models import RewriteJSONRequestModel
from models import SummaryChapterRequestModel
from models import ConvertPDFModel
from models import ConvertPDFOutputModel
from models import SummaryChapterRequestModel
from models import SummaryChapterResponseModel
from models import RewriteJSONResponseModel 
from models import SynthesisContentRequestModel 
from models import SynthesisContentResponseModel
from models import PushToJsonResponseModel 
from models import ModificationInputModel 
from models import ModificationOutputModel 
from models import MetaDataEditModel 
from models import MetaDataEditResponseModel
from models import ContentsRequestModel
from models import ContentsResponseModel
from models import ChapterIdentificationRequestModel
from models import ChapterIdentificationResponseModel
from models import ReformRequestModel
from models import ReformResponseModel
from models import PDFUploadResponseModel
from models import ResponseModel

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
import logging 
import json
import time 
import tiktoken 
import urllib.error
import requests 
import datetime 
import pymupdf
import tempfile
import subprocess 

import pdf2image as p2i 
import asyncio 
import pandas as pd 
from openai import OpenAI 
from generate_qna.generator import generate_qna_for_topic

# custom defined libraries 
from json_trees.generate import JSONParser 
from generation.generate import generate_response
from generation.prompts import (
    prompts, 
    qna_validation_prompt, 
    convert_to_html_prompt
) 

from summarizer.summarize import summarize_texts
from summarizer.summary_modifiers import domain_extraction
from summarizer.summary_modifiers import problem_extractor
from summarizer.summary_modifiers import enlarge_summary
from summarizer.summary_modifiers import qualitate_summary

from json_editor.editor import edit_metadata

from language_detection.detector import detect_language

from data_loader.opeanai_formatters import text_message  

from google.cloud import storage 
from google.cloud import translate_v2
from image_utils.encoder import encode_image 
from datetime import datetime 

from metadata_producers.summaries import generate_chapter_metadata 
from metadata_producers.nodes import classify_about
from metadata_producers.exceptions import AboutListNotGeneratedException, DepthListNotGeneratedException

from synthesizers.synthesize import synthesizer 
from google.cloud.storage.retry import DEFAULT_RETRY
from segregator.segregation import segregator
from segregator.prompts import counting_prompt 
from segregator.modifier import get_relevant_count

from contents_parser.parse_index import parse_index
from contents_parser.exceptions import LLMTooDUMBException, IndexPageNotFoundException
from node_editor.edit_text_nodes import edit

from exceptions import EmptyPDFException
from exceptions import IncorrectGCPBucketException
from exceptions import NoChaptersFoundException
from summarizer.exceptions import SummaryNotFoundException

from chapter_broker.breakdown import segment_breakdown
from chapter_loader.structure import structure_html
from chapter_loader.loader import load_chapters 
from io import BytesIO


from font_chapter.extractcss import css_extractor 

from json import JSONDecodeError

load_dotenv(override=True)

question_type_map: Dict[str, str] = {
    "True/False": "trueFalse", 
    "Fill in the blanks": "fillInTheBlanks", 
    "Short Question Answer": "shortQuestionAnswer", 
    "Multiple Choice": "multipleChoice", 
    "Computational Questions": "computationQuestion", 
    "Software Code Questions": "softwareCodeQuestion", 
}
logger = logging.getLogger(__name__)


PROMPT_FILE_ID: str = os.environ.get("FILE_ID") 
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")
GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY")
HF_TOKEN: str = os.environ.get("HF_TOKEN")
BUCKET_NAME: str = os.environ.get("BUCKET_NAME")

# error directory 
ERROR_DIR: str = "error_dir"

gpt4o = OpenAI(api_key=OPENAI_API_KEY)
gpt4o_encoder = tiktoken.encoding_for_model("gpt-4o-mini")


# initalizing the bucket client  
gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
translator = translate_v2.Client.from_service_account_json(".secrets/translate_api.json")
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

retry = DEFAULT_RETRY.with_deadline(500.0)
retry = retry.with_delay(initial=1.5, multiplier=1.2, maximum=45.0)


#Endpoints 
@app.get("/")
async def home() -> Dict[str, str]: 
    return {"home": "page"}

@app.post("/upload_pdf") 
async def upload_pdfs(
    email_id: str = Form(...), 
    filename: str = Form(...), 
    pdf: UploadFile = File(...),  
) -> PDFUploadResponseModel: 

    start_time: int = time.time()


    try:
        content = await pdf.read()

        if len(content) == 0:
            raise EmptyPDFException()
        
        upload_pdf_blob = bucket.blob(os.path.join(
            email_id, 
            "uploaded_document", 
            filename, 
        ))

        with upload_pdf_blob.open("wb", retry=retry) as fp: 
            fp.write(content)

    # Checking for empty PDF 
    except EmptyPDFException as emptyPDF:
        error_line: int = emptyPDF.__traceback__.tb_lineno 
        error_name: str = type(emptyPDF).__name__
        raise HTTPException(
            status_code=404, 
            detail=f"EmptyPDFException: {error_line} for file {filename}"
        )

    # Checking for connection error 
    except urllib.error.URLError as e:
        if isinstance(e.reason, ConnectionError):
            error_line: int = e.__traceback__.tb_lineno 
            error_name: str = type(e).__name__
            raise HTTPException(
                status_code=404, 
                detail=f"NetworkError: {error_line} for file {filename}"
            )
    # Unexpected Exceptions
    except Exception as err: 
        error_line: int = err.__traceback__.tb_lineno 
        error_name: str = type(err).__name__
        raise HTTPException(
            status_code=404, 
            detail=f"Error {error_name} at line {error_line} for file {filename}"
        )    

        # Add successful upload to the response
    return PDFUploadResponseModel(
            email_id=email_id,
            filename=filename,
            time=time.time() - start_time,
        )

# No LLM is used in this step. SO we are not charging tokens. 
# we are however computing the amount of time this endpoint takes to run 
@app.post("/convert_pdf")
async def convert_pdf(pdf_file: 
    ConvertPDFModel) -> ConvertPDFOutputModel : 
    """
    Input: {
        filename: name of the book 
        email_id: email id of the user used as a unique identified 
    }

    Function: 
    Disintegrates the pdf into a set of images to be stored within processed_image directory  
    """
    # accessing the file blob from the URI 
    start_time = time.time()
    try: 
        pdf_blob = bucket.blob(os.path.join(
            pdf_file.email_id, 
            "uploaded_document", 
            pdf_file.filename, 
        ))
        
        with pdf_blob.open("rb") as f:   
            images: List[PIL.Image] = p2i.convert_from_bytes(
                f.read(), 
                dpi=200, 
                fmt="jpg", 
            )
        
        # check if PDF is uploaded in correct GCP bucket
        file_name = pdf_file.filename
        file_blob = bucket.blob(file_name)
        if not file_blob:
            raise IncorrectGCPBucketException()
        
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
    json_blob.chunk_size = 10 * 1024 * 1024 
    
    with json_blob.open("w", retry=retry) as f: 
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

@app.post("/extract_font_indices")
async def extract_font_indices(request: FontForChapterDetectionRequestModel) -> FontForChapterDetectionResponseModel: 
    start_time: float = time.time()
    # reading the json file 
    image_json_blob = bucket.blob(os.path.join(
        request.email_id, 
        "processed_image", 
        request.filename.split(".")[0] + ".json"
    ))

    fontdb_rules_blob = bucket.blob(os.path.join(
        request.email_id, 
        "fontwarehouse", 
        request.filename.split(".")[0], 
        "cssrules.csv"
    ))

    fontdb_page_combinations = bucket.blob(os.path.join(
        request.email_id, 
        "fontwarehouse", 
        request.filename.split(".")[0], 
        "fontdb.csv"
    ))

    top_five_styles_blob = bucket.blob(os.path.join(
        request.email_id, 
        "fontwarehouse", 
        request.filename.split(".")[0], 
        "top_five_styles.json"
    ))

    fontwise_narrowed_image_indices = bucket.blob(os.path.join(
        request.email_id, 
        "fontwarehouse", 
        request.filename.split(".")[0], 
        "chapter_image_fontwise_indices.json"
    ))

    with image_json_blob.open("rb") as fp: 
        images = json.load(fp=fp)
    
    font_db, css_rules, token_count = css_extractor(images, gpt4o, gpt4o_encoder)    

    with fontdb_rules_blob.open("w") as fp: 
        pd.DataFrame(css_rules).to_csv(fp)

    with fontdb_page_combinations.open("w") as fp: 
        pd.DataFrame(font_db).to_csv(fp)

    df = pd.DataFrame(font_db)
    top_five_fonts = (df["style"]
                    .value_counts()
                    .reset_index()
                    .iloc[:5, :]
                    .values
                    .tolist())
    
    with top_five_styles_blob.open("w") as fp: 
        json.dump(top_five_fonts,fp=fp)
    
    indices : list = []
    for _, font_count in enumerate(top_five_fonts):
        style, _ = font_count
        style_indices = list(filter(lambda ds: ds[1] == style, df.values.tolist()))
        style_index = [indx for indx, _ in style_indices]
        indices.extend(style_index)
    
    with fontwise_narrowed_image_indices.open("w") as fp: 
        json.dump({
           "chapter_indices": indices 
        }, fp = fp)
    
    return FontForChapterDetectionResponseModel(
        time = time.time() - start_time, 
        filename = request.filename, 
        token_count = token_count, 
        email_id=request.email_id, 
    )

@app.post("/extract_contents_page")
async def extract_contents_page(contents_request: ContentsRequestModel) -> ContentsResponseModel: 
    start_time: float = time.time()
    try: 
        images_blob = bucket.blob(os.path.join(
            contents_request.email_id, 
            "processed_image", 
            contents_request.filename.split('.pdf')[0] + ".json", 
        ))

        with images_blob.open("r") as f: 
            images: list = json.load(fp=f)  
        
        first_page, last_page, index_contents, token_count = parse_index(
            images, 
            contents_request.number_of_pages, 
            contents_request.language_code, 
            translator, 
            gpt4o, gpt4o_encoder
        )

        df = pd.DataFrame(index_contents, columns=["sectionName", "title", "headingType", "pageNo"])

        contents_page_blob = bucket.blob(os.path.join(
            contents_request.email_id, 
            "contents_page", 
            f"{contents_request.filename.split('.pdf')[0]}.csv", 
        ))


        with contents_page_blob.open("w", retry=retry) as fp: 
            df.to_csv(fp, index=False)

    except LLMTooDUMBException as tooDumb: 
        error_name: str = type(tooDumb).__name__
        error_line: int  = tooDumb.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}. Response: {tooDumb.response}"
        )

    except IndexPageNotFoundException as notFound: 
        error_name: str = type(notFound).__name__
        error_line: int  = notFound.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}. Number of pages: {notFound.number_of_pages}"
        )

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    return ContentsResponseModel(
        email_id=contents_request.email_id, 
        filename=contents_request.filename, 
        time=time.time() - start_time, 
        token_count = token_count, 
        first_page=first_page, 
        last_page=last_page, 
    )

@app.post("/identify/chapter_pages")
async def identify_chapters(identification_request: ChapterIdentificationRequestModel) -> ChapterIdentificationResponseModel: 
    start_time: int = time.time()
    try: 
        csv_blob = bucket.blob(os.path.join(
            identification_request.email_id, 
            "contents_page", 
            identification_request.filename.split(".pdf")[0] + ".csv", 
        ))

        image_blob = bucket.blob(os.path.join(
            identification_request.email_id,  
            "processed_image", 
            identification_request.filename.split(".pdf")[0] + ".json", 
        ))

        training_data_blob = bucket.blob(os.path.join(
            "TRAINING_DATA", 
            "train.json"    
        ))

        with csv_blob.open("r") as fp: 
            index_content_csv: pd.DataFrame = pd.read_csv(fp).values.tolist()
        
        with image_blob.open("r") as fp: 
            images: list[str] = json.load(fp=fp)

        with training_data_blob.open("r") as fp: 
            training_data: list = json.load(fp=fp)
        
        (content_csv, 
            labelled_chapters,
            unlabelled_chapters, 
            labelled_headings, 
            content_dict, 
            chapter_to_heading_map, 
            token_count) = segment_breakdown(
            images, index_content_csv, 
            identification_request.last_page, 
            identification_request.first_page, 
            identification_request.language_code, 
            gpt4o, gpt4o_encoder
        )

        chapter_count: int = len(labelled_chapters)
        non_chapter_count: int = 0.9 * chapter_count 


        if labelled_headings and len(labelled_headings) > int(non_chapter_count / 2) : 
            heading_chapters = random.sample(labelled_headings, k = int(non_chapter_count / 2)) 
        else: 
            heading_chapters = []

        if unlabelled_chapters and len(unlabelled_chapters) > int(non_chapter_count / 2) : 
            if not heading_chapters: 
                non_chapters = random.sample(unlabelled_chapters, k = int(non_chapter_count) ) 
            else: 
                non_chapters = random.sample(unlabelled_chapters, k = int(non_chapter_count / 2) ) 

        else: 
            non_chapters = []

        df: pd.DataFrame = pd.DataFrame(
            content_csv, 
            columns = [
                "title", 
                "section_number", 
                "index", 
                "heading_type" 
            ]
        )

        chapters: pd.DataFrame = df.loc[df.heading_type == "h1"]
        headings: pd.DataFrame = df.loc[df.heading_type == "h2"] 

        chapter_pages_csv_blob = bucket.blob(os.path.join(
            identification_request.email_id, 
            "book_sections", 
            identification_request.filename.split(".pdf")[0], 
            "chapters.csv"
        ))

        pages_csv_blob = bucket.blob(os.path.join(
            identification_request.email_id, 
            "book_sections", 
            identification_request.filename.split(".pdf")[0], 
            "all_pages.csv"
        ))

        headings_csv_blob = bucket.blob(os.path.join(
            identification_request.email_id, 
            "book_sections", 
            identification_request.filename.split(".pdf")[0], 
            "headings.csv"
        ))

        heading_sections_blob = bucket.blob(os.path.join(
            identification_request.email_id, 
            "book_sections", 
            identification_request.filename.split(".pdf")[0], 
            "sections.json"
        ))

        chapter_to_heading_map_blob = bucket.blob(os.path.join(
            identification_request.email_id, 
            "book_sections", 
            identification_request.filename.split(".pdf")[0], 
            "chapter_to_heading.json"
        ))

        with chapter_pages_csv_blob.open("w", retry=retry) as fp: 
            chapters.to_csv(fp, index=False)

        with pages_csv_blob.open("w", retry=retry) as fp: 
            df.to_csv(fp, index=False)

        with headings_csv_blob.open("w", retry=retry) as fp: 
            headings.to_csv(fp, index=False)
        
        with heading_sections_blob.open("w", retry=retry) as fp: 
            json.dump(content_dict, fp=fp)

        with chapter_to_heading_map_blob.open("w", retry=retry) as fp: 
            json.dump(chapter_to_heading_map, fp=fp)

        with training_data_blob.open("w", retry=retry) as fp: 
            training_data.extend(labelled_chapters)
            training_data.extend(non_chapters)
            training_data.extend(heading_chapters)
            json.dump(training_data, fp=fp)

    except LLMTooDUMBException as tooDumb: 
        error_name: str = type(tooDumb).__name__
        error_line: int  = tooDumb.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}. Response: {tooDumb.response}"
        )

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )

    return ChapterIdentificationResponseModel(
        email_id=identification_request.email_id, 
        filename = identification_request.filename, 
        time= time.time() - start_time, 
        token_count = token_count,  
    )

@app.post("/reform/chapter_pages")
async def reform_chapter_pages(request: ReformRequestModel) -> ReformResponseModel: 
    start_time: float = time.time()
    try: 
        chapter_csv_blob = bucket.blob(os.path.join(
            request.email_id, 
            "book_sections", 
            request.filename.split(".pdf")[0], 
            "chapters.csv"
        ))

        images_blob  = bucket.blob(os.path.join(
            request.email_id, 
            "processed_image", 
            request.filename.split(".pdf")[0] + ".json", 
        ))

        with images_blob.open("r") as fp: 
            images: list = json.load(fp=fp)

        with chapter_csv_blob.open("r") as fp: 
            chapters: list[list[str]] = pd.read_csv(fp).values.tolist()
        
        if not chapters: 
            raise NoChaptersFoundException("The chapters in the book were not found.") 
        
        for idx, chapter in enumerate(chapters[1:], 1):
            _, _, next_index, _ = chapter  
            curr_title, curr_section, curr_index, _ = chapters[idx-1]
            chapter_images: list = images[curr_index:next_index]

            chapter_image_blob = bucket.blob(os.path.join(
                request.email_id, 
                "chapter_processed_images", 
                request.filename.split(".pdf")[0], 
                f"{curr_section}_{curr_title}.json" 
            ))

            with chapter_image_blob.open("w", retry=retry) as fp: 
                json.dump(chapter_images, fp=fp)
                
        last_chapter, last_section, last_index, _ = chapters[len(chapters) - 1]
        chapter_image_blob = bucket.blob(os.path.join(
            request.email_id, 
            "chapter_processed_images", 
            request.filename.split(".pdf")[0], 
            f"{last_section}_{last_chapter}.json" 
        ))

        with chapter_image_blob.open("w", retry=retry) as fp: 
            json.dump(images[last_index:], fp=fp)

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    return ReformResponseModel(
        filename=request.filename, 
        email_id=request.email_id, 
        time=time.time() - start_time
    )

@app.get("/book_chapters/{email_id}/{filename}")
async def get_book_chapters(email_id: str, filename: str) -> JSONResponse: 
    try: 
        blobs = gcs_client.list_blobs(
            BUCKET_NAME, 
            prefix = os.path.join(
                email_id, 
                "chapter_processed_images", 
                f"{filename.split('.')[0]}/", 
            ), 
            delimiter = "/"
        ) 

        chapter_titles: list[str] = [blob.name.split("/")[-1] for blob in blobs]
    except Exception as err:
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )

    return dict(
        titles=chapter_titles, 
    ) 
    
@app.post("/json_editor")  
async def edit_text_json(request: JSONEditorRequestModel) -> JSONEditorResponseModel:
    start_time: float = time.time() 
    chapter_inherent_json_blob = bucket.blob(os.path.join(
        request.email_id,
        "chapterwise_processed_json",
        request.filename.split(".")[0],
        request.chapter_name.split(".json")[0],
        "inherent_metadata.json"
    ))

    chapter_rewritten_json_blob = bucket.blob(os.path.join(
        request.email_id,
        "intermediate_json",
        request.filename.split(".")[0],
        request.chapter_name.split(".json")[0],
        f"modified_processed_json_NODE_ID:{request.node_id}.json"
    ))

    analytical_metadata_json_blob = bucket.blob(os.path.join(
        "chapterwise_analytical_metadata", 
        "analysis_data.json"
    ))

    with chapter_inherent_json_blob.open("r") as fp: inherent_json = json.load(fp=fp) 
    with chapter_rewritten_json_blob.open("r") as fp: json_node = json.load(fp=fp)  

    if analytical_metadata_json_blob.exists(): 
        with analytical_metadata_json_blob.open("r") as fp: train_json : list = json.load(fp=fp)  
    else: 
        train_json: list = [] 

    user_modified_json: dict = json.loads(request.user_modified_json) 

    summary_text : str = " ".join([inherent_text["text"] for inherent_text in inherent_json])
    error_data, token_count = edit(json_node, user_modified_json, summary_text, gpt4o)
    train_json.extend(error_data) 
    
    with chapter_rewritten_json_blob.open("w") as fp: json.dump(user_modified_json, fp=fp) 
    with analytical_metadata_json_blob.open("w") as fp: json.dump(train_json, fp=fp)

    return JSONEditorResponseModel(
        email_id = request.email_id, 
        filename = request.filename, 
        time = time.time() - start_time, 
        token_count = token_count, 
        node_id = request.node_id, 
        chapter_name = request.chapter_name
    ) 


@app.post("/rectify_update_chain") 
async def rectify_update_chain(request : RectificationRequestModel) -> RectificationResponseModel:   
    start_time: float = time.time()
    try: 
        intermediate_json_blobs = gcs_client.list_blobs(
            BUCKET_NAME, 
            prefix=os.path.join(
                request.email_id, 
                "intermediate_json", 
                request.filename.split(".")[0], 
                request.chapter_name.split(".json")[0] + "/", 
            ), 
            delimiter="/"
        ) 

        summary_classification_blob = bucket.blob(os.path.join(
            request.email_id, 
            "chapter_summary_metadata", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            "classified_summary_content.json"
        ))

        older_classification_blob = bucket.blob(os.path.join(
            request.email_id, 
            "chapter_summary_metadata", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            "old_classified_summary_content.json", 
        ))

        with summary_classification_blob.open("r") as fp : summary_json = json.load(fp=fp) 
        with older_classification_blob.open("w") as fp: json.dump(summary_json, fp=fp) 

        concept : list = [] 
        sub_concept: list = []
        topic: list = [] 
        sub_topic: list = [] 
        major_domains: list = [] 
        root_concept: list = []
        sub_domains: list = [] 

        json_nodes: list = []
        for intermediate_json_blob in intermediate_json_blobs: 
            with intermediate_json_blob.open("r") as fp: data_node = json.load(fp=fp) 
            concept.append(data_node.get("concept", ""))
            sub_concept.append(data_node.get("sub_concept", ""))
            topic.append(data_node.get("topic", ""))
            sub_topic.append(data_node.get("sub_topic", ""))
            major_domains.append(data_node.get("major_domains", ""))
            root_concept.append(data_node.get("root_concept", ""))
            
            json_nodes.append(data_node) 

        strength_json, depth_json = summary_json
        strength_json["concept"] = list(set(concept)) 
        strength_json["sub_concept"] = list(set(sub_concept)) 
        strength_json["topic"] = list(set(topic)) 
        strength_json["sub_topic"] = list(set(sub_topic)) 
        depth_json["major_domains"] = list(set(major_domains)) 
        depth_json["root_concept"] = list(set(root_concept)) 
        depth_json["sub_domains"] = list(set(sub_domains)) 
        
        final_json_update_blob = bucket.blob(os.path.join(
            request.email_id, 
            "final_json", 
            request.filename.split(".")[0] + ".json", 
        ))

        with summary_classification_blob.open("w") as fp: json.dump([strength_json, depth_json], fp=fp)
        with final_json_update_blob.open("w") as fp: json.dump(json_nodes, fp=fp) 

    except Exception as err:
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    return RectificationResponseModel(
        time = time.time() - start_time, 
        email_id = request.email_id, 
        filename = request.filename, 
        chapter_name = request.chapter_name, 
    ) 

@app.post("/chapter_loader")
async def chapter_loader(request: ChapterLoaderRequestModel) -> ChapterLoaderResponseModel: 
    start_time = time.time()
    try: 
        chapter_to_heading_map_blob = bucket.blob(os.path.join(
            request.email_id, 
            "book_sections", 
            request.filename.split(".")[0], 
            "chapter_to_heading.json"
        ))

        chapters_blob = bucket.blob(os.path.join(
            request.email_id, 
            "book_sections", 
            request.filename.split(".")[0], 
            "chapters.csv"
        ))

        chapter_image_blob = bucket.blob(os.path.join(
            request.email_id, 
            "chapter_processed_images", 
            request.filename.split(".")[0], 
            request.chapter_name, 
        ))

        with chapter_to_heading_map_blob.open("r") as f:
            chapter_json: dict = json.load(f)
        
        with chapters_blob.open("r") as f:
            df: pd.DataFrame = pd.read_csv(f)
        
        with chapter_image_blob.open("r") as f: 
            chapter_images: list[dict]  = json.load(f) 
        
        responses, token_count = load_chapters(
            request.chapter_name, 
            chapter_json, 
            df, chapter_images, 
            request.language_code, 
            gpt4o, gpt4o_encoder
        )

        structured_chapter: list[dict] = structure_html(responses)

        chapter_processed_json_blob = bucket.blob(os.path.join(
            request.email_id, 
            "chapterwise_processed_json", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            "inherent_metadata.json" 
        ))

        with chapter_processed_json_blob.open("w", retry=retry) as fp: 
            json.dump(structured_chapter, fp)
        
    except Exception as err:
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    return ChapterLoaderResponseModel(
        email_id = request.email_id, 
        filename = request.filename, 
        time = time.time() - start_time, 
        token_count = token_count,  
        chapter_name = request.chapter_name 
    )
        
@app.post("/detect_lang") 
async def detect_lang(request: RequestModel) -> DetectedLanguageResponseModel: 
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
        image_blob = bucket.blob(f"{request.email_id}/processed_image/{request.filename.split('.pdf')[0]}.json")
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
    confidii: list[str] = []
    for image in chosen_images: 
        encoded_image: str = image["img_b64"]
        confidence, language, token_count = detect_language(
            encoded_image, 
            translator,
            gpt4o,   
            gpt4o_encoder, 
        )

        languages.append(language) 
        confidii.append(confidence)
    
    duration = time.time() - start_time
    
    return DetectedLanguageResponseModel(
        filename=request.filename, 
        email_id=request.email_id, 
        detected_language=max(languages, key=languages.count).lower(),
        time=duration, 
        token_count=token_count, 
        confidence=float(sum(confidii) / len(confidii)) 
    ) 

@app.post("/summarize")
async def summarize(request: SummarizationRequestModel) -> SummarizationResponseModel:
    start_time = time.time()
    try:
        chapter_json_blob = bucket.blob(os.path.join(
            request.email_id,
            "chapterwise_processed_json",
            request.filename.split(".")[0],
            request.chapter_name.split(".json")[0],
            "inherent_metadata.json"
        ))

        with chapter_json_blob.open("r") as fp:
            chapter_content = json.load(fp)

        summary_content: str = " ".join([node.get("text") for node in chapter_content]).strip()

        if summary_content:
            status, summary, token_count = summarize_texts(
                summary_content,
                request.language_code,
                gpt4o_encoder, gpt4o
            )

            summary_blob = bucket.blob(os.path.join(
                request.email_id, 
                "chapter_summary_metadata",
                request.filename.split(".")[0],
                request.chapter_name.split(".json")[0],
                "summary_content.txt"
            ))

            if status:
                with summary_blob.open("w", retry=retry) as f:
                    f.write(summary)

                enlarged_summary, token_count = enlarge_summary(
                    summary_content,
                    request.chapter_name,
                    summary,
                    gpt4o,
                )

                accurate_summary, token_count = qualitate_summary(
                    summary_content,
                    enlarged_summary,
                    gpt4o,
                )

                actual_json, token_count = domain_extraction(
                    accurate_summary,
                    gpt4o,
                )

                issues, principle_types, problems, token_count = problem_extractor(
                    summary_content, 
                    summary, 
                    accurate_summary,
                    gpt4o,
                )

                data: list = []
                for issue, principle_type, problem in zip(issues, principle_types, problems):
                    data.append({
                        "generated_output": summary,
                        "desired_generation": accurate_summary,
                        "issue_type": issue,
                        "principle_type": principle_type,
                        "differences": problem,
                        "field_type": "summarize", 
                        **actual_json
                    })

                result_blob = bucket.blob(os.path.join(
                    "chapterwise_analytical_metadata",
                    "analysis_data.json"
                ))

                if result_blob.exists(): 
                    with result_blob.open("r", retry=retry) as f:
                        existing_data = json.load(f)
                        existing_data.extend(data)
                else: 
                    existing_data = data

                with result_blob.open("w", retry=retry) as f:
                    json.dump(existing_data, f, indent=2)
            else:
                print("Empty summary here. Bad summarization output from llm")
                print(summary)
        else:
            token_count: int = 0
    except SummaryNotFoundException as summNotFound:
        error_name: str = type(summNotFound).__name__
        error_line: int = summNotFound.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404,
            detail=f"Error :{error_name} at line {error_line}. The error in response: {summNotFound.llm_response}"
        )

    except Exception as err:
        error_name: str = type(err).__name__
        error_line: int = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404,
            detail=f"Error :{error_name} at line {error_line}"
        )

    duration = time.time() - start_time
    return SummarizationResponseModel(
        filename=request.filename,
        email_id=request.email_id,
        time=duration,
        token_count=token_count,
        status=True
    )


@app.post("/summary_classifier")
async def classify_summary(request: SummaryChapterRequestModel) -> SummaryChapterResponseModel: 
    start_time = time.time()
    try: 
        summary_blob = bucket.blob(os.path.join(
            request.email_id, 
            "chapter_summary_metadata", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            "summary_content.txt"
        ))

        with summary_blob.open("r") as fp: 
            summary_content: str = fp.read()

        content, token_count = generate_chapter_metadata(
            summary_content, 
            request.language_code, 
            gpt4o_encoder, 
            gpt4o)
        
        classified_summary_blob = bucket.blob(os.path.join(
            request.email_id, 
            "chapter_summary_metadata", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            "classified_summary_content.json" 
        ))

        with classified_summary_blob.open("w", retry=retry) as f: 
            json.dump(content, fp=f)

    except JSONDecodeError as decodingError: 
        error_name: str = type(decodingError).__name__
        error_line: int  = decodingError.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )

    except AboutListNotGeneratedException as aboutNotGenerated:  
        error_name: str = type(aboutNotGenerated).__name__
        error_line: int  = aboutNotGenerated.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )

    except DepthListNotGeneratedException as depthNotGenerated: 
        error_name: str = type(depthNotGenerated).__name__
        error_line: int  = depthNotGenerated.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    return SummaryChapterResponseModel(
        filename=request.filename, 
        email_id=request.email_id, 
        chapter_name=request.chapter_name, 
        language_code=request.language_code, 
        time=time.time() - start_time, 
        token_count = token_count
    ) 

@app.get("/get_node_count/{email_id}/{filename}/{chapter_name}")
async def get_node_count(email_id: str, filename: str, chapter_name: str) -> JSONResponse: 
    try: 
        if not chapter_name.endswith(".json"): 
            chapter_name += "?.json"

        chapter_processed_json_blob = bucket.blob(os.path.join(
            email_id, 
            "chapterwise_processed_json", 
            filename.split(".")[0], 
            chapter_name.split(".json")[0], 
            "inherent_metadata.json"
        ))

        with chapter_processed_json_blob.open("r") as fp: 
            processed_json: dict = json.load(fp=fp)
        
        node_count: int = len(processed_json)

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    return {
        "chapter_name": chapter_name.split(".json")[0], 
        "node_count": node_count, 
        "email_id": email_id, 
        "filename": filename, 
    }

@app.post("/rewrite_json")
async def rewrite_json(request: RewriteJSONRequestModel) -> RewriteJSONResponseModel: 
    start_time = time.time()
    try: 
        extracted_json_blob = bucket.blob(os.path.join(
            request.email_id, 
            "chapterwise_processed_json", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            "inherent_metadata.json"
        ))
        
        # after reading this json content you process it with the metadata_generators
        with extracted_json_blob.open("r") as f:  
            extracted_json = json.load(fp=f)[request.node_id]

        # open the classified summary blob from the summaries section 
        classified_summary_blob = bucket.blob(os.path.join(
            request.email_id, 
            "chapter_summary_metadata", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            "classified_summary_content.json"
        )) 
        
        with classified_summary_blob.open("r") as f:   
            generated_list = json.load(fp=f)
        
        generated_metadata_blob = bucket.blob(os.path.join(
            request.email_id, 
            "intermediate_json", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            f"modified_processed_json_NODE_ID:{request.node_id}.json"
        ))

        # classify the prompt 
        comprehensive_node, token_count = classify_about(
            extracted_json, 
            generated_list, 
            request.language_code, 
            gpt4o, 
            gpt4o_encoder, 
        )

        with generated_metadata_blob.open("w", retry=retry) as fp: 
            json.dump(comprehensive_node, fp=fp) 

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
            
    duration = time.time() - start_time
    # process complete 
    return RewriteJSONResponseModel(
        filename=request.filename, 
        email_id=request.email_id, 
        node_id=request.node_id, 
        language_code=request.language_code, 
        time=duration, 
        token_count=token_count, 
    )

@app.post("/preprocess_for_graph")
async def push_to_json(request: RequestModel) -> PushToJsonResponseModel: 
    start_time: float = time.time()
    try: 
        blobs = gcs_client.list_blobs(
            BUCKET_NAME, 
            prefix=os.path.join(
                request.email_id, 
                "intermediate_json", 
                request.filename.split(".")[0], 
            )
        )

        json_blob = bucket.blob(os.path.join(
            request.email_id, 
            "final_json", 
            f"{request.filename.split('.')[0]}.json", 
        ))

        book_associated_json = []

        for blob in blobs: 
            with blob.open("r") as fp: 
                chapter_associated_processed_json = json.load(fp=fp)
                book_associated_json.append(chapter_associated_processed_json)
                
        with json_blob.open("w", retry=retry) as fp: 
            json.dump(book_associated_json, fp=fp)    

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )

    return PushToJsonResponseModel(
        filename=request.filename, 
        email_id=request.email_id, 
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

@app.post("/get_text_node")
async def get_text_node(request: TextNodeRequestModel) -> TextNodeResponseModel: 
    start_time: float = time.time() 
    try: 
        generated_metadata_blob = bucket.blob(os.path.join(
            request.email_id, 
            "intermediate_json", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            f"modified_processed_json_NODE_ID:{request.node_id}.json"
        ))

        with generated_metadata_blob.open("r") as fp: data = json.load(fp=fp)

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    return TextNodeResponseModel(
        filename= request.filename, 
        chapter_name = request.chapter_name, 
        email_id = request.email_id, 
        json_content = json.dumps(data, indent=4), 
        node_id = request.node_id, 
        time = time.time() - start_time, 
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
async def synthesize_relative_strength(request: SynthesisContentRequestModel) -> SynthesisContentResponseModel: 
    starting_time: float = time.time()
    try: 
        classified_metadata_blob = bucket.blob(os.path.join(
            request.email_id, 
            "intermediate_json", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            f"modified_processed_json_NODE_ID:{request.node_id}.json"
        ))

        with classified_metadata_blob.open("r") as f: 
            json_to_be_modified = json.load(fp=f)
        
        status, score, token_count = synthesizer(
            json_to_be_modified[request.branch_name], 
            json_to_be_modified["text"],
            gpt4o, 
            gpt4o_encoder, 
        )

        if not status: 
            score = 0
        
        json_to_be_modified[f"{request.branch_name}_strength"] = score

        with classified_metadata_blob.open("w", retry=retry) as f: 
            json.dump(json_to_be_modified, fp=f)

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    duration = time.time() - starting_time
    return SynthesisContentResponseModel(
        filename=request.filename, 
        email_id=request.email_id, 
        node_id=request.node_id, 
        branch_name=request.branch_name, 
        time=duration, 
        token_count=token_count
    )


@app.post("/synthesize/strength/representational")
async def synthesize_relative_strength(request: SynthesisContentRequestModel) -> SynthesisContentResponseModel: 
    starting_time: float = time.time()
    try: 
        classified_metadata_blob = bucket.blob(os.path.join(
            request.email_id, 
            "intermediate_json", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            f"modified_processed_json_NODE_ID:{request.node_id}.json"
        ))

        with classified_metadata_blob.open("r") as f: 
            json_to_be_modified = json.load(fp=f)
        
        status, score, token_count = synthesizer(
            json_to_be_modified[request.branch_name], 
            json_to_be_modified["text"],
            gpt4o, 
            gpt4o_encoder, 
        )

        if not status: 
            score = 0
        
        json_to_be_modified[f"{request.branch_name}_representation_strength"] = score

        with classified_metadata_blob.open("w", retry=retry) as f: 
            json.dump(json_to_be_modified, fp=f)

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    duration = time.time() - starting_time
    return SynthesisContentResponseModel(
        filename=request.filename, 
        email_id=request.email_id, 
        node_id=request.node_id, 
        branch_name=request.branch_name, 
        time=duration, 
        token_count=token_count
    )


@app.post("/synthesize/depth/representational")
async def synthesize_relative_strength(request: SynthesisContentRequestModel) -> SynthesisContentResponseModel: 
    starting_time: float = time.time()
    try: 
        classified_metadata_blob = bucket.blob(os.path.join(
            request.email_id, 
            "intermediate_json", 
            request.filename.split(".")[0], 
            request.chapter_name.split(".json")[0], 
            f"modified_processed_json_NODE_ID:{request.node_id}.json"
        ))

        with classified_metadata_blob.open("r") as f: 
            json_to_be_modified = json.load(fp=f)
        
        status, score, token_count = synthesizer(
            json_to_be_modified[request.branch_name], 
            json_to_be_modified["text"],
            gpt4o, 
            gpt4o_encoder, 
        )

        if not status: 
            score = 0
        
        json_to_be_modified[f"{request.branch_name}_representation_depth"] = score
        classified_metadata_blob.chunk_size = 10 * 1024 * 1024

        with classified_metadata_blob.open("w", retry=retry) as f: 
            json.dump(json_to_be_modified, fp=f)

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    
    duration = time.time() - starting_time
    return SynthesisContentResponseModel(
        filename=request.filename, 
        email_id=request.email_id, 
        branch_name=request.branch_name, 
        node_id=request.node_id, 
        time=duration, 
        token_count=token_count
    )

@app.post("/pdf_page_count") 
async def retrieve_page_count(request: PdfPageCountRequestModel) -> PdfPageCountResponseModel: 
    start_time: float = time.time() 
    try: 
        uploaded_document = bucket.blob(os.path.join(
            request.email_id, 
            "uploaded_document", 
            request.filename
        ))

        with uploaded_document.open("rb") as document: 
            with tempfile.TemporaryDirectory() as temp_dir:  
                temp_file_path: str = f"{temp_dir}/{request.filename}"
                temp_file = open(temp_file_path, "wb")  
                temp_file.write(document.read())
                temp_file.close() 
                pdf_file = pymupdf.open(temp_file_path)

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
        
    return PdfPageCountResponseModel(
        page_count = len(pdf_file), 
        time = time.time() - start_time, 
        filename=request.filename,  
        email_id=request.email_id, 
    )



@app.post("/segregate")
async def segregate_json(request: RequestModel) -> ResponseModel: 
    start_time: float = time.time()
    final_json_blob = bucket.blob(os.path.join(
        request.email_id, 
        "final_json", 
        f"{request.filename.split('.')[0]}.json"
    ))

    with final_json_blob.open("r") as f: 
        final_json = json.load(fp=f)
    
    topics, concepts, headings = segregator(final_json)
    
    topic_blob = bucket.blob(os.path.join(
        request.email_id, 
        "books", 
        request.filename.split(".")[0], 
        "topic.json"
    ))


    concept_blob = bucket.blob(os.path.join(
        request.email_id, 
        "books", 
        request.filename.split(".")[0], 
        "concept.json"
    ))


    headings_blob = bucket.blob(os.path.join(
        request.email_id, 
        "books", 
        request.filename.split(".")[0], 
        "heading_text.json"
    ))

    with topic_blob.open("w", retry=retry) as f: 
        json.dump(topics, fp=f)

    
    with headings_blob.open("w", retry=retry) as f: 
        json.dump(headings, fp=f)


    with concept_blob.open("w", retry=retry) as f: 
        json.dump(concepts, fp=f)
    
    return ResponseModel(
        time=time.time() - start_time, 
        token_count = 0
    ) 

@app.post("/modify_branch") 
async def modify_branch(branch_data: ModificationInputModel) -> ModificationOutputModel: 
    start_time = time.time()
    try: 
        branch_blob = bucket.blob(os.path.join(
            branch_data.email_id, 
            "books", 
            branch_data.filename.split(".")[0], 
            f"{branch_data.branch_name}.json", 
        ))

        with branch_blob.open("r") as f:
            js_object = json.load(fp=f)
        
        branch_modified, token_count = get_relevant_count(
            js_object, [text_message[1]], 
            counting_prompt, gpt4o, gpt4o_encoder
        )

        with branch_blob.open("w", retry=retry) as f: 
            json.dump(branch_modified, fp=f)

    except Exception as err: 
        error_name: str = type(err).__name__
        error_line: int  = err.__traceback__.tb_lineno
        raise HTTPException(
            status_code=404, 
            detail = f"Error :{error_name} at line {error_line}"
        )
    
    return ModificationOutputModel(
        filename=branch_data.filename, 
        email_id=branch_data.email_id, 
        branch_name=branch_data.branch_name, 
        time=time.time() - start_time, 
        token_count=token_count, 
    )

@app.post("/generate_excel")
async def generate_qna_topic_wise(request: QNATopicWiseRequest):
    try:
        final_json_blob = bucket.blob(f"{request.email_id}/final_json/{request.filename.split('.')[0]}.json")
        with final_json_blob.open("r") as blb:
            json_qna: list[str] = json.load(blb)
        
        df = pd.DataFrame(json_qna)
        
        tasks = []
        
        for topic_name, topic_df in df.groupby("topic"):
            topic_texts = topic_df["text"].tolist()
            task = generate_qna_for_topic(topic_name, topic_texts, gpt4o, gpt4o_encoder)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        all_results = {}
        for topic_name, topic_result in results:
            all_results[topic_name] = topic_result
        
        output_path = f"{request.email_id}/excel_output/{request.filename.split('.')[0]}_qna.xlsx"
        excel_blob = bucket.blob(output_path)
        
        with BytesIO() as output:
            with pd.ExcelWriter(output) as writer:
                for topic_name, topic_data in all_results.items():
                    topic_df = pd.DataFrame(topic_data)
                    topic_df.to_excel(writer, sheet_name=topic_name[:31], index=False)  # Excel sheet names limited to 31 chars
            
            excel_blob.upload_from_string(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
        return {"status": "success", "excel_path": output_path}
        
    except Exception as err:
        logger.error(f"Error generating Excel: {str(err)}")
        return {"status": "error", "message": str(err)}
    
@app.post("/add_word_count") 
async def add_word_count(edit_metadata_request: MetaDataEditModel) -> MetaDataEditResponseModel: 
    start_time = time.time()
    final_json_blob = bucket.blob(os.path.join(
        edit_metadata_request.email_id, 
        "final_json", 
        f"{edit_metadata_request.filename.split('.')[0]}.json", 
    ))

    with final_json_blob.open("r") as f:
        final_json = json.load(fp=f)
    
    concept_blob = bucket.blob(os.path.join(
        edit_metadata_request.email_id, 
        "books", 
        edit_metadata_request.filename.split(".")[0], 
        "concept.json"
    ))

    topic_blob = bucket.blob(os.path.join(
        edit_metadata_request.email_id, 
        "books", 
        edit_metadata_request.filename.split(".")[0], 
        "topic.json"
    ))

    heading_text_blob = bucket.blob(os.path.join(
        edit_metadata_request.email_id, 
        "books", 
        edit_metadata_request.filename.split(".")[0], 
        "heading_text.json"
    ))

    with concept_blob.open("r") as f: 
        concept_json = json.load(fp=f) 

    with topic_blob.open("r") as f: 
        topic_json = json.load(fp=f) 

    with heading_text_blob.open("r") as f: 
        heading_json = json.load(fp=f)
        
    metadata_edited_final: List = edit_metadata(final_json, heading_json, concept_json, topic_json)
    with final_json_blob.open("w", retry=retry) as f: 
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
                question_distribution[question_type][chapter_name][topic_node[category]] = int(round(
                    chapter_question_count * 
                    (preference_weights[topic_node["preferenceLevel"]] / net_weights) 
                , 0))

    modified_final_json : List = []

    try: 
        final_json_blob = bucket.blob(os.path.join(
            emailId, 
            "final_json", 
            f"{fileName.split('.')[0]}.json", 
        ))

        with final_json_blob.open("r") as f: 
            final_json = json.load(fp=f)
        
        didnt_enter_count = 0  
        for _, js_object in enumerate(final_json) :
            if (f"{category}_strength" in js_object 
                and f"{category}_representation_depth" in js_object 
                and f"{category}_representation_strength" in js_object): 


                js_object["cumulative_strength"] = (degree_weights[js_object[f"{category}_strength"]] + 
                                depth_value_weights[js_object[f"{category}_representation_depth"]] +
                                assign_value_weights[js_object[f"{category}_representation_strength"]]) 

                modified_final_json.append(js_object)
            else: 
                js_object["cumulative_strength"] = 0
                didnt_enter_count += 1
            
        print("Error count ", didnt_enter_count) 
        print("Net length ", len(final_json)) 

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
                        sorted(list(filter(lambda mp: mp[category] == topic_name, modified_final_json)),
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

            with generation_data_blob.open("w", retry=retry) as f: 
                json.dump(qd_dict, fp=f)

        except Exception as err: 
            print("No such object found")
            print("error: %s at line %s" % (type(err).__name__, err.__traceback__.tb_lineno))

    else: 
        print("The list was empty ")

    return {"email_id": emailId, "filename": fileName, "computed_question_data": mk} 


@app.post("/generate")
async def generate(request: GenerationContext) -> Dict[str, str | int| float]:
    start_time: float = time.time()

    try: 
        generation_metadata_blob = bucket.blob(os.path.join(
            request.email_id, 
            "generation_data", 
            f"{request.filename}.json", 
        ))
    except Exception as e: 
        print(f"The file {request.filename} has not been processed")
        print(e)

    with generation_metadata_blob.open("r") as f: 
        generation_data = json.load(fp=f)

    associated_json: Dict = generation_data[request.question_type][request.chapter_name][request.topic_name]
    question_count = associated_json["topic_question_count"] 
    text = ""

    for paragraph_node in associated_json["topic_json"]: 
        text += paragraph_node["text"]

    qna_prompt: str = prompts[request.question_type]

    qna, token_count = generate_response(
        messages=text_message, 
        prompt=qna_prompt, 
        validation_prompt=qna_validation_prompt, 
        convert_to_html_prompt=convert_to_html_prompt, 
        context=text,  
        question_count=question_count, 
        language=request.language, 
        gpt4o_encoder=gpt4o_encoder, 
        gpt4o=gpt4o, 
    )

    # dump the output to gcp 
    try: 
        generated_dump_blob = bucket.blob(os.path.join(
            request.email_id, 
            "generated_content", 
            request.filename, 
            f"{request.question_type}_{request.chapter_name}_{request.topic_name}.html", 
        ))

        with generated_dump_blob.open("w", retry=retry) as f: 
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
        
@app.post("/get_status")
async def get_status(request: StatusRequestModel) -> JSONResponse:
    uploaded_pdfs_blobs  = gcs_client.list_blobs(
        BUCKET_NAME, 
        prefix = os.path.join(
            request.email_id,
            "uploaded_document"
        ), 
        delimiter="/", 
    )  

    finished_pdf_blobs = gcs_client.list_blobs(
        BUCKET_NAME, 
        prefix = os.path.join(
            request.email_id, 
            "final_json"
        ), 
        delimiter="/" 
    )

    uploaded_pdfs = []
    finished_pdfs = [] 
    for uploaded_file_blob in uploaded_pdfs_blobs: 
        uploaded_pdfs.append(uploaded_file_blob.name) 
        
    for finished_pdf_blob in finished_pdf_blobs: 
        finished_pdfs.append(finished_pdf_blob.name)

    statuses: list = []
    
    for uploaded_pdf in uploaded_pdfs:  
        if uploaded_pdf in finished_pdfs: 
            statuses.append({
                "file_name": uploaded_pdf.split("/")[-1], 
                "status": "Completed", 
                "status_id": 3, 
                "created_on": str(datetime.now()) 
            })
        else: 
            statuses.append({
                "file_name": uploaded_pdf.split("/")[-1], 
                "status": "Pending", 
                "status_id": 1, 
                "created_on": str(datetime.now()) 
            })
    
    return statuses

@app.post("/get_all_processed_books") 
async def processed_books_request(request: FinalBookListRequest) -> FinalBookListResponse: 
        existent_blobs = gcs_client.list_blobs(
            BUCKET_NAME, 
            prefix=f"{request.email_id}/final_json/", 
            delimiter="/"
        )

        blob_names = [blob.name.split("/")[-1].split(".json")[0]
                                 for blob in existent_blobs]
        
        return FinalBookListResponse(
            email_id=request.email_id, 
            book_list=blob_names, 
        ) 

@app.post("/run_subprocess") 
async def run_subprocess(request: RunSubprocessRequest) -> SubprocessInitiatedResponse:
    """
    Initiates the binary process asynchronously by executing:
        ../autopipeline/project-astra --filename <filename> --emailId <email_id>
    Instead of waiting for the process to complete, it schedules a background task
    to await its termination (using asyncio.create_task(process.wait())),
    ensuring that the process is properly reaped (avoiding zombie processes).
    """
    command = [
        "../autopipeline/project-astra",
        "--filename", request.filename,
        "--emailId", request.email_id
    ]
    
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Schedule waiting for process termination in the background
    asyncio.create_task(process.wait())

    return SubprocessInitiatedResponse(filename=request.filename, email_id=request.email_id)            

@app.post("/send-email")
def send_email(request_data: EmailRequest):
    payload = {
        "request_key": "OpenEyes_1224EzZykXxo",
        "email_key": "RequestComplated",
        "request_emails": [request_data.email],
        "dynamic_data": {"current_year": "2025"}
    }
    
    try:
        response = requests.post( "https://oeservices.uatbyopeneyes.com/api/v1/sendMailWithOpenEyesMT", json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
        

