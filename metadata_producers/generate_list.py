import requests
import json
from typing import Dict 

# list generation prompts imported from the other file 

# add summary to it 
def generateList(summary, 
                 about_list_generation_prompt, 
                 depth_list_generation_prompt, 
                 token) -> Dict:    

    #about extraction
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": about_list_generation_prompt.format(summary), 
        "parameters": {"max_new_tokens": 200, "temperature":0.1}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    noisy_json = response.json()[0]['generated_text'].split("```json")[1]
    clean_json = noisy_json.split("```")
    x = json.loads(clean_json[0])

    #depth extraction
    payload_d = {
    "inputs": depth_list_generation_prompt.format(summary),
    "parameters": {"max_new_tokens": 600, "temperature":0.1}
    }
    response_d = requests.post(API_URL, headers=headers, json=payload_d)
    depth_noisy_json = response_d.json()[0]['generated_text'].split("### OUTPUT ###")[1]
    y = json.loads(depth_noisy_json)
    final_list = []
    final_list.append(x)
    final_list.append(y)
    return final_list
