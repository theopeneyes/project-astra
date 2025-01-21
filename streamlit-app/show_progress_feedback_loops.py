import streamlit as st
import pandas as pd 

import os
import json
import re

from google.cloud import storage
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_ID = "test.fifth@yahoo.com"  # Replace with dynamic user email if needed

# Initialize GCS client
gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

with st.sidebar:
    # App Introduction Section
    with st.expander("What does this app do?"):
        st.markdown("""
        ## Welcome to the Summary Feedback Viewer!
        This application allows you to refine and analyze summaries of book chapters.
        
        **Key Features:**
        - **Load Chapter Content**: Select a chapter and view the full text along with the generated summary.
        - **Refine Summary**: Refine the generated summary to ensure it captures all relevant points.
        - **Identify Differences**: Compare the generated and refined summaries, and identify the differences.
        - **Issue Classification**: Automatically classify any issues into **Principle Issues** or **Nuanced Issues**.
        
        Use the controls below to interact with the app and explore summaries for different chapters.
        """)

if "chapters_fetched" not in st.session_state: 
    chapter_csv_blob = bucket.blob(os.path.join(
        EMAIL_ID, 
        "book_sections", 
        "lbdl", 
        "chapters.csv"
    ))

    with chapter_csv_blob.open("r") as fp: 
        df = pd.read_csv(fp)
        chapters = df[['title', 'section_number']].values.tolist()
        items = []
        for title, section_number in chapters: 

            if not section_number:
                section_number = 'nan'
            try: 
                section_number: int = int(section_number)
            except Exception as e: 
                pass 

            items.append(f'{section_number}_{title}')
        st.session_state.chapters_fetched = items  

# Streamlit App
st.title("Summary Feedback Viewer")
col1, col2 = st.columns(2)
# Input for book name
with col1: 
    BOOK_NAME = st.text_input("Enter the book name", "lbdl")
with col2: 
    chapter_name = st.selectbox(
        "Select Chapter",
        st.session_state.chapters_fetched,
        index=0  # You can change this index based on your requirement
    )


# Functions
def get_blob_content(bucket, blob_path):
    blob = bucket.blob(blob_path)
    with blob.open("r") as fp:
        return fp.read()

def refine_summary(api_key, messages):
    gpt_client = OpenAI(api_key=api_key)
    completions = gpt_client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        temperature=0.01
    )
    return completions.choices[0].message.content

def extract_refined_summary(html_response):
    match = re.findall("<refined_summary>(.*?)</refined_summary>", html_response, re.DOTALL)
    return match[0] if match else None

def identify_differences(api_key, messages):
    gpt_client = OpenAI(api_key=api_key)
    completions = gpt_client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        temperature=0.01
    )
    return completions.choices[0].message.content

def issue_classifier(api_key, differences):
    gpt_client = OpenAI(api_key=api_key)
    
    # Create new messages for issue classification
    messages = [
        {"role": "system", "content": "Generate your answer in English language."},
        {"role": "user", "content": issue_classification_prompt.format(differences)}
    ]
    
    completions = gpt_client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
        temperature=0.01
    )

    html_response = completions.choices[0].message.content

    if re.findall(r"<issue>(.*?)</issue>", html_response, re.DOTALL):  
        issue = re.findall(r"<issue>(.*?)</issue>", html_response, re.DOTALL)[0]
    else: 
        issue = "nuanced"

    return issue

# Define the prompts (same as before)
difference_identification_prompt: str = """
You are tasked with comparing two summaries and identifying key differences between them. 
Provide a concise and clear explanation of what has been added, removed, or modified in the refined summary compared to the generated summary.

### INPUTS ###
GENERATED_SUMMARY: 
{}

REFINED_SUMMARY: 
{}

### INSTRUCTIONS ###
DIFFERENCES:
- Highlight what has been and WHY added to the refined summary.
- Highlight any Hallucinations that have been removed from the summary and why.  
- Highlight any Concepts, Topics or Domains that have been added to the text.
- DO NOT INCLUDE MARKDOWN IN YOUR OUTPUT. 

Ensure the response is well-organized and directly addresses the differences.
"""

