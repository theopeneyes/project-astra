import streamlit as st
import tempfile 
import os
from openai import OpenAI

import pandas as pd 
from typing import List, Dict 

from google.generativeai.types import HarmCategory, HarmBlockThreshold
from matplotlib import pyplot as plt 

import re 
import json 
import requests 

import PIL 

import base64
import pdf2image as p2i 
from io import BytesIO


from dotenv import load_dotenv
import google.generativeai as genai 
import pandas as pd 

# Prompts

json_example: str = """{
    "root_concept": str,
    "major_domains": List[str],
    "sub_domains": List[str],
    "concepts": List[str],
    "Attributes and connections": Dict[str, List[str]],
    "formal_representations": Dict[str, List[str]],
})"""


# definition prompt 
definitions = '''
Here is a thought: ### Ontology creation prompt ###
Objective: Develop Root Concept, Major Domains, Sub Domains, Concepts, Attributes and Relationships, and Formal Representations for the subject covering the list of concepts provided herewith as an ontology.
### Definitions ###
1. Root Concept: The fundamental idea or principle that serves as the foundation for the text's subject matter. It encapsulates the core theme or overarching idea.
2. Major Domains: Broad areas of knowledge or fields that encompass multiple related topics or subjects. These domains provide a framework for organizing concepts within the root concept.
3. Sub Domains: More specific areas within major domains that further refine the focus. Sub domains represent narrower categories that contribute to a deeper understanding of the major domain.
4. Concepts: Individual ideas or phenomena that are part of a sub domain. Concepts represent specific instances, theories, or practices related to the subject matter.
5. Attributes and connections: Characteristics or properties that describe a concept. Attributes provide additional detail and context, helping to define the concept more clearly. Connections or interactions between concepts, attributes, and other entities. Relationships illustrate how different elements relate to one another within the context of the root concept.
6. Formal Representations: Structured ways of depicting concepts, attributes, and relationships, such as models, diagrams, or frameworks. These representations help visualize the connections and hierarchies within the subject matter.
'''

# The inputs go, chapter json, definition json and json_example json 
json_extractor_prompt: str = """
Read the {} and find me the following out of it: 
Root concept, major domain, sub domains, concepts, Attributes and Connections, Formal representations. 
The definition for each is given here: {}. 
Your output should be a JSON, with each variable being the key and the content corresponding to it as its value.
###Incentives###
You will receive a tip of $$$ for correct description.
You will be penalized if you fail to follow instructions or guidance

####JSON structure####:
{}

####Instructions####:
Your output must be unambiguous. DO NOT EXPLAIN.
Extracted JSON:
"""

clause_prompt: str = "If one doesn't exist then use '{}' as the title. "
# main prompts
prompt: str = """
You are a HTML converter bot. Your TASK is to convert text and image as text from a given image
of a page from a book into a HTML document.

Here are further detailed instructions:
Input: You will be given an image from a page of a book. This page will be part of a Chapter from a
book containing sections, and sub-sections and within subsections will be units of Paragraphs and Images. Images could be of Types: [Chart, Diagram, Tables]

Your goal is to extract text from the image of a page from a book conserving the hierarchical
nature of the way the page is structured. You will use HTML tags to conserve the hierarchy.

Follow the following steps when encountered with a page:

Step 1: Determine if the page contains a chapter heading. {}Encapsulate the title within <title>
tags. NOTE that each page must only have ONE unique title and VERIFY that the chosen title is a
chapter title and not a section heading or a sub section heading.

Step 2: Determine if the page contains any section headings. {} Encapsulate the section heading
within <h1> tags. The page can have multiple section headings. VERIFY that the chosen <h1> heading
is a section heading and not a chapter heading or a sub section heading.

Step 3: Identify if the page has any sub section headings. {} Encapsulate it within <h2> tags.
The page can have multiple sub section headings. VERIFY that the chosen <h2> heading is a sub
section heading and not a chapter heading or a section heading.

In any of these above steps, if you encounter a paragraph text, then encapsulate it within <p> tags.

Step 4: Identify if there are any images and classify the type of image into one of 3 categories:
diagram, chart or table.

The definitions of which are given below:

## Definitions
chart: A chart (sometimes known as a graph) is a graphical representation for data visualization,
in which the data is represented by symbols, such as bars in a bar chart, lines in a line chart,
or slices in a pie chart
table: A table is an arrangement of information or data, typically in rows and columns,
or possibly in a more complex structure.
diagram: Any image that isn't a table or a chart is a diagram.

Step 5: Once you have identified the type of image, convert the image into text by explaining the
relevance of the image given the context of the surrounding text and tag them within their
respective tags. For example: encapsulate chart with <chart> tags, diagrams with <diagram>
If the image contains a table, extract the contents of the table as is, and encapsulate it within
<table> tags.

You MUST only use the following list of tags:
[<p>, <h1>, <h2>, <table>, <td>,  <tr>, <th>, <diagram>, <chart>, <title>]

## Instructions
Your outcomes MUST be simple and unambigous.

## Incentives
You will recieve a tip of $$$ for correct conversion
You will be penalized if you fail to conver the document effectively
"""


