import streamlit as st
import os
import pandas as pd 

from typing import List, Dict
from gensim.models import Word2Vec
from io import BytesIO
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 
from openai import OpenAI

import requests 
import PIL 
import base64
import datamapplot
import matplotlib

import pandas as pd 
import streamlit as st
import numpy as np 
import pyrebase
import json 
import asyncio 
import aiohttp


from google.cloud import storage
from dotenv import load_dotenv
import google.generativeai as genai 

load_dotenv()

# Prompts
json_example: str = """{
    "root_concept": str,
    "major_domains": List[str],
    "sub_domains": List[str],
    "concepts": List[str],
    "Attributes and connections": Dict[str, List[str]],
    "formal_representations": Dict[str, List[str]],
}"""
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
short_question_answer_prompt: str = """
You are a Short Question Answer Generator Bot. Your goal is to generate Short 
Question Answers based on the following instructions.  

Definition: Short answer questions are typically composed of a brief prompt that demands a written answer that varies in length from one or two words to a few sentences.

###TASK###: You MUST create Short Answer Question based on the provided text and the topic to which they fall under. 

### OUTPUT FORMAT: 
Your output MUST be in the following format: 
<b>Q: [Your question]</b> 
<p>A: [Your answer]</p> 

### Instructions###: 
  - Your own words – not statements straight out of the textbook
  - Specific problem and direct questions

###Incentives###
You will receive a tip of $$$ for correct description. 
You will be penalized if you fail to follow instructions or examples

###Additional Guidance###
You MUST ensure that your outcomes are unbiased and avoids relying on stereotypes.
You MUST generate the content in a professional tone and educational exam question style.
You MUST not mention intended audience of the activity in the description.
You MUST also provide the correct answer along with the reasons.

##TOPICS: {}

## TEXT: 
{}

### Question Answers: 
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


# MODULE CODES 
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

# GCP_BUCKET_CONFIG: str = os.getenv("GCP_BUCKET")
# gcs_client = storage.Client.from_service_account_json(".secrets/intrepid-abacus-384710-df03a4dd7acc.json")
# gcs_client = storage.Client.from_service_account_info(GCP_BUCKET_CONFIG)

# Define a static bucket name
# BUCKET_NAME = "upload-file-ps"  # Replace with your actual bucket name
# bucket = gcs_client.bucket(BUCKET_NAME)

# LLMs for our application 
# URL: str = "https://project-astra-1086049785812.us-central1.run.app"
URL: str = "http:localhost:8000"

def decode_image(encoded_string: str) -> PIL.Image:
    image_data = base64.b64decode(encoded_string)
    buffered = BytesIO(image_data)
    image = PIL.Image.open(buffered)
    return image

def visualizer(items: List[str]) -> pd.DataFrame: 
    # this function converts a list of topics to semantic vectors 
    tokenized_list = [item.split() for item in items]
    model = Word2Vec(sentences=tokenized_list, vector_size=100, window=5, min_count=1, workers=4)
    
    word_vectors = []
    for word in items: 
        sentence_vector = np.zeros((100,)) 
        for token in word.split(" "): 
            sentence_vector += model.wv[token] 
        word_vectors.append(sentence_vector)

    # returns a dataframe to plot as a scatter plot 
    pca = PCA(n_components=2)

    #vectors 
    vectors = np.vstack(word_vectors)

    # Cluster labels
    cluster = KMeans(n_clusters=3)
    
     
    embeds = pca.fit_transform(vectors) 
    cluster_labels = cluster.fit_predict(embeds).astype(np.int8)

    df: pd.DataFrame = pd.DataFrame(embeds, columns=["x", "y"])
    df["labels"] = items 
    df["cluster_label"] = cluster_labels  
    return df  

def encode_image(image: PIL.Image): 
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def generate_response(
    prompt: str, 
    topics: List[str], 
    context: List[str], 
    hf_token: str
) -> str: 

    API_URL: str = "https://api-inference.huggingface.co/models/"

    headers: Dict[str, str] = {
        "Authorization": "Bearer {}".format(hf_token), 
        "X-use-cache": "true", 
        "Content-Type": "application/json",
        "X-wait-for-model": "true", 
    }

    json_input : Dict[str, str] = {
        "inputs": prompt.format(
            str(topics),
            "\n".join(context),  
        ), 
        "parameters": {"max_new_tokens": 3000, "temperature":0.1}
    }

    response = requests.post(
        API_URL + "mistralai/Mistral-7B-Instruct-v0.2", 
        headers=headers,
        json=json_input, 
    ).json()

    return (
        response[0]
        ["generated_text"]
        .split("Answers:")[1]
    )

# prompts for generation for different types of outputs 

short_question_answer_prompt: str = """
You are a Short Question Answer Generator Bot. Your goal is to generate Short 
Question Answers based on the following instructions.  