issue_classification_prompt = """
You have been provided with differences between two versions of a text. Your task is to classify the collective problem into one of the following categories:

- **Principle Issue**: A broad, conceptual problem that cannot be generalized. It is not context-dependent and can be identified through clear rules or patterns. These issues can be resolved by a language model or similar tools without requiring fine-tuning.
- **Nuanced Issue**: A context-specific problem that can be easily generalized. It requires a fine-tuned model to resolve because it is sensitive to specific details, context, or nuances of the problem.

### INSTRUCTIONS:
1. Read the differences provided carefully.
2. Identify if each difference corresponds to a **Principle Issue** or a **Nuanced Issue** based on the following guidelines:
   - **Principle Issues** typically involve:
     - General errors in logic, clarity, or consistency.
     - Broad problems in language or conceptual understanding.
     - Cannot be resolved with a general solution. Requires without context-specific adaptation.
   - **Nuanced Issues** involve:
     - Specific context-dependent errors or inconsistencies.
     - Problems that require a more tailored or expert approach to resolve.
     - Can be generalized and would require fine-tuning a model to adapt to specific cases.
3. By looking at the all the differences, provide the classification: **Principle Issue** or **Nuanced Issue**.
4. Your output should be in <issue> tags.
5. Output Structure:  
- if the issue is a principle issue then return <issue>principle</issue>  
- if the issue is a nuanced issue then return <issue>nuanced</issue>  

### INPUTS:
- The differences you need to classify are as follows:
{}
  
### OUTPUT:
- By reading all differences, classify it as either **Principle Issue** or **Nuanced Issue**.
- if the issue is a principle issue then return <issue>principle</issue>  
- if the issue is a nuanced issue then return <issue>nuanced</issue>  
"""

summary_refinement_prompt: str = """
You are a summary refinement prompt. Your goal is to take some context which will be provided to you
from within a chapter. You will also be provided with a generated summary as an input using the 
context of the chapter. Your goal is to refine the provided summary. 

### INPUTS ### 
CHAPTER_CONTEXT: str -> Text that belongs to a chapter within a book. 
GENERATED_SUMMARY: str -> Summary generated from all the text provided as input. 
CHAPTER_TITLE: str -> Title of the chapter.

### OUTPUT ### 
REFINED_SUMMARY: str -> Refine the provided summary.

### INSTRUCTIONS ### 
- To refine the summary you must ask yourself the following series of questions. 
    a) Given the chapter title and the Summary Context are all the concepts in the book covered? 
    - If yes, then move on to the next question. 
    - If no, then identify the concepts that aren't covered and include them in the summary. 

    b) Given the length of the Context is the summary large enough?
    - If the summary is large enough then move on to the next question.  
    - If the summary isn't large enough then extend the length of the summary. 
    - If the summary is too large then leave it as it is. 
    - DO NOT HALLUCINATE INFORMATION, TO MAKE IT LARGE. 

    c) Given the Summary Context and the the generated and extended summary, have there been 
    any hallucinations within the summary ?   
    - If there are any hallucinations then remove them. 
    - If there aren't then generate the final summary.  

- In summary, Make sure your summary has covered all the concepts, Is large enough and doesn't have 
hallucinations. 
- Encapsulate the final summary within <refined_summary> tags. 

### CHAPTER CONTEXT ### 
{} 

### CHAPTER TITLE ### 
{}

### GENERATED_SUMMARY ### 
{}

### OUTPUT ### 
"""

if "refined_summary" not in st.session_state:
    st.session_state.refined_summary = ""
if "generated_summary" not in st.session_state:
    st.session_state.generated_summary = ""
if "differences" not in st.session_state:
    st.session_state.differences = ""
if "show_differences" not in st.session_state:
    st.session_state.show_differences = False
if "issue_classification" not in st.session_state:
    st.session_state.issue_classification = ""

