from typing import Dict 
# prompts for generation for different types of outputs 

short_question_answer_prompt: str = """
You are a Short Question Answer Generator Bot. Your goal is to generate Short 
Question Answers based on the following instructions.  

Definition: Short answer questions are typically composed of a brief prompt that demands a written answer that varies in length from one or two words to a few sentences.

###TASK###: You MUST create Short Answer Question based on the provided text and the topic to which they fall under. 

### OUTPUT FORMAT: 
Your output MUST be in the following format: 
<b>Q: [Your question]</b>
<p>A: [Your answer]</p> 

### Instructions###: 
  - Your own words – not statements straight out of the textbook
  - Specific problem and direct questions

###Incentives###
You will receive a tip of $$$ for correct description. 
You will be penalized if you fail to follow instructions or examples

###Additional Guidance###
You MUST ensure that your outcomes are unbiased and avoids relying on stereotypes.
You MUST generate the content in a professional tone and educational exam question style.
You MUST not mention intended audience of the activity in the description.
You MUST also provide the correct answer along with the reasons.

##TOPICS: {}

## TEXT: 
{}

### Question Answers:
"""

prompts: Dict[str, str] = {
    "SQNA": short_question_answer_prompt, 
}

