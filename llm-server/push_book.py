from dotenv import load_dotenv
from google.cloud import storage

import os 
import requests 
from typing import Dict

load_dotenv(override=True)
BUCKET_NAME: str = os.getenv("BUCKET_NAME")
URL: str = "http://127.0.0.1:8000"
HF_TOKEN: str = os.getenv("HF_TOKEN")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") 
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

base_directory: str = "../streamlit-app/test_books"
pdf_name: str = "algorithms.pdf"
user_email: str = "test.second@yahoo.com"

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

print("Classify our data and rewriting it within intermediate_json folder")
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


print("Relevant Count edit") 
requests.post(
    URL + "/add_word_count", 
    json = {
        "filename": pdf_name, 
        "email_id": user_email,  
    }
)





# topics_blob = bucket.blob(os.path.join(
#     user_email, 
#     "books", 
#     "Machine-Learning-For-Absolute-Beginners.pdf", 
#     "topic.json"
# ))


# concepts_blob = bucket.blob(os.path.join(
#     user_email, 
#     "books", 
#     "Machine-Learning-For-Absolute-Beginners.pdf", 
#     "concept.json"
# ))

# with headings_blob.open("r") as f: 
#     headings = json.load(fp=f)


# with concepts_blob.open("r") as f: 
#     concepts = json.load(fp=f)

# with topics_blob.open("r") as f: 
#     topics = json.load(fp=f) 

# with open("json_editor/ignoreme/machine-learning.json", "r") as f: 
#     final_json = json.load(fp=f)

# edited_json = edit_metadata(final_json, headings, concepts, topics)
# with open("json_editor/ignoreme/machine-learning.json", "w") as f: 
#     json.dump(edited_json, fp=f)
