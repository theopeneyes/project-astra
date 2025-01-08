import re 
from .prompts import summarization_prompt as prompt 
from .skeleton import text_messages as messages 
from .exceptions import SummaryNotFoundException 

# summarized document 
def summarize_texts(text_content: str, 
                    language_code: str,  
                    gpt4o_encoder, gpt4o) -> tuple[str| None] : 

    messages[0]["content"][0]["text"] = f"Your output should be in the language associated with the following language code: {language_code}" 
    messages[1]["content"][0]["text"] = prompt.format(language_code, text_content) 
    completion = gpt4o.chat.completions.create(
        messages=messages, 
        model="gpt-4o-mini", 
        temperature=0.1
    )

    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 
    if re.findall(r"<summary>(.*?)</summary>", llm_response, re.DOTALL): 
        summary = re.findall(r"<summary>(.*?)</summary>", llm_response, re.DOTALL)[0]

    if summary == "": 
        raise SummaryNotFoundException(llm_response=llm_response, text_content=text_content)
        # return (None, llm_response, token_count) 
    else: 
        return ("done", summary, token_count)  

    
        

    