# Generate Refined Summary button
if st.button("Generate Refined Summary"):
    try:
        with st.spinner("Refining the summary... This might take a few seconds..."):
            # Load chapter content
            chapter_json_blob_path = os.path.join(
                EMAIL_ID, "chapterwise_processed_json", BOOK_NAME, chapter_name, "inherent_metadata.json"
            )
            chapter_content = json.loads(get_blob_content(bucket, chapter_json_blob_path))

            # Combine text content
            summary_content = " ".join([node.get("text") for node in chapter_content]).strip()

            # Load existing summary
            summary_content_blob_path = os.path.join(
                EMAIL_ID, "chapter_summary_metadata", BOOK_NAME, chapter_name, "summary_content.txt"
            )
            summary_text = get_blob_content(bucket, summary_content_blob_path)

            # Generate prompt
            prompt = summary_refinement_prompt.format(
                summary_content,
                chapter_name,
                summary_text
            )

            # Prepare messages for OpenAI
            text_messages = [
                {"role": "system", "content": "Generate your answer in English language."},
                {"role": "user", "content": prompt},
            ]

            # Refine summary using OpenAI
            html_response = refine_summary(OPENAI_API_KEY, text_messages)
            refined_summary = extract_refined_summary(html_response)

            # Store summaries in session state
            st.session_state.refined_summary = refined_summary
            st.session_state.generated_summary = summary_text
            st.session_state.show_differences = False  # Reset differences flag

            # Display chapter text and generated summary side by side
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Chapter Text")
                st.text_area("Chapter Context", summary_content, height=300, disabled=True)

            with col2:
                st.subheader("Generated Summary")
                st.text_area("Generated Summary", summary_text, height=300, disabled=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# # Display refined summary if available
# if st.session_state.refined_summary:
#     st.subheader("Refined Summary")
#     refined_summary_editable = st.text_area(
#         "Refined Summary",
#         st.session_state.refined_summary,
#         height=300
#     )
#     st.session_state.refined_summary = refined_summary_editable

#     # Generate Differences button
#     # Generate Differences button
# if st.button("Generate Differences"):
#     st.session_state.show_differences = True
#     with st.spinner("Identifying the differences... This might take a few seconds..."):
#         differences_prompt = difference_identification_prompt.format(
#             st.session_state.generated_summary,
#             st.session_state.refined_summary
#         )
#         diff_messages = [
#             {"role": "system", "content": "Generate your answer in English language."},
#             {"role": "user", "content": differences_prompt},
#         ]
#         st.session_state.differences = identify_differences(OPENAI_API_KEY, diff_messages)

#         # Issue classification
#         st.session_state.issue_classification = issue_classifier(
#             OPENAI_API_KEY,
#             diff_messages,
#             st.session_state.differences
#         )

# # Display differences if available and button was clicked
# if st.session_state.show_differences and st.session_state.differences:
#     st.subheader("Differences")
#     st.text_area("Differences", st.session_state.differences, height=300, disabled=True)

#     # Display the issue classification
#     st.subheader("Issue Classification")
#     st.text(st.session_state.issue_classification)

if st.session_state.refined_summary:
    st.subheader("Refined Summary")
    refined_summary_editable = st.text_area(
        "Refined Summary",
        st.session_state.refined_summary,
        height=300
    )
    st.session_state.refined_summary = refined_summary_editable

    # Generate Differences button
    if st.button("Generate Differences"):
        st.session_state.show_differences = True
        with st.spinner("Identifying the differences... This might take a few seconds..."):
            # Generate differences
            differences_prompt = difference_identification_prompt.format(
                st.session_state.generated_summary,
                st.session_state.refined_summary
            )
            diff_messages = [
                {"role": "system", "content": "Generate your answer in English language."},
                {"role": "user", "content": differences_prompt},
            ]
            st.session_state.differences = identify_differences(OPENAI_API_KEY, diff_messages)

            # Generate issue classification
            st.session_state.issue_classification = issue_classifier(
                OPENAI_API_KEY,
                st.session_state.differences
            )

        # Display differences and classification
        if st.session_state.differences:
            st.subheader("Differences")
            st.text_area("Differences", st.session_state.differences, height=300, disabled=True)

            st.subheader("Issue Classification")
            st.text(f"Classification: {st.session_state.issue_classification}")
            st.balloons()

