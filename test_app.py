import streamlit as st 
import os 
import json 

from google.cloud import storage
from typing import Dict, List 

import pandas as pd 
from dotenv import load_dotenv
import datamapplot
from chart_utils.preprocess_chart import visualizer
import requests
import tempfile 
import pyrebase
import asyncio 
import threading 

load_dotenv()

BUCKET_NAME: str = os.getenv("BUCKET_NAME") # name of the bucket 
PROMPT_FILE_ID: str =  os.getenv("FILE_ID") # file_id to fetch remote prompt design sheet
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") # gemini api key 
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") # openai api key 
HF_TOKEN: str = os.getenv("HF_TOKEN") # huggingface token 
URL: str = "http://127.0.0.1:8000"

gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
# bucket 
bucket = gcs_client.bucket(BUCKET_NAME)

# firebase login 
FIREBASE_CONFIG: Dict[str, str] = json.loads(os.getenv("FIREBASE_CLIENT")) 

# firebase config 
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()


prompts: List[str] = {
    "True/False",
    "Fill in the blanks",
    "Short Question Answer",
    "Multiple Choice",
    "Computational Questions",
    "Software Code Questions",
}

async def process_pdf(pdf_name: str, user_email: str, base_directory: str): 
    with open(os.path.join(base_directory, pdf_name), "rb") as fr: 
        pdf_blob = bucket.blob(f"{user_email}/uploaded_document/{pdf_name}")
        with pdf_blob.open("wb") as f:
            f.write(fr.read())

    
    # Asking the endpoint to convert the pdf
    print(f"Currently at converting stage for pdf {pdf_name}...")
    convert_response = requests.post(
        URL + "/convert_pdf", json = {
            "email_id": user_email, 
            "uri": f"{user_email}/uploaded_document/{pdf_name}", 
            "filename": pdf_name,  
        })
    
    convert_output : Dict = convert_response.json()

    print("Detecting the language in which the book is written")
    language_response = requests.post(
        URL + "/detect_lang", 
        json = {
            "email_id": user_email, 
            "filename": pdf_name, 
        }
    )

    text_language: str = language_response.json()["detected_language"]
    print(text_language)
    
    print(f"Currently at data_loading and processing state for {pdf_name}...") 
    requests.post(
        URL + "/data_loader", 
        json = {
            "filename": pdf_name, 
            "email_id": user_email, 
            "uri": convert_output["uri"], 
            "language": text_language
        }, 
    )

    print(f"Currently at summarizing stage for pdf {pdf_name}...")

    # generating summary 
    summarized_blob_path: str = f"{user_email}/summaries/{pdf_name}/" 

    # could cause a problem if the pdf already exists 
    blobs = gcs_client.list_blobs(
        BUCKET_NAME, 
        prefix=summarized_blob_path, 
        delimiter="/", 
    )

    print(f"Storing summary blobs for pdf {pdf_name}...")
    for blob in blobs: 
        if blob.name.endswith("_content.txt"):
            requests.post(
                URL + "/summarize", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "chapter_title": blob.name.split("/")[3].split("_content")[0], 
                    "language": text_language, 
                }
            )
            
            requests.post(
                URL + "/summary_classifier", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "chapter_name": blob.name.split("/")[3].split("_content")[0], 
                    "language": text_language, 
                }
            )
    
    print("Classified our data and rewriting it within intermediate_json folder")
    text_extract_blob = gcs_client.list_blobs(
        BUCKET_NAME, 
        prefix=f"{user_email}/text_extract/", 
        delimiter="/"
    )

    for paragraph_node_blob in text_extract_blob:
        if pdf_name in paragraph_node_blob.name: 
            requests.post(
                URL + "/rewrite_json", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": int(paragraph_node_blob.name
                                .split("/")[-1]
                                .split("_")[-1]
                                .split(".")[0]
                            ), 
                    "language": text_language, 
                }
            )


            requests.post(
                URL + "/synthesize/strength/representational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": int(paragraph_node_blob.name
                                .split("/")[-1]
                                .split("_")[-1]
                                .split(".")[0]
                            ), 
                }
            )


            requests.post(
                URL + "/synthesize/strength/relational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": int(paragraph_node_blob.name
                                .split("/")[-1]
                                .split("_")[-1]
                                .split(".")[0]
                            ), 
                }
            )

            requests.post(
                URL + "/synthesize/depth/representational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": int(paragraph_node_blob.name
                                .split("/")[-1]
                                .split("_")[-1]
                                .split(".")[0]
                            ), 
                }
            )
    
    
    
    # putting it all in one directory  
    requests.post(
        URL + "/preprocess_for_graph", 
        json = {
            "filename": pdf_name, 
            "email_id": user_email, 
        } 
    )
        
    # print(f"Generating a classified output for pdf {pdf_name}...")
    # for idx in range(data_loader_output["page_count"]):  
    #     requests.post(
    #         URL + "/data_classifier", 
    #         json = {
    #             "filename": pdf_name, 
    #             "email_id": user_email, 
    #             "page_number": idx,  
    #         }
    #     )

