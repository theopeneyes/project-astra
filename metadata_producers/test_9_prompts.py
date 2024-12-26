topic_prompt = '''
### SYSTEM ### 
Generate the ouptut in {} language. 
reasoning ={}
### TASK ### 
Your task is to classify the text into the most appropriate topic from the list of topics given below. Refer to the below mentioned definition of a topic:
topic: A topic is a broad subject or area of interest.

json_text = {}
topics = {}
give your output in a JSON that contains a key-value of 'topic': 'your_answer_here'

### INSTRUCTION ###
You MUST encapsulate the JSON within <topic> and </topic> tags. 
Use the reasoning to better formulate your answer. If no reasoning is provided, ignore this instruction. 
### JSON: ###
'''

concept_prompt = '''
### SYSTEM ### 
Generate the ouptut in {} language. 

### TASK ### 
Your task is to classify the text into the most appropriate concept from the list of topics given below. Refer to the below mentioned definition of a concept:
concept: A concept is an abstract idea or general notion that represents something, often serving as the foundation for thinking or communication about a particular topic. Concepts represent specific instances, theories, or practices related to the subject matter.

reason = {}
json_text = {}
concept list = {}
give your output in a JSON that contains a key-value of 'concept': 'your_answer_here'

### INSTRUCTION ###
You MUST encapsulate the JSON within <concept> and </concept> tags.
Use the reasoning to better formulate your answer. If no reasoning is provided, ignore this instruction. 



### JSON: ###

'''

subtopic_prompt = '''
### SYSTEM ### 
Generate the ouptut in {} language. 

### TASK ### 
Your task is to classify the text into the most appropriate subtopic from the list of subtopics given below. Refer to the below mentioned definition of a subtopic:

Here is the topic for the same text to get a better idea: {}

subtopic:  a subtopic is a more specific aspect or division within that larger topic.
reason = {}
json_text = {}
subtopic list = {}
give your output in a JSON that contains a key-value of 'subtopic': 'your_answer_here'

### INSTRUCTION ###
You MUST encapsulate the JSON within <sub_topic> and </sub_topic> tags.
Use the reasoning to better formulate your answer. If no reasoning is provided, ignore this instruction. 

'''




subconcept_prompt = '''
### SYSTEM ### 
Generate the ouptut in {} language. 

### TASK ### 
Your task is to classify the text into the most appropriate subconcept from the list of subconcept given below. Refer to the below mentioned definition of a subconcept:

Here is the concept for the same text to get a better idea: {}

subconcept: A sub-concept is a more specific idea that falls under the broader umbrella of a primary concept. It represents a more focused or specialized aspect of the main concept. Sub-concepts help break down complex ideas into smaller, more understandable parts.

reason = {}
json_text = {}
subconcept list = {}
give your output in a JSON that contains a key-value of 'subconcept': 'your_answer_here'

### INSTRUCTION ###
You MUST encapsulate the JSON within <sub_concept> and </sub_concept> tags.
Use the reasoning to better formulate your answer. If no reasoning is provided, ignore this instruction. 

'''



rootconcept_prompt = '''
### SYSTEM ### 
Generate the ouptut in {} language. 

### TASK ### 
Your task is to classify the text into the most appropriate rootconcept from the list of rootconcept given below. Refer to the below mentioned definition of a rootconcept:

Root Concept: The fundamental idea or principle that serves as the foundation for the text's subject matter. It encapsulates the core theme or overarching idea.

reason = {}
json_text = {}
rootconcept list = {}
give your output in a JSON that contains a key-value of 'rootconcept': 'your_answer_here'

### INSTRUCTION ###
You MUST encapsulate the JSON within <root_concept> and </root_concept> tags.
Use the reasoning to better formulate your answer. If no reasoning is provided, ignore this instruction. 

'''

majordomains_prompt = '''
### SYSTEM ### 
Generate the ouptut in {} language. 

### TASK ### 
Your task is to classify the text into the most appropriate majordomain from the list of majordomain given below. Refer to the below mentioned definition of a majordomain:

Major Domains: Broad areas of knowledge or fields that encompass multiple related topics or subjects. These domains provide a framework for organizing concepts within the root concept.

reason = {}
json_text = {}
majordomain list = {}
give your output in a JSON that contains a key-value of 'major_domain': 'your_answer_here'

### INSTRUCTION ###
You MUST encapsulate the JSON within <major_domains> and </major_domains> tags.
Use the reasoning to better formulate your answer. If no reasoning is provided, ignore this instruction. 
'''


