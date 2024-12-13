# import json
# import os 
# from dotenv import load_dotenv
# load_dotenv()
# BUCKET_NAME = os.getenv("BUCKET_NAME")
# from google.cloud import storage



# # initializing the bucket for data   
# storage_client = storage.Client()
# gcs_client = storage.Client.from_service_account_json('/.secrets/gcp_bucket.json')
# bucket = gcs_client.bucket(BUCKET_NAME)


# try:
#     final_json_blob = bucket.blob(os.path.join(
#                                     "abc@gmail.com",
#                                     "final_json",
#                                     "English.json",
#     ))

#     with final_json_blob.open("r") as f:
#             final_json = json.load(fp=f)

#     # output = your_processing_func(final_json)

# except Exception as E:
#       # do whatever with the error
#       pass

def semantic_similarity(gcp_topic: list,
                        gpt4o_encoder,
                        gpt_4o):
    
    pass

