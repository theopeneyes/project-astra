import streamlit as st
import json
import os
from google.cloud import storage
import copy 
from openai import OpenAI 
from dotenv import load_dotenv 
import tiktoken 
import re 
import json

load_dotenv(override=True)
gpt4o_encoder = tiktoken.encoding_for_model("gpt-4o-mini")

strength_modification_prompt: str = """
You are a STRENGTH JSON MODIFICATION bot. Your goal is to take an input STRENGTH JSON and modify it
according to instructions given below.

### DEFINITIONS ###
* STRENGTH JSON: A strength JSON is a JSON that is formatted as follows:
Dict[
    "concept": List[str]
    "sub_concept": List[str]
    "topic": List[str]
    "sub_topic": List[str]
]

- A strength JSON will always contain the four attributes described in the formatted dictionary
above.

- The definitions of the four attributes are given below:
    * concept: A concept is an abstract idea or general notion that represents something, often serving as the foundation for thinking or communication about a particular topic. Concepts represent specific instances, theories, or practices related to the subject matter.
    * sub_concept: A sub-concept is a more specific idea that falls under the broader umbrella of a primary concept. It represents a more focused or specialized aspect of the main concept. Sub-concepts help break down complex ideas into smaller, more understandable parts.
    * topic: A topic is a broad subject or area of interest.
    * sub_topic: a subtopic is a more specific aspect or division within that larger topic.

### INPUTS ###
CONTEXT:You will be provided with a summary context which summarizes a chapter from within a book.
STRENGTH JSON: You will be provided with a STRENGTH JSON

### INSTRUCTIONS ###
- Analyze the CONTEXT and find concepts, topics, sub_concepts, sub_topics within the CONTEXT that
have not been covered by the lists of concept, topic, sub_concept, sub_topic respectively in the
STRENGTH JSON.
- If any concept is mentioned in the CONTEXT which isn't added to the list of concepts, then add
it to the list.
- If any sub_concept is mentioned in the CONTEXT which isn't added to the list of sub_concepts,
then add it to the list.
- If any topic is mentioned in the CONTEXT which isn't added to the list of topics, then add
it to the list.
- If any sub_topic is mentioned in the CONTEXT which isn't added to the list of sub_topics, then add
it to the list.
- Your output MUST be enclosed between <json> tags.

### CONTEXT ###
{}

### STRENGTH JSON ###
{}

### OUTPUT ###
"""

depth_modification_prompt: str = """
You are a DEPTH JSON MODIFICATION bot. Your goal is to take an input DEPTH JSON and modify it
according to the instructions given below.

### DEFINITIONS ###
* DEPTH JSON: A DEPTH JSON is a JSON that is formatted as follows:
Dict[
    "root_concept": List[str],
    "major_domains": List[str],
    "sub_domains": List[str],
    "attributes_and_connections": Dict[str, List[str]],
    "formal_representations": Dict[str, List[str]]
]

- A DEPTH JSON will always contain the five attributes described in the formatted dictionary above.

- The definitions of the five attributes are given below:
    * root_concept: The fundamental idea or principle that serves as the foundation for the text's subject matter. It encapsulates the core theme or overarching idea.
    * major_domains: Broad areas of knowledge or fields that encompass multiple related topics or subjects. These domains provide a framework for organizing concepts within the root concept.
    * sub_domains: More specific areas within major domains that further refine the focus. Sub domains represent narrower categories that contribute to a deeper understanding of the major domain.
    * attributes_and_connections: Characteristics or properties that describe a concept. Attributes provide additional detail and context, helping to define the concept more clearly. Connections or interactions between concepts, attributes, and other entities. Relationships illustrate how different elements relate to one another within the context of the root concept.
    * formal_representations: Structured ways of depicting concepts, attributes, and relationships, such as models, diagrams, or frameworks. These representations help visualize the connections and hierarchies within the subject matter.

### INPUTS ###
CONTEXT: You will be provided with a summary context that summarizes a chapter from within a book.
DEPTH JSON: You will be provided with a DEPTH JSON.

### INSTRUCTIONS ###
- Analyze the CONTEXT and find root concepts, major domains, sub domains, attributes and connections,
and formal representations within the CONTEXT that are not covered by the respective attributes
in the DEPTH JSON.

- If any root concept is mentioned in the CONTEXT which isn't added to the list of root concepts,
then add it to the list.
- If any major domain is mentioned in the CONTEXT which isn't added to the list of major domains,
then add it to the list.
- If any sub domain is mentioned in the CONTEXT which isn't added to the list of sub domains,
then add it to the list.
- If any attribute or connection is mentioned in the CONTEXT that isn't already mapped in
attributes_and_connections, then add it to the dictionary with the appropriate key.
- If any formal representation is mentioned in the CONTEXT that isn't already mapped in
formal_representations, then add it to the dictionary with the appropriate key.

- Your output MUST be enclosed between <json> tags.

### CONTEXT ###
{}

### DEPTH JSON ###
{}

### OUTPUT ###
"""

