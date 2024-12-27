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
]

user_email: str = "test.fourth@yahoo.com"
BASE_LOCATION: str = "../streamlit-app/test_books/"
pdf_name = pdf_names[1] 

# with open(os.path.join(BASE_LOCATION, pdf_name), "rb") as fp: 
#     requests.post(
#         URL + "/upload_pdf", 
#         data = {
#             "email_id": user_email, 
#             "filename" : pdf_name, 
#         }, 
#         files = {
#             "pdf": fp, 
#         }, 
#         timeout=3000, 
#     )
# # pdf_name = "machine-learning-algorithms.pdf"

# convert_response = requests.post(
#     URL + "/convert_pdf", json = {
#         "email_id": user_email, 
#         "uri": f"{user_email}/uploaded_document/{pdf_name}", 
#         "filename": pdf_name,  
# })

# response = requests.post(
#     URL + "/extract_contents_page", 
#     json = {
#         "email_id": user_email, 
#         "filename": pdf_name, 
#         "number_of_pages": 20, 
#     }
# )

# response_content = response.json()
# last_page: int = response_content.get("last_page")
# first_page: int = response_content.get("first_page")

# response = requests.post(
#     URL + "/identify/chapter_pages", 
#     json = {
#         "email_id": user_email, 
#         "filename": pdf_name, 
#         "last_page": last_page, 
#         "first_page": first_page
#     }
# )


# response = requests.post(
#     URL + "/reform/chapter_pages", 
#     json = {
#         "email_id": user_email, 
#         "filename": pdf_name, 
#     }
# )

response = requests.get(URL + f"/book_chapters/{user_email}/{pdf_name}")
chapters = response.json()

for chapter in chapters["titles"]: 
    # response = requests.post(
    #     URL + "/chapter_loader", 
    #     json = {
    #         "email_id": user_email, 
    #         "filename": pdf_name,         
    #         "chapter_name": chapter, 
    #     }
    # )

    response = requests.post(
        URL + "/summarize", 
        json = {
            "email_id": user_email, 
            "filename": pdf_name,         
            "chapter_name": chapter, 
            "language": "English", 
        }
    )

    if response.status_code == 200:

        response = requests.post(
            URL + "/summary_classifier", 
            json = {
                "email_id": user_email, 
                "filename": pdf_name,         
                "chapter_name": chapter, 
                "language": "English", 
            }
        )


    try: 
        if response.status_code != 200: 
            print(response.content)
        content = response.json()

    except JSONDecodeError as err: 
        print(response.content)
