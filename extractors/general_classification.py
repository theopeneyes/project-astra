import requests
# from prompts import general_classification_prompt

# ## change this json_input once PRs's endpoint is ready. this is NOT FINAL. 
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
#         "text":"sample text about dinosaurs", 
#     },
# ]

"""
INPUT: JSON = [p1, p2, ... pN]
-> p(i) is a JSON about an indiviudal pargraph
-> p(i) has an associated chapter title 
-> summary(ch) is associated with p(i) if p(i)[ch] == ch
-> p(i) and summary(ch)
[ch[p[]], ch2[p[]], ch3[p[]]]
"""


def general_classification(json_input, general_classification_prompt, token):
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