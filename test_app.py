import streamlit as st 
import os 
import json 

from google.cloud import storage
from typing import Dict, List, Set
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
You are a Fill in the blanks Question Generator Bot. Your task is to create question as per instructions
You are expected to create questions in the language in which the content is presented to you.
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


gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
# bucket 
bucket = gcs_client.bucket(BUCKET_NAME)

# firebase login 
FIREBASE_CONFIG: Dict[str, str] = json.loads(os.getenv("FIREBASE_CLIENT")) 

# firebase config 
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()


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
    
    print(f"Currently at data_loading and processing state for {pdf_name}...") 
    data_loader_response = requests.post(
        URL + "/data_loader", 
        json = convert_output, 
    )

    print(f"Currently at summarizing stage for pdf {pdf_name}...")
    data_loader_output: Dict = data_loader_response.json()

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
                    "chapter_title": blob.name.split("/")[3], 
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
        # TODO: Use groq api for this generation  
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

        st.download_button(label="Download QNA", data=content, file_name="qna.txt", mime="text/plain")

@st.fragment
def run_process(book_name: str): 
    
    if st.button("Select book"): 
        with st.spinner("Loading data..."): 
        # st.session_state.page = "pdf_project_page"
            classifier_blobs = gcs_client.list_blobs(
                BUCKET_NAME, 
                prefix=f"{st.session_state.email}/json_data/", 
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
            
            st.markdown(
                f"Click on this link to view the interactive plot: [{book_name}]({URL}/interactive_plot/{st.session_state.email}/{book_name})")

            # running the endpoint asynchronously 
            generate_qna(json_df, topics)

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
            prefix=f"{st.session_state.email}/uploaded_document/", 
            delimiter="/"
        )

        blob_names: List[str] = [blob.name.split("/")[-1] for blob in existent_blobs]
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
        "intermediate_json_data",
        "graph_data", 
        "json_data"
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



