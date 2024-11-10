import requests
import json
from typing import Dict, List  
import re 

# list generation prompts imported from the other file 

# add summary to it 
def generateList(summary: str , 
                 about_list_generation_prompt: str , 
                 depth_list_generation_prompt: str , 
                 language: str, 
                 token: str) -> List[Dict]:    

    about_json: Dict = {}
    depth_json: Dict = {}

    #about extraction
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": about_list_generation_prompt.format(language, summary), 
        "parameters": {"max_new_tokens": 600, "temperature":0.1}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # getting the response and extracting the json properly to avoid errors at all costs  
    llm_response = response.json()[0]['generated_text'].split("JSON:")[1]

    if re.findall(r"<json>(.*?)</json>", llm_response, re.DOTALL): 
        about_json = json.loads(
            re.findall(r"<json>(.*?)</json>", llm_response, re.DOTALL)[0])
    else: 
        print("Encountered a JSON error parsing error from llm output from About Agent...")
        print(llm_response)

    #TODO: These two tasks should be two seperate agents: Fixme @Jevin
    
    #depth extraction
    payload_d = {
        "inputs": depth_list_generation_prompt.format(language, summary),
        "parameters": {"max_new_tokens": 600, "temperature":0.1}
    }

    response_d = requests.post(API_URL, headers=headers, json=payload_d)
    depth_llm_response = response_d.json()[0]['generated_text'].split("### OUTPUT ###")[1]

    if re.findall(r"<json>(.*?)</json>", depth_llm_response, re.DOTALL): 
        depth_json = json.loads(
            re.findall(r"<json>(.*?)</json>", depth_llm_response, re.DOTALL)[0])
    else: 
        print("Encountered a JSON error parsing error from llm output from Depth Agent...")
        print(depth_llm_response)

    return [
        about_json, 
        depth_json, 
    ] 