# MODULE CODE 
messages: List[Dict] = [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "", 
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,{}", 
          }
        }
      ]
    }
]


# loader to get json from the loaded dataframe 
def get_json(book_json: Dict[str, str|int|None], hf_token: str) -> Dict[str, List[str]] | str: 

    API_URL: str = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json",
        "x-wait-for-model": "true"
    }

    book_text: str = book_json["text"]

    # chapter, definition, example 
    response = requests.post(
        API_URL, 
        headers=headers, 
        json = {
            "inputs": json_extractor_prompt.format(
               book_text, definitions, json_example,  
            ),  
            "parameters": {"max_new_tokens": 600, "temperature":0.1}
        }
    ).json() 

    extracted_json = response[0]["generated_text"].split("Extracted JSON:")[1].split("###")[0].strip()
    cleaned_response = re.sub(r'\s+', ' ', extracted_json)
    cleaned_response = cleaned_response.replace("'", '"')
    
    try:
        # Step 4: Parse and pretty print the cleaned JSON string
        data = json.loads(cleaned_response)
        data = {**data, **book_json}
    except json.JSONDecodeError as e:
        #TODO: For JK: Fix the issue of decoding 
        # Some json produced by LLMs do not produce decodeable jsons. Need to fix this issue. 
        print(f"Error decoding JSON: {e}")
        return ""

    return data

def structure_html(output: List[str]) -> List[Dict[str, str|int|None]]:  
    """
    output: List[str] 
    A list of html documents converted from a pdf page using the
    Gemini API.  

    returns: pd.DataFrame 
    Structures the output as a DataFrame to send to the 
    Data Tagger and Organizer 
    """

    title: str| None = None
    heading: str | None  = None
    sub_heading: str | None = None
    table_on: bool = False
    table_content: List[str]
    df_json : List[Dict[str, str]] = []

    for html_page in output:
        paragraph_count: int = 0
        for html_tag in html_page.split("\n"):
            if html_tag.startswith('```'): continue
            elif html_tag.startswith("<table"):

                table_on = True
                table_content = []
                continue

            elif table_on and html_tag.startswith("</table>"):
                table_on = False
                table_content = "\n".join(table_content)
                text = ['table', heading, sub_heading, table_content]

            elif table_on:
                table_content.append(html_tag)
                continue

            elif ( html_tag.startswith('<title>') and
                  html_tag.split(">")[1].split("<")[0] != title) :

                title = html_tag.split(">")[1].split("<")[0]
                continue

            elif ( html_tag.startswith("<h1>") and
                  html_tag.split(">")[1].split("<")[0] != heading):

                heading = html_tag.split(">")[1].split("<")[0]
                continue

            elif (html_tag.startswith("<h2>") and
                  html_tag.split(">")[1].split("<")[0] != sub_heading):

                sub_heading = html_tag.split(">")[1].split("<")[0]
                continue

            elif html_tag.startswith("<p>") :
                text = ['text', heading, sub_heading, html_tag.split(">")[1].split("<")[0]]
                paragraph_count += 1

            elif html_tag.startswith("<diagram>"):
                text = ['diagram', heading, sub_heading, html_tag.split(">")[1].split("<")[0]]
                paragraph_count += 1

            elif html_tag.startswith("<chart>"):
                text = ['chart', heading, sub_heading, html_tag.split(">")[1].split("<")[0]]
                paragraph_count += 1
            else:
                continue

            df_json.append({
                "heading_identifier": title,
                "heading_text": text[1],
                "sub_heading_text": text[2],
                "text_type": text[0],
                "paragraph_number": paragraph_count,
                "text": text[3],
            })

    return df_json


