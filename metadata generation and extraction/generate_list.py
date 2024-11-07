from prompts import chapter_summary
import requests
import json
token = "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"
summary = chapter_summary
about_list_generation_prompt = f'''
"Your are a About Extraction bot.
### Context Creation TASK###
TASK: Generate a list of Concept, Sub concept, Topic, and Sub topic for the summary provided herewith.
summary = {summary}
### Definitions ###
1. concept: A concept is an abstract idea or general notion that represents something, often serving as the foundation for thinking or communication about a particular topic. Concepts represent specific instances, theories, or practices related to the subject matter.
2. sub_concept: A sub-concept is a more specific idea that falls under the broader umbrella of a primary concept. It represents a more focused or specialized aspect of the main concept. Sub-concepts help break down complex ideas into smaller, more understandable parts.
3. topic: A topic is a broad subject or area of interest.
4. sub_topic: a subtopic is a more specific aspect or division within that larger topic.
Generate lists of each of the above and return them as a JSON.
### Instructions ###
enclose your final json output in the <json> tag.
JSON:

'''
depth_json_example = '''

{
        "root_concept": str,
        "major_domains": List[str],
        "sub_domains": List[str],
        "Attributes and connections": Dict[str, List[str]],
        "formal_representations": Dict[str, List[str]],
}

'''
depth_list_generation_prompt = f'''

Your are a Depth Extraction bot.
### Ontology Creation TASK###
TASK: Read {summary} and find me the following for it: 1)Root concept, 2)major domain, 3)sub domains, 4)Attributes and Connections, 5)Formal representations
### Definitions ###
1. Root Concept: The fundamental idea or principle that serves as the foundation for the text's subject matter. It encapsulates the core theme or overarching idea.
2. Major Domains: Broad areas of knowledge or fields that encompass multiple related topics or subjects. These domains provide a framework for organizing concepts within the root concept.
3. Sub Domains: More specific areas within major domains that further refine the focus. Sub domains represent narrower categories that contribute to a deeper understanding of the major domain.
4. Attributes and connections: Characteristics or properties that describe a concept. Attributes provide additional detail and context, helping to define the concept more clearly. Connections or interactions between concepts, attributes, and other entities. Relationships illustrate how different elements relate to one another within the context of the root concept.
5. Formal Representations: Structured ways of depicting concepts, attributes, and relationships, such as models, diagrams, or frameworks. These representations help visualize the connections and hierarchies within the subject matter.
Generate lists of each of the above and save them as a JSON
Your output should be a JSON, with each variable being the key and the content corresponding to it as its value.

### JSON example ###
{depth_json_example}
####Instructions####:
Your output must be unambiguous. DO NOT EXPLAIN.
### OUTPUT ###
'''

def generateList(about_list_generation_prompt, depth_list_generation_prompt, summary, token):    
    #about extraction
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": f"{about_list_generation_prompt}",
        "parameters": {"max_new_tokens": 200, "temperature":0.1}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    noisy_json = response.json()[0]['generated_text'].split("```json")[1]
    clean_json = noisy_json.split("```")
    x = json.loads(clean_json[0])

    #depth extraction
    payload_d = {
    "inputs": f"{depth_list_generation_prompt}",
    "parameters": {"max_new_tokens": 600, "temperature":0.1}
    }
    response_d = requests.post(API_URL, headers=headers, json=payload_d)
    depth_noisy_json = response_d.json()[0]['generated_text'].split("### OUTPUT ###")[1]
    y = json.loads(depth_noisy_json)
    final_list = []
    final_list.append(x)
    final_list.append(y)
    return final_list
generated_list = generateList(about_list_generation_prompt, depth_list_generation_prompt, summary, token)
print(generated_list)