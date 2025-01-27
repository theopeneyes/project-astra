difference_in_json_identification_prompt = """
You are a JSON difference identification bot. Your task is to compare two JSON objects: the WORST POSSIBLE JSON and the BEST JSON. The WORST JSON is intentionally flawed, containing misaligned, vague, or inaccurate information. The BEST JSON has been improved for better alignment, specificity, and relevance based on the provided CONTEXT.

Your goal is to:
1. Identify the differences between the two JSON objects.
2. Explain the mistakes made by the WORST POSSIBLE JSON by using BEST JSON as a reference.
3. Use the CONTEXT to identify why the WORST POSSIBLE JSON could not produce a JSON as the 
BEST JSON. Use specific parts of text within the CONTEXT to provide as EVIDENCE for the reasoning. 

### CONTEXT ###
{}

### INSTRUCTIONS ###
To complete your task effectively, follow these steps:
1. Identify the flaws in the WORST JSON: Pinpoint the keys where the WORST JSON contains vague, inaccurate, or misaligned information. Compare them with the improved values in the BEST JSON.
2. Explain the mistakes made by the WORST POSSIBLE JSON: Use the BEST JSON as a reference to 
explain what things the WORST POSSIBLE JSON should have incorporated into itself. 
3. Justify using the CONTEXT: After explaining what the WORST JSON should have included, explain 
why it was NOT included in GREAT DETAIL. Identify why the choice made by BEST JSON, is the correct
one using the context.  
5. Format your output as follows:
   <changes>
   key1: reason;
   key2: reason;
   key3: reason;
   ...
   key4: reason;
   </changes>

WORST POSSIBLE JSON:
{}

BEST JSON:
{}
"""

domain_generation_prompt = '''
You are a Depth Extraction bot. Your goal is to generate depth metadata about the domain,
sub-domain provided to you as input. You will be provided with a problem within a JSON object.
Your goal is to identify the domain the problem belongs to and classify it accordingly. 

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

principle_classification_prompt: str = """
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
