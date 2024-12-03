# Example json to store in the prompt 

# great code 
json_example: str = """{
    "root_concept": str,
    "major_domains": List[str],
    "sub_domains": List[str],
    "concepts": List[str],
    "Attributes and connections": Dict[str, List[str]],
    "formal_representations": Dict[str, List[str]],
})"""




# definition prompt 
definitions = '''
Here is a thought: ### Ontology creation prompt ###
Objective: Develop Root Concept, Major Domains, Sub Domains, Concepts, Attributes and Relationships, and Formal Representations for the subject covering the list of concepts provided herewith as an ontology.
### Definitions ###
1. Root Concept: The fundamental idea or principle that serves as the foundation for the text's subject matter. It encapsulates the core theme or overarching idea.
2. Major Domains: Broad areas of knowledge or fields that encompass multiple related topics or subjects. These domains provide a framework for organizing concepts within the root concept.
3. Sub Domains: More specific areas within major domains that further refine the focus. Sub domains represent narrower categories that contribute to a deeper understanding of the major domain.
4. Concepts: Individual ideas or phenomena that are part of a sub domain. Concepts represent specific instances, theories, or practices related to the subject matter.
5. Attributes and connections: Characteristics or properties that describe a concept. Attributes provide additional detail and context, helping to define the concept more clearly. Connections or interactions between concepts, attributes, and other entities. Relationships illustrate how different elements relate to one another within the context of the root concept.
6. Formal Representations: Structured ways of depicting concepts, attributes, and relationships, such as models, diagrams, or frameworks. These representations help visualize the connections and hierarchies within the subject matter.
'''

# The inputs go, chapter json, definition json and json_example json 
json_extractor_prompt: str = """
Read the {} and find me the following out of it: 
Root concept, major domain, sub domains, concepts, Attributes and Connections, Formal representations. 
The definition for each is given here: {}. 
Your output should be a JSON, with each variable being the key and the content corresponding to it as its value.
###Incentives###
You will receive a tip of $$$ for correct description.
You will be penalized if you fail to follow instructions or guidance

####JSON structure####:
{}

####Instructions####:
Your output must be unambiguous. DO NOT EXPLAIN.
Extracted JSON:
"""