subdomains_prompt = '''


### SYSTEM ### 
Generate the ouptut in {} language. 

### TASK ### 
Your task is to classify the text into the most appropriate subdomain from the list of subdomains given below. Refer to the below mentioned definition of a subordomain:

sub Domains: More specific areas within major domains that further refine the focus. Sub domains represent narrower categories that contribute to a deeper understanding of the major domain


reason= {}
json_text = {}
subdomain list = {}
give your output in a JSON that contains a key-value of 'sub_domains': 'your_answer_here'

### INSTRUCTION ###
You MUST encapsulate the JSON within <sub_domains> and </sub_domains> tags.
Use the reasoning to better formulate your answer. If no reasoning is provided, ignore this instruction. 
'''


attributes_and_connections_prompt = '''

### SYSTEM ### 
Generate the ouptut in {} language. 

### TASK ### 
Your task is to classify the text into the most appropriate 'attributes and connections' from the list of 'attributes_and_connections' given below. Refer to the below mentioned definition of an 'attribute and connection':

attribute and connections : Characteristics or properties that describe a concept. Attributes provide additional detail and context, helping to define the concept more clearly. Connections or interactions between concepts, attributes, and other entities. Relationships illustrate how different elements relate to one another within the context of the root concept.


reason = {}
json_text = {}
attributes and connections data = {}
**Choose ONE entity from the list of attributes and connections provided below. Output ONLY the key-value pair for the chosen entity, along with its corresponding attributes and connections.**

Give your output in a JSON that contains only the key-value pair for the chosen entity in the following format:


{{
  "Attributes_and_connections": {{
    "Entity_name": ["attribute_1", "attribute_2", "attribute_3", ...]
  }}
}}
### INSTRUCTION ###
You MUST encapsulate the JSON within <Attributes and connections> and </Attributes and connections> tags.
Use the reasoning to better formulate your answer. If no reasoning is provided, ignore this instruction. 

'''

formal_representations_prompt = '''

### SYSTEM ### 
Generate the ouptut in {} language. 

### TASK ### 
Your task is to classify the text into the most appropriate formal representation from the list of representations given below. Refer to the below mentioned definition:

Formal Representations: Structured ways of depicting concepts, attributes, and relationships, such as models, diagrams, or frameworks. These representations help visualize the connections and hierarchies within the subject matter.
Generate lists of each of the above and save them as a JSON
Your output should be a JSON, with each variable being the key and the content corresponding to it as its value.

reason = {}
json_text = {}
formal_representations list = {}
give your output in a JSON that contains a key-value of 'formal_representations': 'your_answer_here'

### INSTRUCTION ###
You MUST encapsulate the JSON within <formal_representations> and </formal_representations> tags.
Use the reasoning to better formulate your answer. If no reasoning is provided, ignore this instruction. 



'''

general_classification_prompt = '''

### SYSTEM ### 
Generate the ouptut in {} language. 

You are an General content classifier bot.

### TASK ###

Your TASK is to classify text based on what it relates to from the following:  exercises, main content and illustrations .

This is the text: {}
Refer to the following definitions to get a clear understanding of each. 

DEFINITIONS =
Main Content:
DETAILED information about a topic that explains EVERYTHING clearly and thoroughly. This section should cover ALL important parts of the topic.

Exercises:
These are QUESTIONS, ACTIVITIES, or TASKS that ask the reader to *respond,* *solve,* or *apply* knowledge. Look for question words (e.g., “What,” “How”), blanks to fill in, instructions, or prompts for practicing or testing understanding.


Illustrations:
Visuals like diagrams, charts, tables, or drawings that help explain or simplify the main content. These visuals make it easier to understand complex ideas by showing them in a simple way.


### Instructions###:
Your outcome MUST be simple, unambiguous, and should only contain the classification.
Just provide the classification. DO NOT EXPLAIN.
give your output in a JSON that contains a key-value of 'general_classification': 'your_answer_here'
ENCLOSE your JSON response in <ctr> and </ctr> tags.

###Incentives###
You will receive a tip of $$$ for correct description.
You will be penalized if you fail to follow instructions or guidance
### classification ###


'''