Definition: Short answer questions are typically composed of a brief prompt that demands a written answer that varies in length from one or two words to a few sentences.

###TASK###: You MUST create Short Answer Question based on the provided text and the topic to which they fall under. 

### OUTPUT FORMAT: 
Your output MUST be in the following format: 
<b>Q: [Your question]</b>
<p>A: [Your answer]</p> 

### Instructions###: 
  - Your own words – not statements straight out of the textbook
  - Specific problem and direct questions

###Incentives###
You will receive a tip of $$$ for correct description. 
You will be penalized if you fail to follow instructions or examples

###Additional Guidance###
You MUST ensure that your outcomes are unbiased and avoids relying on stereotypes.
You MUST generate the content in a professional tone and educational exam question style.
You MUST not mention intended audience of the activity in the description.
You MUST also provide the correct answer along with the reasons.

##TOPICS: {}

## TEXT: 
{}

### Question Answers:
"""
true_false_prompt: str = """
You are a True/ false Question Generator Bot. Your task is to create question as per instructions
 
 Definition: True/false questions are only composed of a statement. Students respond to the questions by indicating whether the statement is true or false. For example: True/false questions have only two possible answers (Answer: True).
 
 ###TASK###: You MUST create True/ False Question based on the provided text
 ### Instructions###: 
 Your task is to describe the details in the provided image. Describe the content in the foreground and the background. Foreground content may include pop-up, notification, alert or information box or button. Focus on details of the foreground content.The aspects to consider while describing foreground shall include the following: 
 Describe the layout . 
 Describe about placement of elements, such as headers, navigation menus, and content sections.
 Reflect on the design principles, such as the use of grids, alignment, and spacing.
 Describe the readability of the text, including font choice, size, color, and contrast against the background.
 Describe the typography across different sections and elements.
 Describe the overall color scheme for visual appeal and appropriateness for the target audience.
 Describe the visual hierarchy, with important elements standing out effectively.
 Describe images and icons including their size, quality, and relevant to the content.
 Describe the buttons including visibility, size, clarity and colour of buttons and interactive elements. Mention whether these buttons are distinguishable
 Describe the existence of navigation panes. Express how many navigation panes exist and describe each of them.
 Illustratively describe what is the proportion of onscreen content to the proportion of the content in the page based on the navigation pane
 
 ### Instructions###: 
  - Your own words – not statements straight out of the textbook
  - One central idea in each question
 ###Additional Guidance###
 You MUST ensure that your outcomes are unbiased and avoids relying on stereotypes.
 You MUST generate the content in a professional tone and educational exam question style.
 You MUST not mention intended audience of the activity in the description.
 You MUST also provide the correct answer along with the reasons.
  
 ###Incentives###
 You will receive a tip of $$$ for correct description. 
 You will be penalized if you fail to follow instructions or examples
 
##TOPICS: {}

## TEXT: 
{}

### Question Answers:
"""
fill_in_the_blanks_prompt = """