strength_cleanup_prompt: str = """
You are a STRENGTH JSON CLEANUP bot. Your goal is to take an input STRENGTH JSON and modify it
according to instructions given below by removing unnecessary items.

### DEFINITIONS ###
* STRENGTH JSON: A strength JSON is a JSON that is formatted as follows:
Dict[
    "concept": List[str]
    "sub_concept": List[str]
    "topic": List[str]
    "sub_topic": List[str]
]

- A strength JSON will always contain the four attributes described in the formatted dictionary
above.

- The definitions of the four attributes are given below:
    * concept: A concept is an abstract idea or general notion that represents something, often serving as the foundation for thinking or communication about a particular topic. Concepts represent specific instances, theories, or practices related to the subject matter.
    * sub_concept: A sub-concept is a more specific idea that falls under the broader umbrella of a primary concept. It represents a more focused or specialized aspect of the main concept. Sub-concepts help break down complex ideas into smaller, more understandable parts.
    * topic: A topic is a broad subject or area of interest.
    * sub_topic: A subtopic is a more specific aspect or division within that larger topic.

### INPUTS ###
CONTEXT: You will be provided with a summary context that summarizes a chapter from within a book.
STRENGTH JSON: You will be provided with a STRENGTH JSON.

### INSTRUCTIONS ###
- Analyze the CONTEXT and identify concepts, sub_concepts, topics, and sub_topics that are NOT discussed or elaborated on sufficiently within the CONTEXT.
- Remove any concept, sub_concept, topic, or sub_topic from the STRENGTH JSON that is unnecessary or irrelevant based on the CONTEXT.
- Ensure that only those items that are meaningfully discussed or directly related to the CONTEXT remain in the STRENGTH JSON.
- Do NOT add any new items to the STRENGTH JSON. Only remove the ones that do not align with the CONTEXT.

### OUTPUT FORMAT ###
- Return the cleaned-up STRENGTH JSON in the exact same format as the input.
- Your output MUST be enclosed between <json> tags.

### CONTEXT ###
{}

### STRENGTH JSON ###
{}

### OUTPUT ###
"""

depth_cleanup_prompt: str = """
You are a DEPTH JSON CLEANUP bot. Your goal is to take an input DEPTH JSON and modify it
by removing unnecessary items according to the instructions given below.

### DEFINITIONS ###
* DEPTH JSON: A DEPTH JSON is a JSON that is formatted as follows:
Dict[
    "root_concept": List[str],
    "major_domains": List[str],
    "sub_domains": List[str],
    "attributes_and_connections": Dict[str, List[str]],
    "formal_representations": Dict[str, List[str]]
]

- A DEPTH JSON will always contain the five attributes described in the formatted dictionary above.

- The definitions of the five attributes are given below:
    * root_concept: The fundamental idea or principle that serves as the foundation for the text's subject matter. It encapsulates the core theme or overarching idea.
    * major_domains: Broad areas of knowledge or fields that encompass multiple related topics or subjects. These domains provide a framework for organizing concepts within the root concept.
    * sub_domains: More specific areas within major domains that further refine the focus. Sub domains represent narrower categories that contribute to a deeper understanding of the major domain.
    * attributes_and_connections: Characteristics or properties that describe a concept. Attributes provide additional detail and context, helping to define the concept more clearly. Connections or interactions between concepts, attributes, and other entities. Relationships illustrate how different elements relate to one another within the context of the root concept.
    * formal_representations: Structured ways of depicting concepts, attributes, and relationships, such as models, diagrams, or frameworks. These representations help visualize the connections and hierarchies within the subject matter.

### INPUTS ###
CONTEXT: You will be provided with a summary context that summarizes a chapter from within a book.
DEPTH JSON: You will be provided with a DEPTH JSON.

### INSTRUCTIONS ###
- Analyze the CONTEXT and identify root concepts, major domains, sub domains, attributes and connections,
and formal representations that are NOT discussed or elaborated on sufficiently within the CONTEXT.
- Remove any root concept, major domain, sub domain, attribute, connection, or formal representation
from the DEPTH JSON that is unnecessary or irrelevant based on the CONTEXT.
- Ensure that only those items that are meaningfully discussed or directly related to the CONTEXT remain in the DEPTH JSON.
- Do NOT add any new items to the DEPTH JSON. Only remove the ones that do not align with the CONTEXT.

### OUTPUT FORMAT ###
- Return the cleaned-up DEPTH JSON in the exact same format as the input.
- Your output MUST be enclosed between <json> tags.

### CONTEXT ###
{}

### DEPTH JSON ###
{}

### OUTPUT ###
"""

