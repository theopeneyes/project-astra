import tiktoken 
import re 
import json 

from .prompts import difference_classification_prompt
from .prompts import difference_in_json_identification_prompt
from .prompts import domain_generation_prompt
from .prompts import principle_classification_prompt

from .skeleton import text_messages as messages 

gpt_encoder = tiktoken.encoding_for_model("gpt-3.5-turbo") 
gpt4o_encoder = tiktoken.encoding_for_model("gpt-4o-mini") 


def edit(json_node: dict, user_modified_json: dict, all_content_text: str, gpt_client) -> list[dict| int]:
    token_count : int = 0 
    prompt: str = difference_in_json_identification_prompt.format(
        all_content_text, json.dumps(json_node), json.dumps(user_modified_json))

    messages[0]["content"][0]["text"] = f"Your output should be in the english language"
    messages[1]["content"][0]["text"] = prompt
    completion = gpt_client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        temperature=0.1
    )

    comparison_response: str = completion.choices[0].message.content
    token_count += len(gpt4o_encoder.encode(comparison_response))  

    if re.findall(r"<changes>(.*?)</changes>", comparison_response, re.DOTALL):
            comparison = re.findall(r"<changes>(.*?)</changes>", comparison_response, re.DOTALL)[0]
    
    data: list = [] 

    for problem in comparison.split("\n"): 
        if problem: 
            prompt: str = domain_generation_prompt.format(problem)
            messages[0]["content"][0]["text"] = f"Your output should be in the english language"
            messages[1]["content"][0]["text"] = prompt
            completion = gpt_client.chat.completions.create(
                messages=messages,
                model="gpt-3.5-turbo",
                temperature=0.1
            )

            domain_generated: str = completion.choices[0].message.content
            token_count += len(gpt_encoder.encode(domain_generated)) 

            if re.findall(r"<json>(.*?)</json>", domain_generated, re.DOTALL):
                domain_stringified:str=re.findall(r"<json>(.*?)</json>", domain_generated, re.DOTALL)[0]
                domain_json : dict = json.loads(domain_stringified) 
            

            prompt: str = difference_classification_prompt.format(problem)
            messages[0]["content"][0]["text"] = f"Your output should be in the english language"
            messages[1]["content"][0]["text"] = prompt
            completion = gpt_client.chat.completions.create(
                messages=messages,
                model="gpt-3.5-turbo",
                temperature=0.1
            )

            classified_problem_response: str = completion.choices[0].message.content
            token_count += len(gpt_encoder.encode(classified_problem_response)) 

            if re.findall(r"<issue>(.*?)</issue>", classified_problem_response, re.DOTALL):
                classified_problem:str=re.findall(r"<issue>(.*?)</issue>", classified_problem_response,
                                                re.DOTALL)[0]
            
            if classified_problem == "principle":  
                prompt: str = principle_classification_prompt.format(problem)
                messages[0]["content"][0]["text"] = f"Your output should be in the english language"
                messages[1]["content"][0]["text"] = prompt
                completion = gpt_client.chat.completions.create(
                    messages=messages,
                    model="gpt-3.5-turbo",
                    temperature=0.1
                )
        
                principle_response: str = completion.choices[0].message.content
                token_count += len(gpt_encoder.encode(principle_response)) 

                if re.findall(r"<issue>(.*?)</issue>", principle_response, re.DOTALL):
                    principle_type:str=re.findall(r"<issue>(.*?)</issue>",
                                                    principle_response, re.DOTALL)[0] 
            else: 
                principle_type: str | None = None 
            
            data.append({
                "generated_output": json_node,
                "desired_generation": user_modified_json, 
                "issue_type": classified_problem,
                "differences": problem,
                "principle_type": principle_type, 
                "field_type": "rewrite_json",
                **domain_json 
            }) 
    
    return data, token_count
        