from metadata_producers.prompts import general_classification_prompt
from metadata_producers.sub_general_classification import sub_general_classifier_exercises
import os
import requests
import re
import json
import logging
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("HF_TOKEN")

def general_classifier_test(single_json: dict):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": general_classification_prompt.format(single_json),
        "parameters": {"max_new_tokens": 700, "temperature":0.1}

    }
    response = requests.post(API_URL, headers=headers, json=payload)
    llm_response =  (response.json()[0]["generated_text"].split("### classification ###")[1])
    print(llm_response)
    if re.findall(r"<category>(.*?)</category>", llm_response, re.DOTALL): 
        classified_json = re.findall(r"<category>(.*?)</category>", llm_response, re.DOTALL)[0]
        single_json["general_classification"] = classified_json
    else: 
        logging.info("No JSON was found in the LLM response. The llm response can be found below.")
        logging.info(llm_response)
        classified_json = {}
    
    return classified_json
    
    # if(single_json("general_classification")=="Exercises"):
    #     sub_general_classification_exercises()
    # elif(single_json("general_classification")=="Illustrations"):
    #     sub_general_classification_exercises()