"You are a Fill in the blanks Question Generator Bot. Your task is to create question as per instructions
 
 Definition: Questions with blanks that can be filled in with one or two words in the sentence
 
 ###TASK###: You MUST create Fill in the blanks question based on the provided text
 
 ### Instructions###: 
  - Your own words – not statements straight out of the textbook
  - Specific problem and direct questions
  - Prompts that omit only one or two key words in the sentence
 ###Additional Guidance###
 You MUST ensure that your outcomes are unbiased and avoids relying on stereotypes.
 You MUST generate the content in a professional tone and educational exam question style.
 You MUST not mention intended audience of the activity in the description.
 You MUST also provide the key points that are essential in correct answer along with its reasons.
  
 ###Incentives###
 You will receive a tip of $$$ for correct description. 
 You will be penalized if you fail to follow instructions or examples
 
  
##TOPICS: {}

## TEXT: 
{}
### Questions And Answers:
"""
multiple_choice_prompt: str = """
You are a Multiple Choice Question Generator Bot. Your task is to create question as per instructions
 
 Definition: Multiple choice questions are composed of one question (stem) with multiple possible answers (choices), including the correct answer and several incorrect answers (distractors). Typically, students select the correct answer by circling the associated number or letter, or filling in the associated circle on the machine-readable response sheet.
 
 ###TASK###: You MUST create Multiple Choice Question based on the provided text
 
 ### Instructions###: 
  - Your own words – not statements straight out of the textbook
  - Single, clearly formulated problems
  - Statements based on common student misconceptions
  - True statements that do not answer the questions
  - Short options – and all same length
  - Correct options evenly distributed over A, B, C, etc.
  - At least 4 or 5 options for the user to select from
 ###Additional Guidance###
 You MUST ensure that your outcomes are unbiased and avoids relying on stereotypes.
 You MUST generate the content in a professional tone and educational exam question style.
 You MUST not mention intended audience of the activity in the description.
 You MUST also provide the correct answer along with the reasons.
  
 ###Incentives###
 You will receive a tip of $$$ for correct description. 
 You will be penalized if you fail to follow instructions or examples
 
##TOPICS: {}

## TEXT: 
{}

### Multiple Choice Questions And Answers:
"""
computational_questions_prompt: str = """
You are a Computational Question Generator Bot. Your task is to create question as per instructions
 
 Definition: Computational questions require that students perform calculations in order to solve for an answer. Computational questions can be used to assess student’s memory of solution techniques and their ability to apply those techniques to solve both questions they have attempted before and questions that stretch their abilities by requiring that they combine and use solution techniques in novel ways.
 
 ###TASK###: You MUST create Computational questions based on the provided text
 
 ### Instructions###: 
  - Your own words – not statements straight out of the textbook
  - Be solvable using knowledge of the key concepts and techniques from the course. Before the exam solve them yourself or get a teaching assistant to attempt the questions.
  - Indicate the mark breakdown to reinforce the expectations developed in in-class examples for the amount of detail, etc. required for the solution.
 ###Additional Guidance###
 You MUST ensure that your outcomes are unbiased and avoids relying on stereotypes.
 You MUST generate the content in a professional tone and educational exam question style.
 You MUST not mention intended audience of the activity in the description.
 You MUST also provide the correct answer along with the steps and workings.
  
 ###Incentives###
 You will receive a tip of $$$ for correct description. 
 You will be penalized if you fail to follow instructions or examples

##TOPICS: {}

## TEXT: 
{}

### Computational Code Questions And Answers:
"""
software_code_questions_prompt: str ="""
You are a Software writing Question Generator Bot. Your task is to create question as per instructions
 
Definition: Software writing questions"" refers to a set of inquiries designed to assess a person's understanding of the process of creating software, including aspects like coding, algorithms, data structures, software design principles, and problem-solving techniques, often used in technical interviews for software development roles.
 
###TASK###: You MUST create Software writing question based on the provided text
 
