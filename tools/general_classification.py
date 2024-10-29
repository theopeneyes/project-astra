import requests
from prompts import general_classification_prompt

## change this json_input once PRs's endpoint is ready. this is NOT FINAL. 
json_input = [
    {
        "heading_identifier":"Carburetor",
        "heading_text":"Introduction",
        "sub_heading_text":'null',
        "text_type":"text",
        "paragraph_number":1,
        "text":"Sample text about carburetor"
    }, 
    {
        "heading_identifier":"Dinosaurs",
        "heading_text":"Jurassic Era",
        "sub_heading_text": "Trannosaurous Rex",
        "text_type":"text",
        "paragraph_number":9,
        "text":"Sample text about Dinosaurs"
    },
]


def general_classification(json_input, general_classification_prompt, token='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'):
    general_classification_prompt = general_classification_prompt.format(json_input)
    headers = {"Authorization": f"Bearer {token}"}
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    payload = {
    "inputs": f"{general_classification_prompt}",
    "parameters": {"max_new_tokens": 50, "temperature":0.1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    classification = response.json()[0]["generated_text"].split("classification:")[1].split("<category>")[1].split("</category>")[0]

    return classification