async def run_async(pdf_names: List[str], user_email: str, base_directory: str):
    await asyncio.gather(
        *[ asyncio.create_task(
            process_pdf(pdf_name, user_email, base_directory)
        ) for pdf_name in pdf_names]
    )

# client 
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
def generate_qna(json_df: pd.DataFrame, topics: List[str], language: str): 
    selected_topics = st.multiselect("Topics", options=topics)

    qna_type: str = st.selectbox(
        "QNA Type", 
        options = prompts, 
    )

    topic_clicked = st.button("Filter and Generate")

    # getting the prompt for qna generation 
    # short_answer_prompt: str = prompts_repository["Short Answer Question"].to_list()[-2]
    # print(short_answer_prompt)
    if topic_clicked: 
        with st.spinner("Generating Question Answers..."): 
        # Using the sub domains obtained above to filter the dataframe  
        # TODO: Use groq api for this generation  
            json_df.dropna(inplace=True)
            filtered_df: pd.DataFrame = json_df[json_df.apply(
                lambda x: any([ topic in x["major_domains"] + x["concept"] + x["sub_domains"]
                            for topic in selected_topics]), axis=1)]


            texts: List[str] = filtered_df["text"].to_list()
            topics = [topic for topic in topics if isinstance(topic, str)]

            response = requests.post(
                URL + "/generate", 
                json = {
                    "topics": topics, 
                    "context": " ".join(texts), 
                    "question_type": qna_type, 
                    "language": language  
                }
            )
            content = response.json()["output"]
            # content: str = generate_response(
            #     prompts[qna_type], 
            #     topics=topics, 
            #     context=texts, 
            #     hf_token=HF_TOKEN, 
            # )

            # content = requests.post(
            #     URL + "/generate", 
            #     json = {
            #         "context": " ".join(texts), 
            #         "topics": topics, 
            #         "question_type": qna_type, 
            #     }
            # ).json()

        st.write(content, unsafe_allow_html=True)

        st.download_button(label="Download QNA", data=content, file_name="qna.txt", mime="text/plain")

# def generate_unique_values(items: List[str| List[str]]) -> List[str]: 
#     unique_values: List[str] = [] 
#     for item in items: 
#         if isinstance(item, str): 
#             unique_values.append(unique_values)
#         elif isinstance(item, list): 
#             unique_values = unique_values + item
    
#     return list(set(unique_values)) 

