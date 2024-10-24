import tempfile 
import os

import pandas as pd 
from typing import List

from gensim.models import Word2Vec
from io import BytesIO
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 

import requests 

import PIL 

import base64

from dotenv import load_dotenv

import pandas as pd 
import streamlit as st
import numpy as np 
import plotly.express as px 


load_dotenv()

# LLMs for application 
URL: str = "https://project-astra-1086049785812.us-central1.run.app"

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
    hf_token: str, 
    model: str) -> str: 

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

from typing import Dict 
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


FILE_ID: str = '1kTXuGtEUyZDrb4g7-2MxiXBgWW9WBaJT'
# downloads secrets from the web ig
def download_secrets(file_id : str) -> Dict[str, str] : 
    URL: str  = f"https://drive.google.com/uc?id={file_id}" 

    # get the string content 
    content = requests.get(url=URL).content.decode("utf-8")
    secrets: Dict[str, str] = {}
    for items in content.split("\n"): 
        if "=" in items: 
            key_name, secret = items.split("=")
            secrets[key_name] = secret 

    return secrets 


secrets: str = download_secrets(FILE_ID)
HF_TOKEN: str = secrets.get("HF_TOKEN")

@st.fragment
def generate_qna(json_df: pd.DataFrame): 
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

            print(f"The content is ... {texts}")
            content: str = generate_response(
                prompts[qna_type], 
                topics=sub_domains, 
                context=texts, 
                hf_token=HF_TOKEN, 
                model="mistral", 
            )

            # content = requests.post(
            #     URL + "/generate", 
            #     json = {
            #         "context": " ".join(texts), 
            #         "topics": topics, 
            #         "question_type": qna_type, 
            #     }
            # ).json()

            print(f"The content in response here: {content}")

        st.write(content, unsafe_allow_html=True)

# Application code starts here. We can also replace the above code with endpoints once they are deployed. 

# Streamlit UI
st.title("Project Astra Demo")

# File uploader component
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

# If a file is uploaded
if uploaded_pdf is not None:
    button : bool = st.button("Process PDF")
    if button: 
        with tempfile.TemporaryDirectory() as temp_dir: 
            file_path = os.path.join(temp_dir, uploaded_pdf.name)

            #TODO: Change this into a request sent to a server 
            with open(file_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())
            
            with st.spinner("Parsing the file..."): 
                # html_pages: List[str] = parse_pdf(
                #     config, st, 
                #     file_path, prompt, clause_prompt, 
                #     uploaded_pdf.name, ERROR_DIR, messages)

                pdf2images = requests.post(
                    URL + "/convert_pdf", 
                    files = {
                        "pdf_file": (uploaded_pdf.name, uploaded_pdf.getbuffer(), "application/pdf"), 
                    }
                )
            
            
            with st.spinner("Converting HTML to Table..."): 
                # text_metadata: List[Dict[str, str| int | None]] = structure_html(html_pages)
                text_metadata = requests.post(
                    URL + "/data_loader", 
                    json=pdf2images.json()
                )

            # Data classifier part 
            with st.spinner("Sending each text to the classifier..."): 
                # json_outputs: List[Dict] = []
                # msg: str = "Sending HTMLs to be converted to JSON..."

                # progress_bar = st.progress(0, text=msg)
            
                # for idx, text_json in enumerate(text_metadata): 
                #     if idx == len(text_metadata): 
                #         msg = "Processing JSON from HTML has finished!"
                #     progress_bar.progress((idx+1) / len(text_metadata), text=msg)
                #     op = get_json(text_json, HF_TOKEN)
                #     if op != "":    
                #         json_outputs.append(op) 
                json_outputs = requests.post(
                    URL + "/data_classifier", 
                    json=text_metadata.json()
                )

            with st.spinner("Generating json..."): 
                json_df: pd.DataFrame = pd.DataFrame.from_records(json_outputs.json())

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
            figure = px.scatter(
                embeds_2d, x='x', y='y', 
                color='cluster_label', hover_data=['labels'], 
            )

            st.plotly_chart(figure)
            generate_qna(json_df)

            
            