from typing import Dict, List 
import requests
import json 
import re 
import logging 

def append_about(token: str, about_metadata_prompt: str, json_list: List[Dict], generated_list: str):
    for item in json_list:
        about_metadata_prompt = about_metadata_prompt.format(
            item["text"], 
            generated_list[0]["concept"], 
            generated_list[0]["sub_concept"], generated_list[0]["concept"], 
            generated_list[0]["topic"], 
            generated_list[0]["sub_topic"], generated_list[0]["topic"], 
        ) 

    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": about_metadata_prompt,
        "parameters": {"max_new_tokens": 200, "temperature":0.1}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    # print(response.json()[0]["generated_text"].split("### JSON: ###")[1])
    return response.json()

# append_about(token, about_metadata_prompt, json_list)

def classify_about(token: str, 
                   single_json: Dict, 
                   generated_list: Dict, 
                   classification_prompt: str, 
                   language: str):

    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    try: 
        payload = {
            "inputs": classification_prompt.format(
                language, 
                single_json["text"], 
                generated_list[0]["Concept"], 
                generated_list[0]["Sub_concept"], generated_list[0]["Concept"], 
                generated_list[0]["Topic"], 
                generated_list[0]["Sub_topic"], generated_list[0]["Topic"], 
                generated_list[1]["root_concept"], 
                generated_list[1]["major_domains"], 
                generated_list[1]["sub_domains"], 
                generated_list[1]["Attributes and connections"], 
                generated_list[1]["formal_representations"], 
            ),

            "parameters": {"max_new_tokens": 700, "temperature":0.1}
        }
    except Exception as E: 
        logging.info("Got a key as follows : " + str(E))
        logging.info("The generated list is as follows: ")
        logging.info(json.dumps(generated_list, indent=4)) 

    response = requests.post(API_URL, headers=headers, json=payload)
    llm_response = (response.json()[0]["generated_text"]
                    .split("### OUTPUT JSON ###")[1]) 
    if re.findall(r"<json>(.*?)</json>", llm_response, re.DOTALL): 
        classified_json = re.findall(r"<json>(.*?)</json>", llm_response, re.DOTALL)[0]
    else: 
        logging.info("No JSON was found in the LLM response. The llm response can be found below.")
        logging.info(llm_response)
        classified_json = {}

    clean_json = json.loads(classified_json)
    result = {** single_json, **clean_json}
    return result
    
    