difference_reason_prompt: str = """
You are a difference reasoning bot. Your goal is to analyze a WORST JSON, the summary
CONTEXT, and the MISSING JSON to explain why certain attributes were not included in the
WORST JSON. You must treat the WORST JSON as the most flawed and inadequate representation
possible. Your reasoning should always hold the WORST JSON accountable for omissions, errors,
or poor design.

### INPUTS ###
CONTEXT: You will be provided with the summarized text of a chapter.
WORST JSON: You will also be provided with a WORST JSON, which will be a series of key-value
pairs where the key will be a descriptor of the list of entities that describe the content in
some way within the summary.
MISSING JSON: This will be a dictionary where the key will be a descriptor, and the value
will be a list of items that SHOULD HAVE BEEN added to the WORST JSON but weren't.

### INSTRUCTIONS ###
- Analyze the CONTEXT and compare it with the WORST JSON and MISSING JSON.
- For each item in the MISSING JSON:
    1. Assume that the WORST JSON is inherently flawed and inadequate in capturing relevant
       attributes.
    2. Provide a reason why the item was not added to the WORST JSON. The reason should:
        - Highlight the inadequacy, poor design, or lack of comprehensiveness of the WORST JSON.
        - Emphasize flaws in the WORST JSON's ability to interpret or process the CONTEXT.
        - Avoid attributing blame to the CONTEXT or summary for being unclear or ambiguous.
    3. Clearly state whether the omission is justified solely based on the failure or limitations
       of the WORST JSON (e.g., poor logic, incomplete representation, lack of sophistication).

- Ensure your reasoning is grounded in the given CONTEXT but never shift blame to it.
Instead, focus on the shortcomings of the WORST JSON in recognizing, capturing, or processing
the relevant information.

### OUTPUT FORMAT ###
- Your output MUST be a JSON dictionary with the keys being the descriptors and values
also being dictionaries with the items in the list being keys and the REASON being the values.
- It should be enclosed between <reasoning> tags.

### CONTEXT ###
{}

### WORST JSON ###
{}

### MISSING JSON ###
{}

### OUTPUT ###
"""

