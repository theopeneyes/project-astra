import os 
import json 
import streamlit as st 
import asyncio

from google.cloud import storage

from dotenv import load_dotenv
import pyrebase
import aiohttp
import pandas as pd 
import requests
import threading 


load_dotenv()

BUCKET_NAME: str = os.getenv("BUCKET_NAME")  
NODE_SERVER_URL: str = "http://127.0.0.1:5173"
URL: str = "http://127.0.0.1:8000"

gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")

# bucket 
bucket = gcs_client.bucket(BUCKET_NAME)

# firebase login 
FIREBASE_CONFIG: dict[str, str] = json.loads(os.getenv("FIREBASE_CLIENT")) 

# firebase config 
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()


prompts = [ 
    "True/False",
    "Fill in the blanks",
    "Short Question Answer",
    "Multiple Choice",
    "Computational Questions",
    "Software Code Questions",
]




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

async def process_pdf(pdf_name: str, user_email: str, base_directory: str): 
    filename = f"{base_directory}/{pdf_name}"    
    async with aiohttp.ClientSession() as session:
        with open(filename, 'rb') as pdf_file:
            form_data = aiohttp.FormData()
            form_data.add_field('email_id', user_email)
            form_data.add_field('filename', pdf_name)
            form_data.add_field('pdf', pdf_file, filename=pdf_name, content_type='application/pdf')

            async with session.post(URL + "/upload_pdf", data=form_data) as response:
                if response.status_code == 200: 
                    await response.json()
                else: 
                    return 

    async with session.post(URL + "/run_subprocess", json = {"email_id": pdf_name, "filename": pdf_name}) as response: 
        if response.status_code == 200: 
            await response.json()
        else: 
            return 

@st.fragment
def generate_qna(filename: str, language: str): 

    generation_clicked = st.button("Generate selected Question Answers!")

    html_blobs: list = gcs_client.list_blobs(
        BUCKET_NAME, 
        prefix=f"{st.session_state.email}/generated_content/{st.session_state.book_name}/", 
        delimiter="/"
    )

    if generation_clicked: 
        filepaths: list = []
        for html_blob in html_blobs: 
            names: list[str] = html_blob.name.split("/")[-1].split("_")
            names[1] = names[1].replace(" ", "_")
            names[2] = names[2].replace(" ", "_")

            filepaths.append([
                names[0].replace("_", " "), 
                names[1].replace("_", " "), 
                names[2].replace("_", " ").split(".html")[0], 
                os.path.join(
                    URL, 
                    "generation_output",
                    st.session_state.email, 
                    st.session_state.book_name, 
                    names[0], 
                    names[1], 
                    names[2], 
                )
            ])
        
        df = pd.DataFrame(filepaths, columns=["Question Type", "Chapter Name", "Topic Name", "Generated Answers Link"])
        st.dataframe(
            df,
            column_config={
                "Generated Answers Link": st.column_config.LinkColumn(label="🔗") 
            },
        )

        try: 
            generation_recipe_blob = bucket.blob(os.path.join(
                st.session_state.email, 
                "generation_data",
                f"{filename}.json", 
            ))

            with generation_recipe_blob.open("r") as f: 
                generation_recipe: dict = json.load(fp=f)
            
            for question_type, chapter_map in generation_recipe.items(): 
                with st.spinner(f"Generating {question_type} Question Answers..."): 
                    for chapter_name, topic_map in chapter_map.items(): 
                        for topic_name in topic_map.keys(): 

                            response = requests.post(
                                URL + "/generate", 
                                json = {
                                    "email_id": st.session_state.email, 
                                    "filename": filename, 
                                    "question_type": question_type,
                                    "topic_name": topic_name,  
                                    "chapter_name": chapter_name,  
                                    "language": language  
                                }
                            )


                        
                            if response.status_code != 200: 
                                print(f"Question Type: {question_type}, Chapter name: {chapter_name}, Topic Name: {topic_name}")
            
            
        except Exception as e: 
            print(e)
            print("No such blob exists! Please select the question and answers within the generated book tree!")

def run_process(book_name: str): 
    if st.button("Select book"): 

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

async def run_async(pdf_names: list[str], user_email: str, base_directory):
    await asyncio.gather(
        *[ asyncio.create_task(
            process_pdf(pdf_name, user_email, base_directory)
        ) for pdf_name in pdf_names]
    )


def parse_pdfs(directory_path: str, pdfs: list[str], user_email: str): 
    asyncio.run(run_async(
        [pdf_name
         for pdf_name in pdfs], user_email, directory_path 
    ))

@st.fragment
def select_book(blob_names: list[str], directory_path: str, non_existent_pdfs: str) -> str: 
    book_name = st.selectbox(
        label="Select one of the following pdfs...",
        options=blob_names)

    with st.spinner("Are we waiting for it?..."):         
        thread = threading.Thread(target=parse_pdfs, args=(directory_path, 
                                non_existent_pdfs, st.session_state.email)) 
        thread.start()

    st.session_state.book_name = book_name
    if book_name: 
        run_process(book_name)

@st.fragment
def run_main(): 
    directory_path: str = st.text_input("Enter directory path:")
    select_dir = st.button("Choose")
    if select_dir: 
        pdfs = set(os.listdir(directory_path)) 

        request = requests.post(
            URL + "/get_all_processed_books", 
            json = {
                "email_id": st.session_state.email_id,  
            },  

        )
        if request.status_code == 200: 
            response_dict = request.json()
            blob_names = response_dict["book_list"]
        

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
    page_to_func: dict[str, str]  = {
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



