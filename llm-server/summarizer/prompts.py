summarization_prompt: str = """
### SYSTEM ### 
You MUST ensure that the summarization is in {} language. 

You are a summarization bot. Your goal is to take the chapter content within a book and 
generate a detailed summary from the given text. Here is the text content provided below:  

### Text to summarize ### 
{}

### Instruction ### 
You must enclose the summary within <summary> tags in your output. 

### Summary ###
"""

hallucination_elimination_prompt: str = """
You are a hallucination elimintation bot. You will be provided with some context of a chapter and
summary of that context. Your goal will be to remove all hallucinations from within the summary.


### INPUTS ###
CONTEXT: You will be provided with an large corpus of text that belongs to a chapter.
SUMMARY: You will be provided with a summary of the large corpus of text.


### DEFINITONS ###
- Hallucinations: Statements written in the summary which is not EXPLICITLY mentioned or
IMPLIED in the CONTEXT.

### INSTRUCTIONS ###
- Find out which parts of texts in the SUMMARY are Hallucinations.
- Remove all Hallucinations from the SUMMARY.
- If there are not many Hallucinations, then shrink the text to a smaller version of the summary.
- Add the summary between <accurate_summary> tags.

### CONTEXT ###
{}

### SUMMARY ###
{}

### OUTPUT ###
"""

summary_enlargement_prompt: str = """
You are a summary enlargement bot. Your goal is to expand the summary of a chapter.

### DEFINITIONS ###
- domain: Broad areas of knowledge or fields that encompass multiple related topics or subjects.
These domains provide a framework for organizing concepts within the root concept.

- subdomain: More specific areas within major domains that further refine the focus.
Sub domains represent narrower categories that contribute to a deeper understanding of the major domain.

### INPUT ###
CONTEXT: You will be provided with an large corpus of text that belongs to a chapter.
SUMMARY: You will be provided with a summary of the large corpus of text.
TITLE: The title of the chapter to which the large corpus of text belongs to.

### INSTRUCTIONS ###
- Carefully VIEW the CONTEXT of the Chapter. Identify domains and subdomains that aren't covered in
the SUMMARY.
- Summarize the text that talks about a certain domain/sub-domain and add it to the existing
summary to increase the length of the summary.
- If there are no domains/sub-domains uncovered in the context then increase the size of the summary
by covering more text that was skipped from the CONTEXT.
- Your summary should lie between <enlarged_summary> tags.

### CONTEXT ###
{}

### SUMMARY ###
{}

### TITLE ###
{}

### OUTPUT ###
"""

domain_generation_prompt = '''
You are a Depth Extraction bot. Your goal is to generate depth metadata about the major-domain,
sub-domain provided to you as input.

### SUMMARY ###
{}

### ONTOLOGY CREATION TASK ###
TASK: Read the summary provided above and find the following for it:
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

difference_identification_prompt: str = """
You are a difference identification bot. Your goal is to the flaws within the original summary,
which the ideal summary improves upon. You have to point out ISSUES that exist with the
original summary.

### DEFINITION ###
1. concept: A concept is an abstract idea or general notion that represents something, often serving as the foundation for thinking or communication about a particular topic. Concepts represent specific instances, theories, or practices related to the subject matter.
2. sub_concept: A sub-concept is a more specific idea that falls under the broader umbrella of a primary concept. It represents a more focused or specialized aspect of the main concept. Sub-concepts help break down complex ideas into smaller, more understandable parts.
3. topic: A topic is a broad subject or area of interest.
4. sub_topic: a subtopic is a more specific aspect or division within that larger topic.

### INPUTS ###
- CONTEXT: You will be provided with an large corpus of text that belongs to a chapter.
- SUMMARY: You will be provided with a summary of the large corpus of text.
- IDEAL SUMMARY: You will be provided with an ideal summary of the large corpus of text.

### INSTRUCTIONS ###
- You are to identify the differences in the following domains:
    - HALLUCINATIONS: Identify which parts in the SUMMARY are hallucinated and improved upon
    in the IDEAL SUMMARY. Leave it as an empty parameter if none are found.
    - ADDED IDEAS: Identify the concepts, sub_concepts, topics, sub_topics that were missing in the
    SUMMARY and how they were added in the IDEAL SUMMARY. Leave it as an empty parameter if
    none are found.
    - WORD OR SENTENCE MODIFICATIONS: Identify the word modifications that were lacking in the
    SUMMARY but were ADDED in the IDEAL SUMMARY. Leave it as an empty parameter if none are found.
    - OTHER MODIFICATIONS: Modifications that are out of all the three domains mentioned above. 
- Your output MUST not be in MARKDOWN.


### CONTEXT ###
{}

### SUMMARY ###
{}

### IDEAL SUMMARY ###
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