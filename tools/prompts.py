# topic = ""
# concept = ""

# chapter1 = '''
# In computer science, a linked list is a linear collection of data elements whose order is not given by their physical placement in memory. Instead, each element points to the next. It is a data structure consisting of a collection of nodes which together represent a sequence. In its most basic form, each node contains data, and a reference (in other words, a link) to the next node in the sequence. This structure allows for efficient insertion or removal of elements from any position in the sequence during iteration. More complex variants add additional links, allowing more efficient insertion or removal of nodes at arbitrary positions. A drawback of linked lists is that data access time is linear in respect to the number of nodes in the list. Because nodes are serially linked, accessing any node requires that the prior node be accessed beforehand (which introduces difficulties in pipelining). Faster access, such as random access, is not feasible. Arrays have better cache locality compared to linked lists.
# ''


general_classification_prompt = '''
You are an General content classifier bot. Your TASK is to classify the text based on what it relates to from the following: introduction, exercises, main content, summary, illustrations .

This is the text: {}

Please refer to the following definitions for a clear understanding of the terms:
'introduction': 'The opening section that provides background information and context for the topic, preparing readers for what they’re about to learn. It sets the stage and often includes the purpose or objectives of the content.',

'exercises': 'Questions or activities designed to practice or test understanding of the content, often reinforcing learning through hands-on application. They may involve problem-solving, matching, or short answers.',

'main content':'In-depth information on a topic, covering all aspects comprehensively. It explains concepts fully, often with examples, data, and explanations.',

'summary':'A summary/conclusion distills the key points and main message of content into a focused, essential form, removing supporting details while preserving the core meaning and outcome.',
'illustrations': 'Visual images or diagrams or any content that can help explain,enhance or understand  the main content, making complex ideas easier to understand. They can include charts, code, drawings, tables, graphs, diagrams, flowcharts, etc. '


### Instructions###:
Your outcome MUST be simple, unambiguous, and should only contain the classification.
Just provide the classification. DO NOT EXPLAIN.
ENCLOSE your answer in <category> tags.

###Incentives###
You will receive a tip of $$$ for correct description.
You will be penalized if you fail to follow instructions or guidance
classification:

'''


topic_prompt = """
You are an Concept extractor bot. Your TASK is to help extract Concept from {1} in maximum of 4 words . The following is the definition for ease of understanding: A concept is an abstract idea or general notion that represents something, often serving as the foundation for thinking or communication about a particular topic.  You are extracting concepts from educational text books/ chapters.
### Instructions###:
Your outcomes MUST be simple and unambiguous.

###Incentives###
You will receive a tip of $$$ for correct description.
You will be penalized if you fail to follow instructions or guidance.

concept:
{} {}
"""

subtopic_prompt = """
You are an Sub concept extractor bot. Your TASK is to help extract Sub concept from {1} in maximum of 4 words . The following is the definition for ease of understanding: A sub-concept is a more specific idea that falls under the broader umbrella of a primary concept. It represents a more focused or specialized aspect of the main concept. Sub-concepts help break down complex ideas into smaller, more understandable parts. You are extracting concepts from educational text books/ chapters.

The primary concept for this chapter is {2}. Give subconcept strongly in context to the concept.

### Instructions###:
Your outcomes MUST be simple, unambiguous and should only contain the desired subconcept.
After generating the topic enclose it within <subconcept> tags

###Incentives###
You will receive a tip of $$$ for correct description.
You will be penalized if you fail to follow instructions or guidance.
subconcept
{} 

"""


concept_prompt = """
You are an Concept extractor bot. Your TASK is to help extract Concept from {} in maximum of 4 words . The following is the definition for ease of understanding: A concept is an abstract idea or general notion that represents something, often serving as the foundation for thinking or communication about a particular topic.  You are extracting concepts from educational text books/ chapters.
### Instructions###:
Your outcomes MUST be simple and unambiguous.

###Incentives###
You will receive a tip of $$$ for correct description.
You will be penalized if you fail to follow instructions or guidance.

concept
"""

subconcept_prompt = """
You are an Sub concept extractor bot. Your TASK is to help extract Sub concept from {} in maximum of 4 words . The following is the definition for ease of understanding: A sub-concept is a more specific idea that falls under the broader umbrella of a primary concept. It represents a more focused or specialized aspect of the main concept. Sub-concepts help break down complex ideas into smaller, more understandable parts. You are extracting concepts from educational text books/ chapters.

The primary concept for this chapter is {}. Give subconcept strongly in context to the concept.

### Instructions###:
Your outcomes MUST be simple, unambiguous and should only contain the desired subconcept.
After generating the topic enclose it within <subconcept> tags

###Incentives###
You will receive a tip of $$$ for correct description.
You will be penalized if you fail to follow instructions or guidance.
subconcept:
"""
