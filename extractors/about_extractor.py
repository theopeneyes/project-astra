# json_input = [
#     {
#         "heading_identifier":"carburetor",
#         "heading_text":"introduction",
#         "sub_heading_text":'null',
#         "text_type":"text",
#         "paragraph_number":1,
#         "text":"sample text about carburetor"
#     }, 
#     {
#         "heading_identifier":"dinosaurs",
#         "heading_text":"jurassic era",
#         "sub_heading_text": "trannosaurous rex",
#         "text_type":"text",
#         "paragraph_number":9,
#         "text":"sample text about dinosaurs"
#     },
# ]

import requests 

## concept 
def concept_extractor(json_input, concept_prompt, token):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    concept_prompt = concept_prompt.format(json_input)
    payload = {
        "inputs": f"{concept_prompt}",
        "parameters": {"max_new_tokens": 5, "temperature":0.1}

    }
    response = requests.post(API_URL, headers=headers, json=payload)
    concept = response.json()[0]["generated_text"].split("concept:")[1].strip()
    return concept

## subconcept
def subconcept_extractor(json_input, subconcept_prompt, token):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    subconcept_prompt = subconcept_prompt.format(json_input, )
    payload = {
        "inputs": f"{subconcept_prompt}",
        "parameters": {"max_new_tokens": 20, "temperature":0.1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    subconcept = response.json()[0]["generated_text"].split("subconcept:")[1].split("<subconcept>")[1].split("</subconcept>")[0]
    return subconcept

## Topic 
def topic_extractor(topic_prompt, token):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": f"{topic_prompt}",
        "parameters": {"max_new_tokens": 20, "temperature":0.1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    topic = response.json()[0]["generated_text"].split("Topic:")[1].split("<topic>")[1].split("</topic>")[0]
    return topic


## subtopic
def subtopic_extractor(subtopic_prompt, token):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": f"{subtopic_prompt}",
        "parameters": {"max_new_tokens": 20, "temperature":0.1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    subtopic = response.json()[0]["generated_text"].split("subtopic:")[1].split("<subtopic>")[1].split("</subtopic>")[0]
    return subtopic

subtopic_extractor(subtopic_prompt, token)
# next_json = {

#     'topic': topic,
#     'subtopic': subtopic_extractor(subtopic_prompt),
#     'concept': concept,
#     'subconcept': subconcept_extractor(subconcept_prompt),
# }