### Instructions###: 
  - Your own words – not statements straight out of the textbook
  - Focus on problem-solving: These questions usually present a real-world scenario that requires the candidate to design and implement a software solution, demonstrating their ability to break down complex problems into manageable steps.
  - Coding skills evaluation: Many software writing questions involve writing actual code snippets in a specific programming language to solve the given problem, assessing the candidate's syntax proficiency and coding style.
  - Algorithmic thinking: Questions might ask candidates to analyze the time and space complexity of different algorithms to choose the most efficient solution for a problem.
  - Design principles: Some questions might focus on software design patterns and best practices, asking candidates to explain how they would structure a complex system or handle specific scenarios.
  - Examples of software writing questions: ""Write a function to reverse a string."": (Assesses basic coding skills and understanding of string manipulation) or ""Design a data structure to store and efficiently retrieve the top 10 most frequently used words in a text file."": (Tests knowledge of data structures like hash tables and priority queues)
 ###Additional Guidance###
 You MUST ensure that your outcomes are unbiased and avoids relying on stereotypes.
 You MUST generate the content in a professional tone and educational exam question style.
 You MUST not mention intended audience of the activity in the description.
 You MUST also provide the correct answer along with the step by step code along with notes for the code.
  
 ###Incentives###
 You will receive a tip of $$$ for correct description. 
 You will be penalized if you fail to follow instructions or examples
 
##TOPICS: {}

## TEXT: 
{}

