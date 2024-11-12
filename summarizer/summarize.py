import requests 
import re 
from typing import Tuple 
from typing import Dict

# summarized document 
def summarize_texts(text_content: str, 
                    language: str,  
                    prompt: str, 
                    messages: Dict, 
                    gpt4o_encoder, gpt4o) -> Tuple[str| None, str] : 
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
    messages[0]["content"][0]["text"] = messages[0]["content"][0]["text"].format(language)
    messages[1]["content"][0]["text"] = prompt.format(language, text_content) 
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
        return (None, llm_response, token_count) 
    else: 
        return ("done", summary, token_count)  

    
        

    

