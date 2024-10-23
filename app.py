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
URL: str = ""
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


@st.fragment
def generate_qna(json_df: pd.DataFrame): 
    selected_topics = st.multiselect("Topics", options=topics)
    topic_clicked = st.button("Filter")

    qna_type: str = st.selectbox(
        "QNA Type", 
        options = [
            
        ]
    )
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
            # content: str = generate_response(
            #     short_question_answer_prompt, 
            #     topics=sub_domains, 
            #     context=texts, 
            #     hf_token=HF_TOKEN, 
            #     model="mistral", 
            # )

            content = requests.post(
                URL + "/generate", 
                json = {
                    "context": " ".join(texts), 
                    "topics": topics, 
                    "question_type": qna_type, 
                }
            ).json()

            content = content["output"]

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

            
            