### Software code questions and Answers:
"""
prompts: Dict[str, str] = {
    "True/False": true_false_prompt,
    "Fill in the blanks": fill_in_the_blanks_prompt,
    "Short Question Answer": short_question_answer_prompt, 
    "Multiple Choice": multiple_choice_prompt,
    "Computational Questions": computational_questions_prompt,
    "Software Code Questions": software_code_questions_prompt 
}


# downloads secrets from the web ig
# def download_secrets(file_id : str) -> Dict[str, str] : 
#     URL: str  = f"https://drive.google.com/uc?id={file_id}" 

#     # get the string content 
#     content = requests.get(url=URL).content.decode("utf-8")
#     secrets: Dict[str, str] = {}
#     for items in content.split("\n"): 
#         if "=" in items: 
#             key_name, secret = items.split("=")
#             secrets[key_name] = secret 

#     return secrets 


# secret tokens
HF_TOKEN: str = os.getenv("HF_TOKEN") 

FIREBASE_CONFIG: Dict[str, str] = json.loads(os.getenv("FIREBASE_CLIENT")) 

BUCKET_NAME: str = os.getenv("BUCKET_NAME")

# initializing the bucket for data   
gcs_client = storage.Client.from_service_account_json('.secrets/gcp_bucket.json')
bucket = gcs_client.bucket(BUCKET_NAME)

# firebase config 
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()


@st.fragment
def generate_qna(json_df: pd.DataFrame, topics: List[str]): 
    selected_topics = st.multiselect("Topics", options=topics)

    qna_type: str = st.selectbox(
        "QNA Type", 
        options = list(prompts.keys()), 
    )

    topic_clicked = st.button("Filter and Generate")

    # getting the prompt for qna generation 
    # short_answer_prompt: str = prompts_repository["Short Answer Question"].to_list()[-2]
    # print(short_answer_prompt)
    if topic_clicked: 
        with st.spinner("Generating Question Answers..."): 
        # Using the sub domains obtained above to filter the dataframe  
            filtered_df: pd.DataFrame = json_df[json_df.apply(
                lambda x: any([ topic in x["major_domains"] + x["concepts"] + x["sub_domains"]
                            for topic in selected_topics]), axis=1)]

            texts: List[str] = filtered_df["text"].to_list()

            content: str = generate_response(
                prompts[qna_type], 
                topics=topics, 
                context=texts, 
                hf_token=HF_TOKEN, 
            )

            # content = requests.post(
            #     URL + "/generate", 
            #     json = {
            #         "context": " ".join(texts), 
            #         "topics": topics, 
            #         "question_type": qna_type, 
            #     }
            # ).json()

        st.write(content, unsafe_allow_html=True)


PROMPT_FILE_ID: str =  os.getenv("FILE_ID") # file_id to fetch remote prompt design sheet
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") # gemini api key 
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") # openai api key 
HF_TOKEN: str = os.getenv("HF_TOKEN") # huggingface token 

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
def create_user_folders(email: str):
    """Create the necessary folders for the user in the GCS bucket."""
    user_folder = email  # Use the user's email as the folder name

    # Define subfolder names
    subfolders = [
        "uploaded_document",
        "processed_image",
        "summaries", 
        "text_extract",
        "intermediate_json_data",
        "graph_data", 
        "json_data"
    ]

    for subfolder in subfolders:
        blob = bucket.blob(f"{user_folder}/{subfolder}/")  # Append a trailing slash to create a folder
        blob.upload_from_string('')

async def async_summarize(url: str, email_id: str, pdf_name: str, chapter_title: str) -> Dict: 
    async with aiohttp.ClientSession() as client: 
        async with client.post(url + "/summarize", json={
            "email_id":email_id, 
            "filename": pdf_name, 
            "chapter_title": chapter_title, 
        }) as response:  
            return await response.json()

async def async_summarize_multiple(pdf_name: str, email_id: str): 
    summarized_blob_path: str = f"{email_id}/summaries/{pdf_name}/" 
    # could cause a problem if the pdf already exists 
    blobs = gcs_client.list_blobs(
        BUCKET_NAME, 
        prefix=summarized_blob_path, 
        delimiter="/", 
    )

    return await asyncio.gather(
        *[asyncio.create_task(
            async_summarize(
                URL, pdf_name,
                email_id,  
                chapter_title=blob.name.split("/")[3], 
            )
        ) for blob in blobs if blob.name.endswith("_content.txt")]
    )
# If a file is uploaded
# @st.fragment
# def register() -> bool | None:
#     email = st.text_input("Email ID")
#     password = st.text_input("Password")
#     register_btn = st.button("Register!")

#     if register_btn: 
#         try: 
#             auth.create_user(email=email, password=password)
#             create_user_folders(email=email)

#             st.success("Congratulations! Now you're a Proud Project-Austrian!")
#             st.markdown("Please go to the login page and Authenticate yourself")
                
#         except Exception as e: 
#             st.write(":red[There was some issue registering you...]")
#             print(e)
#             return False 
        
        
#         if st.button("Go To Login"): 
#             return True 

# @st.fragment
# def login() -> bool | None :
#     email = st.text_input("Email ID") 
#     password = st.text_input("Password")
#     login_btn = st.button("Login!")
#     if login_btn: 
#         try: 
#             user = auth.get_user_by_email(email)
#             st.session_state[user.uid] = user.email 
#             cookies.set("session_id", user.uid)
#             return True  
            
#         except Exception as _: 

#             st.write(":red[User does not exist!] Register down below!")
#             reg = st.button("Register")
#             if reg: 
#                 return False  
#             else: 
#                 return None 

@st.fragment
def objective(): 
    st.title("Project Astra Demo")

    # File uploader component
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_pdf is not None:
        button : bool = st.button("Process PDF")
        if button: 
            # pushing the pdf to gcp
            pdf_blob_path: str = f"{st.session_state.email}/uploaded_document/{uploaded_pdf.name}"
            pdf_blob = bucket.blob(pdf_blob_path)

            with pdf_blob.open("wb") as pdf: 
                pdf.write(uploaded_pdf.getbuffer())
            
            with st.spinner("Parsing the file..."): 
                # takes the data loader model as an input 
                pdf2images = requests.post(
                    URL + "/convert_pdf", 
                    json={
                        "email_id": st.session_state.email, 
                        "uri": pdf_blob_path, 
                        "filename": uploaded_pdf.name 
                    }
                )
            
            
            with st.spinner("Converting HTML to Table..."): 
                # text_metadata: List[Dict[str, str| int | None]] = structure_html(html_pages)
                text_metadata = requests.post(
                    URL + "/data_loader", 
                    json=pdf2images.json()
                ).json()
            
            # the summarization docs have been created. 
            # next step is to summarize all the individual chapters 
            with st.spinner("Summarizing the docs paralelly..."): 
                #TODO: make all of this async 
                # asyncio.run(async_summarize_multiple(
                #     text_metadata["filename"], text_metadata["email_id"]
                # ))

                summarized_blob_path: str = f"{st.session_state.email}/summaries/{uploaded_pdf.name}/" 
                # could cause a problem if the pdf already exists 
                blobs = gcs_client.list_blobs(
                    BUCKET_NAME, 
                    prefix=summarized_blob_path, 
                    delimiter="/", 
                )
                
                for blob in blobs: 
                    if blob.name.endswith("_content.txt"):
                        requests.post(
                            URL + "/summarize", 
                            json = {
                                "email_id": st.session_state.email, 
                                "filename": uploaded_pdf.name, 
                                "chapter_title": blob.name.split("/")[3], 
                            }
                        )

            # Data classifier part 
            with st.spinner("Sending each text to the classifier..."): 
                for idx in range(text_metadata["page_count"]): 
                    requests.post(
                        URL + "/data_classifier", 
                        json={
                            "filename": uploaded_pdf.name, 
                            "email_id": st.session_state.email, 
                            "page_number": idx
                        }
                    )

            json_outputs: List[Dict] = []

            with st.spinner("Getting output json from the bucket..."): 
                classifier_blobs = gcs_client.list_blobs(
                    BUCKET_NAME, 
                    prefix=f"{st.session_state.email}/json_data/", 
                    delimiter="/", 
                )

                for blob in classifier_blobs: 
                    if uploaded_pdf.name in blob.name:
                        with blob.open("r") as f:
                            json_outputs.append(json.load(fp=f))  
                # json_outputs = requests.post(
                #     URL + "/data_classifier", 
                #     json=text_metadata.json()
                # )

            with st.spinner("Generating json..."): 
                json_df: pd.DataFrame = pd.DataFrame.from_records(json_outputs)


            # gets all unique sub-domains and then chooses three from it 
            # essentially a for loop to sum a list of lists and then get unique sub_domains 
            # out of it. Out of which we pick three at random. This code may be changed later.  
            
            # let's also include major domains and concepts as well  

            sub_domains: List[str] = list(set(sum(json_df["sub_domains"].to_list(), [])))  
            major_domains: List[str] =  list(set(sum(json_df["major_domains"].to_list(), []))) 
            concepts: List[str] = list(set(sum(json_df["sub_domains"].to_list(), [])))        

            topics: List[str] = sub_domains + major_domains + concepts 

            # Converting into embeddings  
            embeds_2d: pd.DataFrame = visualizer(topics)
            data = embeds_2d[["x", "y"]].values 
            labels = embeds_2d["labels"].values 

            with st.spinner("Rendering the image..."): 
                data = data * 50 
                
                # Mapplot on the app 
                # with tempfile.TemporaryDirectory() as tmp_dir: 
                # img_folder_blob = bucket.blob(f"{st.session_state.email}/datamapplots/")
                # img_folder_blob.upload_from_string('')
                
                # img_blob = bucket.blob(f"{st.session_state.email}/datamapplots/{uploaded_pdf.name}_topic_img.jpg")
                matplotlib_fig, _ = datamapplot.create_plot(
                    data[:50], labels[:50],
                    title="Visual Representation of the topics in the book.", 
                    label_over_points=True,
                    dynamic_label_size=True,
                    dynamic_label_size_scaling_factor=1.5,
                    max_font_size=24,
                    min_font_size=4,
                    min_font_weight=100,
                    max_font_weight=400,
                )

                st.pyplot(matplotlib_fig, bbox_inches="tight")

                # with img_blob.open("w") as f: 
                    


                    # fig.savefig(f"{tmp_dir}/saved_img.jpg")
                    # matplotlib_fig = PIL.Image.open(f"{tmp_dir}/saved_img.jpg") 
                # endpoint approach 

                # x_col = data[:, 0].tolist()
                # y_col = data[:, 1].tolist()
                # labels = labels.tolist()
                # print("We're here before posting...")

                # response_img = requests.post(
                #     URL + "/create_img", 
                #     json={
                #         "X_col": x_col[:20], 
                #         "Y_col": y_col[:20], 
                #         "labels": labels[:20],  
                #     }, 
                #     timeout=1000
                # )

                # print("Posting is done and successfull")

                # matplotlib_fig = decode_image(response_img.json()["encoded_image"]) 
                # st.image(matplotlib_fig, use_column_width=True)
                # print("Issue is in image rendering!")

            # figure = px.scatter(
            #     embeds_2d, x='x', y='y', 
            #     hover_data=['labels'], 
            # )

            # st.plotly_chart(figure)
            generate_qna(json_df, topics)

@st.fragment
def intro():  
    st.title("Welcome to :blue[Project Astra]!")
    st.write("<b>A Knowledge Graph Generation Project!</b>", unsafe_allow_html=True)
    st.markdown("""
    **Project Astra** is a groundbreaking initiative in **Knowledge Graph Generation**! 

    Our mission is to turn unstructured data into meaningful, interconnected knowledge, unlocking insights for smarter applications, intelligent analysis, and future-ready solutions.

    Whether you're a developer, researcher, or tech enthusiast, Project Astra brings the power of knowledge graphs closer to you. 

    Explore this new frontier and discover how structured data can transform the way we understand and interact with information.

    Let's turn data into wisdom, one node at a time.
    """)

@st.fragment
def password_reset():
    if st.session_state.email: 
        email = st.session_state.email
    else: 
        st.write(":red[You have not entered any email information for us...]")

    st.success(f"Verification Email Sent to ```{email}```.")
    st.markdown(f'''
    We have successfully sent a verification email to **{email}**.

    Please check your inbox and follow the instructions in the email to verify your account. If you don’t see the email in your inbox, check your spam or junk folder.

    > **Next Steps:**  
    > - Open the email sent to **{email}**.
    > - Click the verification link provided.
    > - Follow any further instructions to complete the verification process.

    Thank you for your patience!
    ''') 
    
page_to_func: Dict[str, str]  = {
    "Intro": intro, 
    "objective": objective, 
    "password_reset": password_reset, 
}

page: str = "Intro"
with st.sidebar: 
    choice = st.selectbox("Login/Register", options={
        "Login", 
        "Register"
    })

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    st.session_state.email = email

    if choice == "Login": 
        forgot_password = st.button("Forgot your password?")
        login_btn = st.button("Login!")

        if login_btn: 
            try: 
                user = auth.sign_in_with_email_and_password(email, password)
                page = "objective"
            except Exception as _: 
                st.write(":red[User does not exist!] Register yourself by changing the page!")
        elif forgot_password: 
            try: 
                auth.send_password_reset_email(email)
                page = "password_reset"
            except Exception as _:
                st.write(":red[You may want to go to the register page and register first...]")

    elif choice == "Register": 
        register_btn = st.button("register")
        
        if register_btn: 
            try: 
                auth.create_user_with_email_and_password(email=email, password=password)
                create_user_folders(email) 
            
                st.success("Congratulations! Now you're a Proud Project-Austrian!")
                st.markdown("Please go to the login page and Authenticate yourself")
                st.balloons()
                page = "Intro"

            except Exception as E: 

                st.write(":red[There was some issue registering you... Maybe you are already registered? Try the login page]")
                print(E)

                
page_to_func[page]()
# writing the code for login and redirection             

# choice = st.selectbox("Login/Register", options=["Login", "Register"])
# if choice == "Login": 
#     status = login() # true, false or None 
#     # if it is true, the user is authenticated and should be sent to the project-astra page

#     if status:
#         objective()

#     # the user has clicked the register button 
#     elif isinstance(status, bool): 
#         if register(): 
#             login()
# else: 
#     if register(): 
#         login()
# print(dict(cookies)) 