recognition_reason_prompt: str = """
You are a recognition reasoning bot. Your task is to analyze the WORST JSON, the summary CONTEXT, and the MISSING JSON to explain why specific attributes were not included in the WORST JSON. The aim is to identify the flaws in the WORST JSON's design and logic that led to the omission of these attributes.

### INPUTS ###
CONTEXT: You will be provided with the summarized text of a chapter.
WORST JSON: You will also be provided with a WORST JSON, a series of key-value pairs where the key represents a descriptor of entities found in the summary.
MISSING JSON: This will be a dictionary where the key is a descriptor, and the value is a list of items that SHOULD have been added to the WORST JSON but weren't.

### INSTRUCTIONS ###
- Compare the CONTEXT with the WORST JSON and MISSING JSON.
- For each item in the MISSING JSON:
    1. Focus on identifying why the WORST JSON failed to include that particular attribute.
    2. Analyze and describe how the WORST JSON's poor logic, oversimplification, or design limitations led to the omission.
    3. Provide reasoning that explicitly lays the blame on the shortcomings of the WORST JSON, avoiding any blame on the CONTEXT or summary.
    4. Emphasize that the WORST JSON's failure to recognize and include these attributes indicates flaws in its structure, data processing abilities, or overall design.

- Your output should specifically focus on explaining the failures in the WORST JSON's structure and logic in capturing or processing the relevant information.

### OUTPUT FORMAT ###
- Your output MUST be a JSON dictionary with the keys being the descriptors and values being dictionaries. Each key will represent an item from the MISSING JSON, and the value will be the detailed reasoning why it was omitted.
- This reasoning should explain how the WORST JSON's deficiencies prevented it from recognizing or capturing these attributes.
- The reasoning should emphasize that the issue lies with the inadequacy of the WORST JSON, not the CONTEXT or summary.

### CONTEXT ###
{}

### WORST JSON ###
{}

### MISSING JSON ###
{}

### OUTPUT ###
"""

difference_classification_prompt: str = """
You are a problem classification bot. Your goal is to classify a problem into one of two: principle
or nuanced problem.

### INPUT ###
PROBLEM: You will be provided with a input problem which you have to classify.

### DEFINITIONS ###
Problem Types:
- principle: A problem that can be effectively resolved by following a structured sequence of steps or by improving the quality of the output through refinement. These issues are systematic, predictable, and can be addressed using established methods or principles.

- nuanced: A problem that is highly context-specific, non-generalizable, and requires a deeper understanding of broader or intricate factors to address. These issues often demand situational judgment and cannot be solved solely through predefined processes.

### INSTRUCTIONS ###
- classify the problem into nuanced or principle using the definitions above.
- if the problem is nuanced then return <issue>nuanced</issue>
- if the problem is principle then return <issue>principle</issue>

### PROBLEM ###
{}

### OUTPUT ###
"""

principle_type_classification_prompt: str = """
You are a principle classification bot. Your goal is to classify the principle problem into one of
two: Meta-prompting or Feedback.

### DEFINITIONS ###
- meta-prompting: If the problem can be resolved by taking a sequence of steps it can be classified
as meta-prompting.
- feedback: If the problem can be resolved by simply making the quality of it better it can be
classified as feedback.

### INSTRUCTIONS ###
- classify the problem into meta-prompting or feedback using the definitions above.
- if the problem is meta-prompting then return <issue>meta-prompting</issue>
- if the problem is feedback then return <issue>feedback</issue>

### PROBLEM ###
{}

### OUTPUT ###
"""

domain_generation_prompt = '''
You are a Depth Extraction bot. Your goal is to generate depth metadata about the major-domain,
sub-domain provided to you as input.

### PROBLEM ###
{}

### ONTOLOGY CREATION TASK ###
TASK: Read the problem provided above and find the following for it:
1) domain
2) subdomain

### DEFINITIONS ###
1. domain: Broad areas of knowledge or fields that encompass multiple related topics or
subjects. These domains provide a framework for organizing concepts within the root concept.
2. subdomain: More specific areas within major domains that further refine the focus. Sub domains represent narrower categories that contribute to a deeper understanding of the major domain.

Your output should be a JSON, with each variable being the key and the content corresponding to it as its value.

### JSON example ###

"domain": str,
"subdomain": str,

#### INSTRUCTIONS ####:
- Your output must be unambiguous. DO NOT EXPLAIN.
- You MUST write your final JSON output in between <json> tags.
- You MUST ENSURE that you only provide a SINGLE JSON DICITONARY as an output.
- If you do not find any one of concept or subconcept or topic or subtopic, then simply return an empty list attached to the corresponding key.

### OUTPUT ###
'''

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BUCKET_NAME = "upload-file-ps"
EMAIL_ID = "test.fifth@yahoo.com"
FILES = ["lbdl", "Machine-Learning-For-Absolute-Beginners"]
GCP_JSON_PATH = "./.secrets/gcp_bucket.json"

gpt4omini = OpenAI(api_key=OPENAI_API_KEY)
# Streamlit App
st.title("Chapter Summary Editor")

text_messages: list[dict] = [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Generate your answer in English language.",
        },
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "",
        },
      ]
    }
]

