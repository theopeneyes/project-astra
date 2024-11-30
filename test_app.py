import streamlit as st 
import os 
import json 

from google.cloud import storage
from typing import Dict, List 

from dotenv import load_dotenv
import requests
import pyrebase
import asyncio 
import threading 

load_dotenv()

BUCKET_NAME: str = os.getenv("BUCKET_NAME") # name of the bucket 
PROMPT_FILE_ID: str =  os.getenv("FILE_ID") # file_id to fetch remote prompt design sheet
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") # gemini api key 
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") # openai api key 
HF_TOKEN: str = os.getenv("HF_TOKEN") # huggingface token 
NODE_SERVER_URL: str = "http://127.0.0.1:5173"
URL: str = "http://127.0.0.1:8000"

gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
# bucket 
bucket = gcs_client.bucket(BUCKET_NAME)

# firebase login 
FIREBASE_CONFIG: Dict[str, str] = json.loads(os.getenv("FIREBASE_CLIENT")) 

# firebase config 
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()


prompts: List[str] = [ 
    "True/False",
    "Fill in the blanks",
    "Short Question Answer",
    "Multiple Choice",
    "Computational Questions",
    "Software Code Questions",
]

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

            # topic extraction 
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
                    "branch_name": "topic" 
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
                    "branch_name": "topic" 
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
                    "branch_name": "topic" 
                }
            )


            # concept extraction 
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
                    "branch_name": "concept" 
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
                    "branch_name": "concept" 
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
                    "branch_name": "concept" 
                }
            )

            # heading extraction 
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
                    "branch_name": "heading_text" 
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
                    "branch_name": "heading_text" 
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
                    "branch_name": "heading_text" 
                }
            )
    
    
    print("Preprocessing the data for the graph...")    
    # putting it all in one directory  
    requests.post(
        URL + "/preprocess_for_graph", 
        json = {
            "filename": pdf_name, 
            "email_id": user_email, 
        } 
    )

    print("Segregating the json by topics, headings and concepts....")
    requests.post(
        URL + "/segregate", 
        json = {
            "filename": pdf_name, 
            "email_id": user_email, 
        } 
    )

    print("Getting topic relevant count") 
    requests.post(
        URL + "/modify_branch", 
        json = {
           "filename": pdf_name, 
           "email_id": user_email,  
           "branch_name": "topic"
        }
        
    )


    print("Getting concept relevant count") 
    requests.post(
        URL + "/modify_branch", 
        json = {
           "filename": pdf_name, 
           "email_id": user_email,  
           "branch_name": "concept"
        }
        
    )

    print("Getting heading relevant count") 
    requests.post(
        URL + "/modify_branch", 
        json = {
           "filename": pdf_name, 
           "email_id": user_email,  
           "branch_name": "heading_text"
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
def generate_qna(filename: str, language: str,): 
    generation_clicked = st.button("Generate selected Question Answers!")
    if generation_clicked: 
        # reach for the selected json by the user 
        try: 
            generation_recipe_blob = bucket.blob(os.path.join(
                st.session_state.email, 
                "generation_data",
                f"{filename}.json", 
            ))

            with generation_recipe_blob.open("r") as f: 
                generation_recipe: Dict = json.load(fp=f)
            
            filepaths: List = []
        
            for question_type, chapter_map in generation_recipe.items(): 
                for chapter_name, topic_map in chapter_map.items(): 
                    for topic_name in topic_map.keys(): 
                        response = requests.post(
                            URL + "/generate", 
                            json = {
                                "email_id": st.session_state.email, 
                                "filename": filename, 
                                "question_type": question_type,
                                "topic_name": chapter_name,  
                                "chapter_name": topic_name,  
                                "language": language  
                            }
                        )
                        
                        if response.status_code != 200: 
                            print(f"Question Type: {question_type}, Chapter name: {chapter_name}, Topic Name: {topic_name}")
                            filepaths.append(
                                f"/generation_output/{st.session_state.email}/{question_type}/{chapter_name}/{topic_name}"
                            )
                        
        except Exception as e: 
            print(e)
            print("No such blob exists! Please select the question and answers within the generated book tree!")

@st.fragment
def run_process(book_name: str): 
    if st.button("Select book"): 
        # with st.spinner("Loading data..."): 
        # # st.session_state.page = "pdf_project_page"
        #     classifier_blob = bucket.blob(
        #         f"{st.session_state.email}/final_json/{book_name}.json",
        #     )

        #     with classifier_blob.open("r") as f: 
        #         json_outputs = json.load(fp=f)
            
        #     json_df: pd.DataFrame = pd.DataFrame.from_records(json_outputs)
    
        # # gets all unique sub-domains and then chooses three from it 
        # # essentially a for loop to sum a list of lists and then get unique sub_domains 
        # # out of it. Out of which we pick three at random. This code may be changed later.  

        # # let's also include major domains and concepts as well 
        # # st.json(json_outputs)
        # # st.dataframe(json_df)
        # # print(json_df["sub_domains"].to_list()) 
        # # print(type(json_df["sub_domains"].to_list())) 
        # json_df["sub_domains"] = json_df.sub_domains.apply(lambda x: str(x))
        # json_df["major_domains"] = json_df.sub_domains.apply(lambda x: str(x))
        # json_df["concept"] = json_df.sub_domains.apply(lambda x: str(x))

        # sub_domains: List[str] = list(set(json_df["sub_domains"].to_list()))   
        # major_domains: List[str] =  list(set(json_df["major_domains"].to_list())) 
        # concepts: List[str] = list(set(json_df["concept"].to_list()))         
        
        # topics: List[str] = sub_domains + major_domains + concepts 
        

        # # Converting into embeddings  
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
            f"Click on this link to view the JSON Tree: [{book_name}]({NODE_SERVER_URL}/{st.session_state.email}/{book_name})")
        
        
        # running the endpoint asynchronously 
        generate_qna(book_name, text_language)

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
        "books", 
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