def encode_image(image: PIL.Image): 
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def parse_pdf(config, st: st,  
              pdf_path: str, prompt: str,
              clause_prompt: str,
              name_of_pdf: str,
              error_dir: str, 
              messages: List) -> List[str]:

    title: str | None = None
    new_prompt: str
    output: List[str] = []

    with st.spinner("Converting the pdf pages to images..."): 
        images: List[PIL.Image] = p2i.convert_from_path(
            pdf_path,
            dpi=200,
        )

    for i, image in enumerate(images):
        with st.spinner(f"Sending Image {i+1} to Gemini..."): 
            if title:
                new_prompt = prompt.format(clause_prompt.format(title, "title"), "", "")
            else:
                new_prompt = prompt.format("", "", "")

            response = gemini.generate_content(
                [ new_prompt, image],
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                },
                generation_config = config,
            )

        try:
            output.append(response.text)
            if re.findall(r"<title>(.*?)</title>", output[-1])[0] != title:
                title = re.findall(r"<title>(.*?)</title>", output[-1])[0]

        except Exception as _:
            with st.spinner("Error occured in Gemini, sending it now to GPT4oMini..."): 
                messages[0]["content"][0]["text"] = new_prompt 
                messages[0]["content"][1]["image_url"]["url"] = (
                    f"data:image/jpeg;base64,{encode_image(image)}") 

                response = gpt4o.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                )

            try: 
                output.append(response.choices[0].message.content)
                if re.findall(r"<title>(.*?)</title>", output[-1])[0] != title:
                    title = re.findall(r"<title>(.*?)</title>", output[-1])[0]
                    
            except Exception as _: 
                with st.spinner(f"Couldn't parse Image {i+1}, saving the image for inspection..."): 
                    plt.imshow(image)
                    plt.savefig(os.path.join(error_dir, f"{name_of_pdf}_page_{i}.jpg"))
    
    return output

#loading environment variables 
load_dotenv()

PROMPT_FILE_ID: str = os.getenv("FILE_ID", None) # file_id to fetch remote prompt design sheet
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", None) # gemini api key 
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", None) # openai api key 
HF_TOKEN: str = os.getenv("HF_TOKEN", None) # huggingface token 

ERROR_DIR: str = "data_loader/image_error"

genai.configure(api_key=GEMINI_API_KEY)

config = genai.GenerationConfig(
    temperature=0,
    top_p = 0.98,
    top_k = 5,
)

gemini = genai.GenerativeModel(model_name="gemini-1.5-flash")
gpt4o = OpenAI(api_key=OPENAI_API_KEY)

#models we will be using 
models: List = [gemini, gpt4o]

# Streamlit UI
st.title("Project Astra Demo")

# File uploader component
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

# If a file is uploaded
if uploaded_pdf is not None:
    with tempfile.TemporaryDirectory() as temp_dir: 
        file_path = os.path.join(temp_dir, uploaded_pdf.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())
        
        with st.spinner("Parsing the file..."): 
            html_pages: List[str] = parse_pdf(
                config, st, 
                file_path, prompt, clause_prompt, 
                uploaded_pdf.name, ERROR_DIR, messages)
        
        
        with st.spinner("Converting HTML to Table..."): 
            text_metadata: List[Dict[str, str| int | None]] = structure_html(html_pages)

        # Data classifier part 
        with st.spinner("Sending each text to the classifier..."): 
            json_outputs: List[Dict] = []
        
            for idx, text_json in enumerate(text_metadata): 
                with st.spinner(f"Converting HTML for Page {idx+1} to json..."):
                    op = get_json(text_json, HF_TOKEN)
                    if op != "":    
                        json_outputs.append(op) 

        with st.spinner("Generating json..."): 
            print(json_outputs)
            json_df: pd.DataFrame = pd.DataFrame.from_records(json_outputs)
        
        st.write("Data Classifier output")
        st.dataframe(json_df)