subgeneral_exercises_prompt = '''
### SYSTEM ###
Generate the ouptut in {} language. 
You are an Exercises classifier bot. Your TASK is to classify the text based on one of the following categories: Activity, Quiz or Questions.
Here's the text to classify: {}

Use these definitions to guide your choice:

Activity:
A **hands-on** or **interactive task** where learners **engage** directly, often with **group** participation or **physical** action to practice or explore ideas.

Quiz: 
A **short test** that checks knowledge or understanding with **multiple-choice** or **short-answer** questions, providing a quick **assessment** of specific points.

Questions: 
**Inquiries** designed to make learners **think** or **recall** information. Formats may include **multiple-choice**, **true/false**, or **open-ended** questions to prompt analysis.

### Instructions###
strictly enclose your output in <exercises-cls> and <exercises-cls> tags.
Do not add explanations or extra text.
give your output in a JSON that contains a key-value of 'subgeneral_exercises': 'your_answer_here'

### Incentives ###
Correct classifications will earn you a tip. Misclassification or failure to follow instructions will result in a penalty.

### OUTPUT ###

'''

subgeneral_illustration_prompt = '''

### SYSTEM ###
Generate the ouptut in {} language. 

You are an Illustrations classifier bot. Your TASK is to classify the text based on one of the following categories: Examples, case study, illustrations. 
Here's the text to classify: {}

Use these definitions to guide your choice:

Examples:
Specific instances or items that show or clarify a broader idea. They help by demonstrating how something applies or works in different situations.

Case Study:
A detailed examination of a specific event, group, or individual to understand how something works or to learn from real-life situations. It often includes observations and findings.

Illustration:
A visual representation or diagram that shows an idea, object, or concept to help explain it more clearly. It often includes pictures, drawings, or charts.

### Instructions###
strictly enclose your output in <illustration-cls> and </illustration-cls> tags.
Do not add explanations or extra text.
give your output in a JSON that contains a key-value of 'subgeneral_illustration': 'your_answer_here'

### Incentives ###
Correct classifications will earn you a tip. Misclassification or failure to follow instructions will result in a penalty.

### OUTPUT ###

'''



###########################################################################








validator_prompt = '''


### SYSTEM ###
Generate the ouptut in {} language. 
### TASK ###
You are a validator bot. Your task is to read the contents of a given JSON and see if the given value of an attribute is rightly classified against the given summary or not. 
For example,
if 'subtopic': 'air flow in venturi tubes', your job is to read the given summary, and determine whether 'air flow in venturi tube' is actually a subtopic or not. 

Definitions for each attribute in the JSON is given below:
topic: A topic is a broad subject or area of interest.
concept: A concept is an abstract idea or general notion that represents something, often serving as the foundation for thinking or communication about a particular topic. Concepts represent specific instances, theories, or practices related to the subject matter.
subtopic:  a subtopic is a more specific aspect or division within that larger topic.
subconcept: A sub-concept is a more specific idea that falls under the broader umbrella of a primary concept. It represents a more focused or specialized aspect of the main concept. Sub-concepts help break down complex ideas into smaller, more understandable parts.
Root Concept: The fundamental idea or principle that serves as the foundation for the text's subject matter. It encapsulates the core theme or overarching idea.
Major Domains: Broad areas of knowledge or fields that encompass multiple related topics or subjects. These domains provide a framework for organizing concepts within the root concept.
sub domains: More specific areas within major domains that further refine the focus. Sub domains represent narrower categories that contribute to a deeper understanding of the major domain
attribute and connections : Characteristics or properties that describe a concept. Attributes provide additional detail and context, helping to define the concept more clearly. Connections or interactions between concepts, attributes, and other entities. Relationships illustrate how different elements relate to one another within the context of the root concept.
Formal Representations: Structured ways of depicting concepts, attributes, and relationships, such as models, diagrams, or frameworks. These representations help visualize the connections and hierarchies within the subject matter.

### instructions ###
return your output in a json of the following format-
'status': True if rightly classified, False if not.
'reason': 'Reason as to why the classification might be incorrect if status: False. If status: True, reason: None' 



ENCLOSE your answer in <validator> and </validator> tags.


json = {}
summary = {}

'''