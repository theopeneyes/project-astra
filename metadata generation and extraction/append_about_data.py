import os
from dotenv import load_dotenv
import requests
import json
load_dotenv()
token = os.getenv("HF_TOKEN")

about_json_example = {

    'Concept': str,
    'Sub concept': str,
    'Topic': str,
    'Sub topic': str,
    "root_concept": str,
    "major_domains": str,
    "sub_domains": str,
    "Attributes and connections": {
    str: str
  },
    "formal_representations": {
    "Diagram": str,
    "Model": str
  }

}

json_list = {
        "heading_identifier":"Carburetor",
        "heading_text":"Introduction",
        "sub_heading_text":'null',
        "text_type":"text",
        "paragraph_number":1,
        "text":"A carburetor is a device that blends air and fuel for an internal combustion engine in appropriate ratios for combustion. It operates primarily based on Bernoulli's principle, which states that an increase in the speed of a fluid (in this case, air) occurs simultaneously with a decrease in pressure. The carburetor's main components include the throttle, choke, venturi, float chamber, and jets. The venturi tube, located at the air intake, accelerates the air passing through, reducing its pressure and allowing fuel to be drawn into the airflow. The resulting air-fuel mixture is then sent into the combustion chamber, where it's ignited to produce power. Although carburetors have largely been replaced by fuel injection systems in modern vehicles due to their efficiency and emissions advantages, they remain popular in small engines and vintage automobiles."
}

generated_list = [{'Concept': ['Carburetor', 'Internal Combustion Engine', 'Air-Fuel Mixture', 'Engine Vacuum', 'Fuel Injection', 'Ignition'], 'Sub concept': ['Device', 'Mixing Air with Fuel', 'Drawing in Air', 'Picking up Fuel', 'Efficient Combustion', 'Engine Cylinders'], 'Topic': ['Engine Technology', 'Engine Components', 'Fuel Systems', 'Engine Operation'], 'Sub topic': ['Carburetor Function', 'Air-Fuel Mixture Process', 'Engine Vacuum Mechanism', 'Fuel Injection System', 'Ignition Process']}, {'root_concept': 'Carburetor', 'major_domains': ['Automotive Engineering', 'Internal Combustion Engines'], 'sub_domains': ['Engine Components', 'Fuel Injection Systems'], 'Attributes and connections': {'Carburetor': ['Device', 'Mixes air with fuel', "Uses engine's vacuum", 'Draws in air', 'Picks up fuel via nozzle', "Flows into engine's cylinders"], "Engine's vacuum": ['Draws in air', 'Essential for carburetor function'], 'Fuel Injection Systems': ['Alternative to carburetors', 'Injects fuel directly into engine']}, 'formal_representations': {'Diagram': ['Carburetor internal structure', 'Engine vacuum system', 'Fuel injection system comparison'], 'Model': ['Carburetor operation cycle', 'Engine air-fuel mixture process', 'Comparison of fuel delivery systems']}}]

about_metadata_prompt = f'''

text = {json_list["text"]}
Step 1: Classify the text into one of the items from the list provided below: {generated_list[0]["Concept"]}

Step 2: Classify the text into one of the items from the list provided below: {generated_list[0]["Sub concept"]}. Use concept: {generated_list[0]["Concept"]} as context to the sub concepts you are supposed to extract. 

Step 3: Classify the text into one of the items from the list provided below: {generated_list[0]["Topic"]}

Step 4: Classify the text into one of the items from the list provided below: {generated_list[0]["Sub topic"]}. Use Sub concept {generated_list[0]["Topic"]} as contect to the sub topic you are supposed to extract. 

Then, add your classifications to a JSON in the following format: {about_json_example}


return this final json enclosed in the <json> and </json> tags.
### JSON: ###

'''

# print(generated_list[0]["Topic"])

def append_about(token, about_metadata_prompt, json_list):
    json_text_list = [item["text"] for item in json_list]
    
    for i, item in enumerate(json_list):
        about_metadata_prompt = f'''

        text = {json_list[0]["text"]}
        Step 1: Classify the text into one of the items from the list provided below: {generated_list[i]["Concept"]}

        Step 2: Classify the text into one of the items from the list provided below: {generated_list[i]["Sub concept"]}. Use concept: {generated_list[0]["Concept"]} as context to the sub concepts you are supposed to extract. 

        Step 3: Classify the text into one of the items from the list provided below: {generated_list[i]["Topic"]}

        Step 4: Classify the text into one of the items from the list provided below: {generated_list[i]["Sub topic"]}. Use Sub concept {generated_list[0]["Topic"]} as contect to the sub topic you are supposed to extract. 

        Then, add your classifications to a JSON in the following format: {about_json_example}


        return this final json enclosed in the <json> and </json> tags.
        ### JSON: ###

        '''
                


        
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": f"{about_metadata_prompt}",
        "parameters": {"max_new_tokens": 200, "temperature":0.1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    # print(response.json()[0]["generated_text"].split("### JSON: ###")[1])
    return response.json()

# append_about(token, about_metadata_prompt, json_list)



def classify_about(single_json):

    prompt = f'''
    json_text = {single_json["text"]}
    You are a classification BOT. Your task is to go through step by step and classify the given text and save the results of each step into JSON.

    step 1: Classify the text into one of the concepts from the list of concepts provided:{generated_list[0]["Concept"]}.
    step 2: Classify the text into one of the subconcepts from the list of subconcepts provided: {generated_list[0]["Sub concept"]}. Use this list of concept for a better context: {generated_list[0]["Concept"]}.
    step 3: Classify the text into one of the topics from the list of topics provided: {generated_list[0]["Topic"]} 
    step 4: Classify the text into one of the subtopics from the list of subtopics provided: {generated_list[0]["Sub topic"]}. Use this list of topic for a better context: {generated_list[0]["Topic"]}
    step 5: Classify the text into one of the root concepts from the list of root concepts provided: {generated_list[1]["root_concept"]}.
    step 6: Classify the text into one of the Major Domains from the list of major domains provided: {generated_list[1]["major_domains"]}.
    step 7: Classify the text into one of the Sub Domains from the list of sub domains provided: {generated_list[1]["sub_domains"]}.
    step 7: For the text, select a key-value pair of Attributes and connections from the dictionary provided: {generated_list[1]["Attributes and connections"]} .
    step 7: Classify the text into one of the Formal representations from the list of Formal representations provided: {generated_list[1]["formal_representations"]}.
    
    The JSON you return should look like following:
    {about_json_example}
    
    ### OUTPUT JSON ###
    '''
        
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": f"{prompt}",
        "parameters": {"max_new_tokens": 700, "temperature":0.1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.json()[0]["generated_text"])
    # string_json = response.json()[0]["generated_text"].split("```json")[1].split("```")[0]

    
    # string_json = response.json()[0]["generated_text"].split("### JSON Output ###")[1].split("### Explanation ###")[0]
    # clean_json = json.loads(string_json)
    # result = {** single_json, **clean_json}
    # print(result)
    return 0

y = classify_about(json_list)
print(type(y))