def classify_problem(problem: str, gpt4omini, gpt4o_encoder):
    """
    Classify a given problem as either principle or nuanced.

    Parameters:
        problem (str): The problem to classify.
        gpt4omini: GPT client object for interaction.
        gpt4o_encoder: Encoder object to count tokens.

    Returns:
        tuple: (classification (str), token_count (int))
    """
    prompt: str = difference_classification_prompt.format(problem)
    text_messages[1]["content"][0]["text"] = prompt

    completions = gpt4omini.chat.completions.create(
        messages=text_messages,
        model="gpt-4o-mini",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count: int = len(gpt4o_encoder.encode(html_response))

    if re.findall(r"<issue>(.*?)</issue>", html_response, re.DOTALL):
        classification = re.findall(r"<issue>(.*?)</issue>", html_response, re.DOTALL)[0]
        return classification, token_count

    raise ValueError("Unable to classify the problem.")

def modify_summary(
        content: str,
        strength_json: dict,
        depth_json: dict,
        gpt4o, gpt4o_encoder):

    prompt: str = strength_modification_prompt.format(content, json.dumps(strength_json))
    text_messages[1]["content"][0]["text"] = prompt

    completions = gpt4o.chat.completions.create(
        messages = text_messages,
        model = "gpt-4o-mini",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<json>(.*?)</json>", html_response, re.DOTALL):
        strength_modified_json: dict = json.loads(re.findall("<json>(.*?)</json>",
                                        html_response, re.DOTALL)[0])
    else:
        strength_modified_json: dict = {
            "concept": [],
            "sub_concept": [],
            "topic": [],
            "sub_topic": []
        }


    prompt: str = depth_modification_prompt.format(content, json.dumps(depth_json))
    text_messages[1]["content"][0]["text"] = prompt

    completions = gpt4o.chat.completions.create(
        messages = text_messages,
        model = "gpt-4o-mini",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<json>(.*?)</json>", html_response, re.DOTALL):
        depth_modified_json: dict = json.loads(re.findall("<json>(.*?)</json>",
                                        html_response, re.DOTALL)[0])
    else:
        depth_modified_json: dict = {
            "root_concepts": [],
            "major_domains": [],
            "sub_domains": [],
            "attributes_and_connections": dict(),
            "formal_representations": dict(),
        }

    return [strength_modified_json, depth_modified_json]

def cleanup_summary(
        content: str,
        strength_json: dict,
        depth_json: dict,
        gpt4o,
        gpt4o_encoder):

    prompt: str = strength_cleanup_prompt.format(content, json.dumps(strength_json))
    text_messages[1]["content"][0]["text"] = prompt

    completions = gpt4o.chat.completions.create(
        messages=text_messages,
        model="gpt-4o-mini",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<json>(.*?)</json>", html_response, re.DOTALL):
        strength_cleaned_json: dict = json.loads(re.findall("<json>(.*?)</json>",
                                           html_response, re.DOTALL)[0])
    else:
        strength_cleaned_json: dict = {
            "concept": [],
            "sub_concept": [],
            "topic": [],
            "sub_topic": []
        }

    prompt: str = depth_cleanup_prompt.format(content, json.dumps(depth_json))
    text_messages[1]["content"][0]["text"] = prompt

    completions = gpt4o.chat.completions.create(
        messages=text_messages,
        model="gpt-4o-mini",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<json>(.*?)</json>", html_response, re.DOTALL):
        depth_cleaned_json: dict = json.loads(re.findall("<json>(.*?)</json>",
                                         html_response, re.DOTALL)[0])
    else:
        depth_cleaned_json: dict = {
            "root_concepts": [],
            "major_domains": [],
            "sub_domains": [],
            "attributes_and_connections": dict(),
            "formal_representations": dict(),
        }

    return [strength_cleaned_json, depth_cleaned_json]

def addition_difference(
        strength_json: dict,
        depth_json: dict,
        modified_strength_json: dict,
        modified_depth_json: dict)-> list[dict]:

    strength_differences: dict = {}
    for key in modified_strength_json:
        strength_differences[key] = list(set(modified_strength_json[key]) - set(strength_json[key]))

    depth_differences: dict = {}

    for key in modified_depth_json:
        if isinstance(modified_depth_json[key], dict):
            depth_differences[key] = {}
            for sub_key in modified_depth_json[key]:
                unique_values = list(set(modified_depth_json[key].get(sub_key, [])) -
                                     set(depth_json[key].get(sub_key, [])))
                if unique_values:
                    depth_differences[key][sub_key] = unique_values
        else:
            depth_differences[key] = list(set(modified_depth_json[key]) - set(depth_json[key]))

    return [strength_differences, depth_differences]

def subtraction_difference(
        strength_json: dict,
        depth_json: dict,
        modified_strength_json: dict,
        modified_depth_json: dict) -> list[dict]:

    strength_differences: dict = {}
    for key, value in strength_json.items():
        strength_differences[key] = list(set(strength_json[key]) - set(modified_strength_json[key]))

    depth_differences: dict = {}
    for key in depth_json:
        if isinstance(depth_json[key], dict):
            depth_differences[key] = {}
            for sub_key in depth_json[key]:
                removed_values = list(set(depth_json[key].get(sub_key, [])) -
                                      set(modified_depth_json[key].get(sub_key, [])))
                if removed_values:
                    depth_differences[key][sub_key] = removed_values
        else:
            depth_differences[key] = list(set(depth_json[key]) - set(modified_depth_json[key]))

    return [strength_differences, depth_differences]

def classify_principle(problem: str, gpt4omini, gpt4o_encoder):
    """
    Classify a principle problem as either meta-prompting or feedback.

    Parameters:
        problem (str): The principle problem to classify.
        gpt4omini: GPT client object for interaction.
        gpt4o_encoder: Encoder object to count tokens.

    Returns:
        tuple: (classification (str), token_count (int))
    """
    prompt: str = principle_type_classification_prompt.format(problem)
    text_messages[1]["content"][0]["text"] = prompt

    completions = gpt4omini.chat.completions.create(
        messages=text_messages,
        model="gpt-4o-mini",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count: int = len(gpt4o_encoder.encode(html_response))

    if re.findall(r"<issue>(.*?)</issue>", html_response, re.DOTALL):
        classification =re.findall(r"<issue>(.*?)</issue>", html_response, re.DOTALL)[0]
        return classification, token_count

    raise ValueError("Unable to classify the problem.")


def reason_difference(
    summary_context: str,
    strength_json: dict,
    depth_json: dict,
    missing_strength_json: dict,
    missing_depth_json: dict,
    gpt4o, gpt4o_encoder) -> tuple[dict]:

    prompt: str = difference_reason_prompt.format(summary_context,
                                                  json.dumps(strength_json), json.dumps(missing_strength_json))
    text_messages[1]["content"][0]["text"] = prompt

    completions = gpt4o.chat.completions.create(
        messages=text_messages,
        model="gpt-4o-mini",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<reasoning>(.*?)</reasoning>", html_response, re.DOTALL):
        strength_reasoning_json: dict = json.loads(re.findall("<reasoning>(.*?)</reasoning>",
                                         html_response, re.DOTALL)[0])

    prompt: str = difference_reason_prompt.format(summary_context,
                                                  json.dumps(depth_json), json.dumps(missing_depth_json))
    text_messages[1]["content"][0]["text"] = prompt

    completions = gpt4o.chat.completions.create(
        messages=text_messages,
        model="gpt-4o-mini",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<reasoning>(.*?)</reasoning>", html_response, re.DOTALL):
        depth_reasoning_json: dict = json.loads(re.findall("<reasoning>(.*?)</reasoning>",
                                         html_response, re.DOTALL)[0])

    return strength_reasoning_json, depth_reasoning_json

def domain_extraction(reason: str, gpt4omini, gpt4o_encoder) -> list[dict | int]:
    # infinite void
    prompt: str = domain_generation_prompt.format(reason)
    text_messages[1]["content"][0]["text"] = prompt

    completions = gpt4omini.chat.completions.create(
        messages = text_messages,
        model = "gpt-4o-mini",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<json>(.*?)</json>", html_response, re.DOTALL):
        attribute_json: str = re.findall("<json>(.*?)</json>",
                                        html_response, re.DOTALL)[0]
        if attribute_json:
            try:
                actual_json: dict = json.loads(attribute_json.lower())
            except:
                actual_json: dict = {
                    "domain": "",
                    "subdomain": "",
                }

    return actual_json, token_count

col1, col2 = st.columns(2)

with col1: 
    book_name = st.selectbox("Select a Book", FILES)

with col2: 
    chapter_name = st.text_input("Enter Chapter Name", "1_Machine Learning")

# Initialize GCS client
gcs_client = storage.Client.from_service_account_json(GCP_JSON_PATH)
bucket = gcs_client.bucket(BUCKET_NAME)

# Define blob paths
summary_blob_path = os.path.join(EMAIL_ID, "chapter_summary_metadata", book_name, chapter_name, "summary_content.txt")
classified_summary_blob_path = os.path.join(EMAIL_ID, "chapter_summary_metadata", book_name, chapter_name, "classified_summary_content.json")
summary_blob = bucket.blob(summary_blob_path)
classified_summary_blob = bucket.blob(classified_summary_blob_path)

try:
    # Load Summary and JSON Data
    with summary_blob.open("r") as fp:
        summary_text = fp.read()
    
    with classified_summary_blob.open("r") as fp:
        summary_classified_json = json.load(fp)
    
    initial_strength_json, initial_depth_json = summary_classified_json
    
    # Initialize session state for strength and depth JSONs if not exists
    if 'strength_json' not in st.session_state:
        st.session_state.strength_json = copy.deepcopy(initial_strength_json)
    if 'depth_json' not in st.session_state:
        st.session_state.depth_json = copy.deepcopy(initial_depth_json)
    
    # 2. Summary Text Section
    st.subheader("Summary")
    st.text_area("Summary Text", summary_text, height=200)
    
    # 3. JSON Modification Section
    st.subheader("Modify JSONs")
    col1, col2 = st.columns(2)
    
    # Strength JSON editor
    with col1:
        st.markdown("### Strength JSON")
        for concept, values in st.session_state.strength_json.items():
            st.markdown(f"#### {concept.title()}")
            if isinstance(values, list):
                if f"strength_{concept}_values" not in st.session_state:
                    st.session_state[f"strength_{concept}_values"] = values.copy()
                
                selected_values = st.multiselect(
                    f"Select values for {concept}",
                    st.session_state[f"strength_{concept}_values"],
                    default=st.session_state[f"strength_{concept}_values"],
                    key=f"strength_select_{concept}"
                )
                st.session_state.strength_json[concept] = selected_values
                
                new_value = st.text_input(f"Add new value to {concept}", key=f"add_strength_{concept}")
                if st.button(f"Add to {concept}", key=f"button_strength_{concept}"):
                    if new_value and new_value not in st.session_state[f"strength_{concept}_values"]:
                        st.session_state[f"strength_{concept}_values"].append(new_value)
                        st.session_state.strength_json[concept] = st.session_state[f"strength_{concept}_values"]
                        st.rerun()
            else:
                st.text("Dictionary type - direct editing not supported")
    
    # Depth JSON editor
    with col2:
        st.markdown("### Depth JSON")
        for concept, values in st.session_state.depth_json.items():
            st.markdown(f"#### {concept.title()}")
            if isinstance(values, list):
                if f"depth_{concept}_values" not in st.session_state:
                    st.session_state[f"depth_{concept}_values"] = values.copy()
                
                selected_values = st.multiselect(
                    f"Select values for {concept}",
                    st.session_state[f"depth_{concept}_values"],
                    default=st.session_state[f"depth_{concept}_values"],
                    key=f"depth_select_{concept}"
                )
                st.session_state.depth_json[concept] = selected_values
                
                new_value = st.text_input(f"Add new value to {concept}", key=f"add_depth_{concept}")
                if st.button(f"Add to {concept}", key=f"button_depth_{concept}"):
                    if new_value and new_value not in st.session_state[f"depth_{concept}_values"]:
                        st.session_state[f"depth_{concept}_values"].append(new_value)
                        st.session_state.depth_json[concept] = st.session_state[f"depth_{concept}_values"]
                        st.rerun()
            else:
                st.text("Dictionary type - direct editing not supported")
    
    # Submit button
    if st.button("Submit JSONs"):
        st.subheader("Original vs Updated JSONs")
        comp_col1, comp_col2 = st.columns(2)
        
        # Display original JSONs
        with comp_col1:
            st.markdown("### Original JSONs")
            st.markdown("#### Strength JSON")
            st.json(initial_strength_json)
            st.markdown("#### Depth JSON")
            st.json(initial_depth_json)
        
        # Display updated JSONs
        with comp_col2:
            st.markdown("### Updated JSONs")
            st.markdown("#### Strength JSON")
            st.json(st.session_state.strength_json)
            st.markdown("#### Depth JSON")
            st.json(st.session_state.depth_json)
        
        # Show changes summary
        st.subheader("Changes Summary")
        
        # Calculate and display changes
        added_strength = {
            k: list(set(st.session_state.strength_json.get(k, [])) - set(initial_strength_json.get(k, [])))
            for k in set(st.session_state.strength_json) | set(initial_strength_json)
            if isinstance(st.session_state.strength_json.get(k, []), list)
        }
        removed_strength = {
            k: list(set(initial_strength_json.get(k, [])) - set(st.session_state.strength_json.get(k, [])))
            for k in set(st.session_state.strength_json) | set(initial_strength_json)
            if isinstance(initial_strength_json.get(k, []), list)
        }
        
        added_depth = {
            k: list(set(st.session_state.depth_json.get(k, [])) - set(initial_depth_json.get(k, [])))
            for k in set(st.session_state.depth_json) | set(initial_depth_json)
            if isinstance(st.session_state.depth_json.get(k, []), list)
        }
        removed_depth = {
            k: list(set(initial_depth_json.get(k, [])) - set(st.session_state.depth_json.get(k, [])))
            for k in set(st.session_state.depth_json) | set(initial_depth_json)
            if isinstance(initial_depth_json.get(k, []), list)
        }
        
        change_col1, change_col2 = st.columns(2)
        with change_col1:
            st.markdown("### Strength JSON Changes")
            st.markdown("#### Added:")
            for concept, values in added_strength.items():
                if values:
                    st.markdown(f"**{concept}:** {values}")
            st.markdown("#### Removed:")
            for concept, values in removed_strength.items():
                if values:
                    st.markdown(f"**{concept}:** {values}")
        
        with change_col2:
            st.markdown("### Depth JSON Changes")
            st.markdown("#### Added:")
            for concept, values in added_depth.items():
                if values:
                    st.markdown(f"**{concept}:** {values}")
            st.markdown("#### Removed:")
            for concept, values in removed_depth.items():
                if values:
                    st.markdown(f"**{concept}:** {values}")

        with st.spinner("Analyzing changes..."):
            # Make sure all JSONs are properly formatted before processing
            initial_strength_clean = json.loads(json.dumps(initial_strength_json))
            initial_depth_clean = json.loads(json.dumps(initial_depth_json))
            updated_strength_clean = json.loads(json.dumps(st.session_state.strength_json))
            updated_depth_clean = json.loads(json.dumps(st.session_state.depth_json))
            
            # Calculate differences
            modified_difference_strength_json, modified_difference_depth_json = addition_difference(
                initial_strength_clean,
                initial_depth_clean,
                updated_strength_clean,
                updated_depth_clean
            )
            
            # Get reasoning
            strength_reason, depth_reason = reason_difference(
                summary_text,
                initial_strength_clean,
                initial_depth_clean,
                modified_difference_strength_json,
                modified_difference_depth_json,
                gpt4omini,
                gpt4o_encoder
            )
            
            # Store results in session state
            st.session_state.strength_reason = strength_reason
            st.session_state.depth_reason = depth_reason

        col1, col2 = st.columns(2)
        with col1: 
            st.markdown("### Strength JSON Reasons")
            st.json(st.session_state.strength_reason)

        with col2: 
            st.markdown("### Depth JSON Reasons")
            st.json(st.session_state.depth_reason)
            


except json.JSONDecodeError as e:
    st.error(f"JSON formatting error: {str(e)}")
    st.write("Debug: Problem JSON structure:")
    st.write({
        "initial_strength": initial_strength_json,
        "initial_depth": initial_depth_json,
        "updated_strength": st.session_state.strength_json,
        "updated_depth": st.session_state.depth_json
    })

except Exception as e:
    st.error(f"An error occurred: {str(e)}")




