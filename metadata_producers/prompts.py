# chapter_summary = '''
# A carburetor is a device in internal combustion engines that mixes air with fuel in the correct ratio for efficient combustion. It uses the engine's vacuum to draw in air, which then picks up fuel via a nozzle. This mixture flows into the engine's cylinders for ignition.
# '''

# json_input = [
#     {
#         "heading_identifier":"Carburetor",
#         "heading_text":"Introduction",
#         "sub_heading_text": 'null',
#         "text_type":"text",
#         "paragraph_number":1,
#         "text":"paragraph 1 about carburetor"
#     }, 
#     {
#         "heading_identifier":"Carburetor",
#         "heading_text":"Uses",
#         "sub_heading_text": "invention and modification",
#         "text_type":"text",
#         "paragraph_number":2,
#         "text":"paragraph 2 about carburetor "
#     }, 

# ]

about_list_generation_prompt = '''
Your are a About Extraction bot.
### Context Creation TASK###
TASK: Generate a list of Concept, Sub concept, Topic, and Sub topic for the summary provided herewith.
summary = {}
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

depth_list_generation_prompt = '''
Your are a Depth Extraction bot.
### Ontology Creation TASK###
TASK: Read {} and find me the following for it: 1)Root concept, 2)major domain, 3)sub domains, 4)Attributes and Connections, 5)Formal representations
### Definitions ###
1. Root Concept: The fundamental idea or principle that serves as the foundation for the text's subject matter. It encapsulates the core theme or overarching idea.
2. Major Domains: Broad areas of knowledge or fields that encompass multiple related topics or subjects. These domains provide a framework for organizing concepts within the root concept.
3. Sub Domains: More specific areas within major domains that further refine the focus. Sub domains represent narrower categories that contribute to a deeper understanding of the major domain.
4. Attributes and connections: Characteristics or properties that describe a concept. Attributes provide additional detail and context, helping to define the concept more clearly. Connections or interactions between concepts, attributes, and other entities. Relationships illustrate how different elements relate to one another within the context of the root concept.
5. Formal Representations: Structured ways of depicting concepts, attributes, and relationships, such as models, diagrams, or frameworks. These representations help visualize the connections and hierarchies within the subject matter.
Generate lists of each of the above and save them as a JSON
Your output should be a JSON, with each variable being the key and the content corresponding to it as its value.

### JSON example ###

"root_concept": str,
"major_domains": List[str],
"sub_domains": List[str],
"Attributes and connections": Dict[str, List[str]],
"formal_representations": Dict[str, List[str]],

####Instructions####:
Your output must be unambiguous. DO NOT EXPLAIN. 
Enclose your final json output within <json> tags.

### OUTPUT ###
'''


# Format inputs: 
# json_list["text"]
# generated_list[0]["Concept"] 
# generated_list[0]["Sub concept"], generated_list[0]["Concept"] 
# generated_list[0]["Topic"]
# generated_list[0]["Sub topic"], generated_list[0]["Topic"]
about_metadata_prompt = '''
text = {}
Step 1: Classify the text into one of the items from the list provided below: {}
Step 2: Classify the text into one of the items from the list provided below: {}. Use concept: {} as context to the sub concepts you are supposed to extract. 
Step 3: Classify the text into one of the items from the list provided below: {}
Step 4: Classify the text into one of the items from the list provided below: {}. Use Sub concept {} as contect to the sub topic you are supposed to extract. 
Then, add your classifications to a JSON in the following format:

'Concept': str,
'Sub concept': str,
'Topic': str,
'Sub topic': str,
"root_concept": str,
"major_domains": str,
"sub_domains": str,
"Attributes and connections": Dict[str,str]
"formal_representations": Dict[ 
    "Diagram": str,
    "Model": str
]

return this final json enclosed in the <json> and </json> tags.
### JSON: ###
'''

# prompt inputs 
# single_json["text"]
# generated_list[0]["Concept"]
# generated_list[0]["Sub concept"], generated_list[0]["Concept"]
# generated_list[0]["Topic"] 
# generated_list[0]["Sub topic"], generated_list[0]["Topic"]
# generated_list[1]["root_concept"]
# generated_list[1]["major_domains"]
# generated_list[1]["sub_domains"]
# generated_list[1]["Attributes and connections"]
# generated_list[1]["formal_representations"]
classification_prompt = '''`
json_text = {}
You are a classification BOT. Your task is to go through step by step and classify the given text and save the results of each step into JSON.
step 1: Classify the text into one of the concepts from the list of concepts provided:{}.
step 2: Classify the text into one of the subconcepts from the list of subconcepts provided: {}. Use this list of concept for a better context: {}.
step 3: Classify the text into one of the topics from the list of topics provided: {} 
step 4: Classify the text into one of the subtopics from the list of subtopics provided: {}. Use this list of topic for a better context: {}
step 5: Classify the text into one of the root concepts from the list of root concepts provided: {}.
step 6: Classify the text into one of the Major Domains from the list of major domains provided: {}.
step 7: Classify the text into one of the Sub Domains from the list of sub domains provided: {}.
step 8: For the text, select a key-value pair of Attributes and connections from the dictionary provided: {} .
step 9: Classify the text into one of the Formal representations from the list of Formal representations provided: {}.

The JSON you return should look like following:
'Concept': str,
'Sub concept': str,
'Topic': str,
'Sub topic': str,
"root_concept": str,
"major_domains": str,
"sub_domains": str,
"Attributes and connections": Dict[str,str]
"formal_representations": Dict[ 
    "Diagram": str,
    "Model": str
]

### Instruction ### 
Enclose your output within <json> tags. 

### OUTPUT JSON ###
'''