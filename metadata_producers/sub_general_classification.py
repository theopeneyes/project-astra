from metadata_producers.prompts import general_classification_prompt, sub_general_classification_exercises_prompt, sub_general_classification_illustration_prompt
import json
import os
import requests
import logging
import re

from dotenv import load_dotenv
load_dotenv()
token = os.getenv("HF_TOKEN")


# takes a single json, with all 16 metadata, and gives out what part is the said data belongs to    
def sub_general_classifier_exercises(single_json):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": sub_general_classification_exercises_prompt.format(single_json),
        "parameters": {"max_new_tokens": 700, "temperature":0.1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.json())
    llm_response =  (response.json()[0]["generated_text"].split("### OUTPUT ###")[1])
    if re.findall(r"<exercises-cls>(.*?)</exercises-cls>", llm_response, re.DOTALL): 
        classified_json = re.findall(r"<exercises-cls>(.*?)</exercises-cls>", llm_response, re.DOTALL)[0]
    else: 
        logging.info("No JSON was found in the LLM response. The llm response can be found below.")
        logging.info(llm_response)
        classified_json = {}

    return classified_json

def sub_general_classifier_illustration(single_json):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": sub_general_classification_illustration_prompt.format(single_json),
        "parameters": {"max_new_tokens": 700, "temperature":0.1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.json())
    llm_response =  (response.json()[0]["generated_text"].split("### OUTPUT ###")[1])
    if re.findall(r"<illus>(.*?)</illus>", llm_response, re.DOTALL): 
        classified_json = re.findall(r"<illus>(.*?)</illus>", llm_response, re.DOTALL)[0]
    else: 
        logging.info("No JSON was found in the LLM response. The llm response can be found below.")
        logging.info(llm_response)
        classified_json = {}

    return classified_json