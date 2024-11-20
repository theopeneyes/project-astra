from metadata_producers.test_9_prompts import *
from metadata_producers.test_9_agents import *
from data_loader.opeanai_formatters import messages, summary_message
import re
import json

def json_validator(single_json: dict,summary:str, language: str, gpt4o_encoder, gpt4o, prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json, summary)
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    # print(llm_response)
    if re.findall(r"<validator>(.*?)</validator>", llm_response, re.DOTALL): 
        summary = re.findall(r"<validator>(.*?)</validator>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x
        # print(x)
    
def reiterator(validator_response: dict, single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt):
    
    
    pass


# {
#     status: True/False,
#     reason: "sgnwug"/ None
# }