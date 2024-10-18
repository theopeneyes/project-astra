from .llms import llms 
from typing import List, Dict 

import requests 

def generate_response(
    prompt: str, 
    topics: List[str], 
    context: List[str], 
    hf_token: str, 
    model: str) -> str: 

    API_URL: str = "https://api-inference.huggingface.co/models/"

    headers: Dict[str, str] = {
        "Authorization": "Bearer {}".format(hf_token), 
        "X-use-cache": "true", 
        "Content-Type": "application/json",
        "X-wait-for-model": "true", 
    }

    json_input : Dict[str, str] = {
        "inputs": prompt.format(
            str(topics),
            "\n".join(context),  
        ), 
        "parameters": {"max_new_tokens": 1000, "temperature":0.1}
    }

    response = requests.post(
        API_URL + llms[model], 
        headers=headers,
        json=json_input, 
    )

    return (
        response[0]
        ["generated_text"]
        .split("### Question Answers:")[1]
    )

    