@st.fragment
def run_process(book_name: str): 
    if st.button("Select book"): 
        with st.spinner("Loading data..."): 
        # st.session_state.page = "pdf_project_page"
            classifier_blobs = gcs_client.list_blobs(
                BUCKET_NAME, 
                prefix=f"{st.session_state.email}/intermediate_json/", 
                delimiter="/", 
            )

            json_outputs : List[Dict] = [] 
            for blob in classifier_blobs: 
                if book_name in blob.name: 
                    with blob.open("r") as f: 
                        json_outputs.append(json.loads(f.read()))
            
            json_df: pd.DataFrame = pd.DataFrame.from_records(json_outputs)

        # gets all unique sub-domains and then chooses three from it 
        # essentially a for loop to sum a list of lists and then get unique sub_domains 
        # out of it. Out of which we pick three at random. This code may be changed later.  

        # let's also include major domains and concepts as well 
        # st.json(json_outputs)
        # st.dataframe(json_df)
        # print(json_df["sub_domains"].to_list()) 
        # print(type(json_df["sub_domains"].to_list())) 
        sub_domains: List[str] = list(set(json_df["sub_domains"].to_list()))   
        major_domains: List[str] =  list(set(json_df["major_domains"].to_list())) 
        concepts: List[str] = list(set(json_df["concept"].to_list()))         
        
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
            matplotlib_fig = datamapplot.create_interactive_plot(
                data[:50], labels[:50],
                title="Visual Representation of the topics in the book.", 
                font_family="Playfair Display SC",
            )


            with tempfile.TemporaryDirectory() as tmp_dir: 
                matplotlib_fig.save(f"{tmp_dir}/{book_name}.html")
                html_folder = bucket.blob(f"{st.session_state.email}/rendered_html/")
                html_folder.upload_from_string('')
                
                html_file = bucket.blob(f"{st.session_state.email}/rendered_html/{book_name}.html")
                with html_file.open("w") as f: 
                    with open(f"{tmp_dir}/{book_name}.html") as html: 
                        f.write(html.read())
            
            with st.spinner("Detecting the lanugage within the book..."): 
                language_response = requests.post(
                    URL + "/detect_lang", 
                    json = {
                        "email_id": st.session_state.email, 
                        "filename": book_name, 
                    }
                )

                text_language: str = language_response.json()["detected_language"]

            st.markdown(
                f"Click on this link to view the interactive plot: [{book_name}]({URL}/interactive_plot/{st.session_state.email}/{book_name})")
            
            
            # running the endpoint asynchronously 
            generate_qna(json_df, topics, text_language)

def parse_pdfs(directory_path: str, pdfs: List[str], user_email: str): 
    asyncio.run(run_async(
        [pdf_name
         for pdf_name in pdfs], user_email, directory_path 
    ))

@st.fragment
def select_book(blob_names: List[str], directory_path: str, non_existent_pdfs: str): 
    book_name = st.selectbox(
        label="Select one of the following pdfs...",
        options=blob_names)

    with st.spinner("Are we waiting for it?..."):         
        thread = threading.Thread(target=parse_pdfs, args=(directory_path, 
                                non_existent_pdfs, st.session_state.email)) 
        thread.start()

    if book_name: 
        run_process(book_name)
        # asyncio.run(run_async(
        #     *[os.path.join(directory_path, pdf) for pdf in non_existent_pdfs], 
        # ))

@st.fragment
def run_main(): 
    directory_path: str = st.text_input("Enter directory path:")
    select_dir = st.button("Choose")
    if select_dir: 
        pdfs = set(os.listdir(directory_path)) 

        existent_blobs = gcs_client.list_blobs(
            BUCKET_NAME, 
            prefix=f"{st.session_state.email}/final_json/", 
            delimiter="/"
        )

        blob_names: List[str] = [blob.name.split("/")[-1].split(".json")[0]
                                 for blob in existent_blobs]

        non_existent_pdfs = list(pdfs - set(blob_names))

        # documents that are ready... 
        select_book(blob_names[1:], directory_path, non_existent_pdfs)

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

def create_user_folders(email: str):
    """Create the necessary folders for the user in the GCS bucket."""
    user_folder = email  # Use the user's email as the folder name

    # Define subfolder names
    subfolders = [
        "uploaded_document",
        "processed_image",
        "summaries", 
        "text_extract",
        "intermediate_json",
        "graph_data", 
        "final_json"
    ]

    for subfolder in subfolders:
        blob = bucket.blob(f"{user_folder}/{subfolder}/")  # Append a trailing slash to create a folder
        blob.upload_from_string('')

with st.sidebar:
    page_to_func: Dict[str, str]  = {
        "intro": intro, 
        "objective": run_main, 
        "password_reset": password_reset, 
    }

    page = "intro"
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
                    page = "intro"

                except Exception as E: 
                    st.write(":red[There was some issue registering you... Maybe you are already registered? Try the login page]")
                    print(E)

page_to_func[page.lower()]()



