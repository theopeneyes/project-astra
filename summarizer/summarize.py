import requests 
import re 
from typing import Tuple 
from typing import Dict

# summarized document 
def summarize_texts(text_content: str, language: str,  prompt: str, messages: Dict, token: str, groqAi) -> Tuple[str| None, str] : 
    # TODO: Using an SLM to summarize the document, cannot make the language custom  

    # LM Approach 
    # client = InferenceClient(
    #     model="sshleifer/distilbart-cnn-12-6", 
    #     api_key=token
    # )
    # # summary output 
    # return client.summarization(texts)["summary_text"]

    # SLM 3.5 MINI INSTRUCT Approach  
    # API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    # headers = {"Authorization": f"Bearer {token}"}
    # payload = {
    #     "inputs": prompt.format(language, text_content),
    #     "parameters": {"max_new_tokens": 600, "temperature":0.1}
    # }

    # response = requests.post(API_URL, headers=headers, json=payload)

    # Bigger language model  
    messages[0]["content"] = messages[0]["content"].format(language)
    messages[1]["content"] = prompt.format(language, text_content) 
    completion = groqAi.chat.completions.create(
        messages=messages, 
        model="llama3-8b-8192", 
        temperature=0.1
    )

    llm_response = completion.choices[0].message.content

    if re.findall(r"<summary>(.*?)</summary>", llm_response, re.DOTALL): 
        summary = re.findall(r"<summary>(.*?)</summary>", llm_response, re.DOTALL)[0]
    
    if summary == "": 
        return (None, llm_response) 
    else: 
        return ("done", summary)  

    
        

    

