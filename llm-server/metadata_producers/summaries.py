from .prompts import about_list_generation_prompt, depth_list_generation_prompt
from .exceptions import AboutListNotGeneratedException, DepthListNotGeneratedException
from .skeleton import text_messages as messages
from json import JSONDecodeError

import json
import re 
# list generation prompts imported from the other file 

# add summary to it 
def generate_chapter_metadata(
        summary: str , 
        language: str, 
        gpt4o_encoder, 
        gpt4o) -> list[dict]:    

    about_json: dict = {}
    depth_json: dict = {}

    token_count: int =  0
    messages[0]["content"][0]["text"] = messages[0]["content"][0]["text"].format(language)
    messages[1]["content"][0]["text"] = about_list_generation_prompt.format(language, summary)

    completion = gpt4o.chat.completions.create(
        messages=messages, 
        model="gpt-4o-mini", 
        temperature=0.1
    )

    llm_response: str = completion.choices[0].message.content
    token_count += len(gpt4o_encoder.encode(llm_response)) 
    if re.findall(r"<json>(.*?)</json>", llm_response, re.DOTALL): 
        try:
            about_json = json.loads(
                re.findall(r"<json>(.*?)</json>", llm_response, re.DOTALL)[0])
        except JSONDecodeError as decodeError: 
            print(llm_response)
            print(re.findall(r"<json>(.*?)</json>", llm_response, re.DOTALL)[0])
            raise decodeError 
    else: 
        print("Encountered a JSON error parsing error from llm output from Depth Agent...")
        print(f"The prompt provided is {about_list_generation_prompt.format(language, summary)}")
        print(f"The chat completion provided is : {llm_response}")
        print(json.dumps(messages, indent=4))
        raise AboutListNotGeneratedException(llm_response = llm_response)
                    
    messages[0]["content"][0]["text"] = messages[0]["content"][0]["text"].format(language)
    messages[1]["content"][0]["text"] = depth_list_generation_prompt.format(language, summary)
    about_list_generation_prompt.format(language, summary)
    completion = gpt4o.chat.completions.create(
        messages=messages, 
        model="gpt-4o-mini", 
        temperature=0.1
    )

    depth_llm_response: str = completion.choices[0].message.content
    token_count += len(gpt4o_encoder.encode(depth_llm_response)) 

    if re.findall(r"<json>(.*?)</json>", depth_llm_response, re.DOTALL): 
            depth_json = json.loads(
                re.findall(r"<json>(.*?)</json>", depth_llm_response, re.DOTALL)[0])
    else: 
        print("Encountered a JSON error parsing error from llm output from Depth Agent...")
        print(f"The prompt provided is {depth_list_generation_prompt.format(language, summary)}")
        print(f"The chat completion provided is : {depth_llm_response}")
        print(json.dumps(messages, indent=4))
        raise DepthListNotGeneratedException(llm_response=depth_llm_response)

    return [
        about_json, 
        depth_json, 
    ], token_count   
