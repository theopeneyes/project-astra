from dotenv import load_dotenv
from google.cloud import storage
from json.decoder import JSONDecodeError
import os 
import requests 

load_dotenv(override=True)
BUCKET_NAME: str = os.getenv("BUCKET_NAME")
URL: str = "http://127.0.0.1:8000"
HF_TOKEN: str = os.getenv("HF_TOKEN")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") 
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

base_directory: str = "../streamlit-app/test_books"
pdf_names: str = [
    "Machine-Learning-For-Absolute-Beginners.pdf", 
    "lbdl.pdf", 
    "rdpd.pdf"
]

user_email: str = "test.fifth@yahoo.com"
BASE_LOCATION: str = "../streamlit-app/test_books/"
pdf_name = pdf_names[2] 

with open(os.path.join(BASE_LOCATION, pdf_name), "rb") as fp: 
    requests.post(
        URL + "/upload_pdf", 
        data = {
            "email_id": user_email, 
            "filename" : pdf_name, 
        }, 
        files = {
            "pdf": fp, 
        }, 
        timeout=300, 
    )

# pdf_name = "machine-learning-algorithms.pdf"

convert_response = requests.post(
    URL + "/convert_pdf", json = {
        "email_id": user_email, 
        "uri": f"{user_email}/uploaded_document/{pdf_name}", 
        "filename": pdf_name,  
})

language_detected_response = requests.post(
   URL + "/detect_lang", json = {
      "email_id": user_email,  
      "filename": pdf_name, 
   } 
)

language_code = language_detected_response.get("detected_language")

response = requests.post(
    URL + "/extract_contents_page", 
    json = {
        "email_id": user_email, 
        "filename": pdf_name, 
        "number_of_pages": 20, 
        "language_code": language_code
    }
)

response_content = response.json()
last_page: int = response_content.get("last_page")
first_page: int = response_content.get("first_page")

response = requests.post(
    URL + "/identify/chapter_pages", 
    json = {
        "email_id": user_email, 
        "filename": pdf_name, 
        "last_page": last_page, 
        "first_page": first_page, 
        "language_code": language_code
    }
)


response = requests.post(
    URL + "/reform/chapter_pages", 
    json = {
        "email_id": user_email, 
        "filename": pdf_name, 
    }
)

response = requests.get(URL + f"/book_chapters/{user_email}/{pdf_name}")
chapters = response.json()

for chapter in chapters["titles"]: 
    response = requests.post(
        URL + "/chapter_loader", 
        json = {
            "email_id": user_email, 
            "filename": pdf_name,         
            "chapter_name": chapter, 
            "language_code": language_code, 
        }
    )

    response = requests.post(
        URL + "/summarize", 
        json = {
            "email_id": user_email, 
            "filename": pdf_name,         
            "chapter_name": chapter, 
            "language_code": language_code, 
        }
    )

    if response.status_code == 200:

        response = requests.post(
            URL + "/summary_classifier", 
            json = {
                "email_id": user_email, 
                "filename": pdf_name,         
                "chapter_name": chapter, 
                "language_code": language_code, 
            }
        )
    

response = requests.get(URL + f"/book_chapters/{user_email}/{pdf_name}")
chapters = response.json()


print("The chapter name is : " , chapters["titles"])

for chapter in chapters["titles"]: 
    # print(chapter)
    response = requests.get(
        URL + f"/get_node_count/{user_email}/{pdf_name}/{chapter}", 
    )

    if response.status_code == 200: 
        count: int =  response.json()["node_count"]
        print("The chapter name is : " , chapter)
    
        for idx in range(count):
            requests.post(
                URL + "/rewrite_json",
                json = {
                    "chapter_name": chapter, 
                    "email_id": user_email,  
                    "filename": pdf_name,
                    "language_code": language_code, 
                    "node_id": idx, 
                }
            )
        
            # topic extraction 
            requests.post(
                URL + "/synthesize/strength/representational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": idx, 
                    "branch_name": "topic",  
                    "chapter_name": chapter, 
                }
            )


            requests.post(
                URL + "/synthesize/strength/relational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": idx,  
                    "branch_name": "topic",  
                    "chapter_name": chapter, 
                }
            )

            requests.post(
                URL + "/synthesize/depth/representational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": idx, 
                    "branch_name": "topic" , 
                    "chapter_name": chapter, 
                }
            )

            requests.post(
                URL + "/synthesize/strength/representational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": idx, 
                    "branch_name": "heading_text",  
                    "chapter_name": chapter, 
                }
            )


            requests.post(
                URL + "/synthesize/strength/relational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": idx,  
                    "branch_name": "heading_text",  
                    "chapter_name": chapter, 
                }
            )

            requests.post(
                URL + "/synthesize/depth/representational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": idx, 
                    "branch_name": "heading_text" , 
                    "chapter_name": chapter, 
                }
            )

            requests.post(
                URL + "/synthesize/strength/representational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": idx, 
                    "branch_name": "concept",  
                    "chapter_name": chapter, 
                }
            )


            requests.post(
                URL + "/synthesize/strength/relational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": idx,  
                    "branch_name": "concept",  
                    "chapter_name": chapter, 
                }
            )

            requests.post(
                URL + "/synthesize/depth/representational", 
                json = {
                    "email_id": user_email, 
                    "filename": pdf_name, 
                    "node_id": idx, 
                    "branch_name": "concept" , 
                    "chapter_name": chapter, 
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
response =  requests.post(
    URL + "/add_word_count", 
    json = {
        "filename": pdf_name, 
        "email_id": user_email,  
    }
)
        
try: 
    if response.status_code != 200: 
        print(response.content)
    content = response.json()

except JSONDecodeError as err: 
    print(response.content)