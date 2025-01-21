import json 
import re 
from .prompts import summary_enlargement_prompt  
from .prompts import hallucination_elimination_prompt
from .prompts import domain_generation_prompt
from .prompts import difference_identification_prompt 
from .prompts import difference_classification_prompt 
from .prompts import principle_type_classification_prompt 
from .skeleton import text_messages

def enlarge_summary(
        content: str, 
        chapter_title: str, 
        summary_text: str, 
        gpt4omini, gpt4o_encoder) -> str: 

    prompt: str = summary_enlargement_prompt.format(content, chapter_title, summary_text)
    text_messages[1]["content"][0]["text"] = prompt
    # print(json.dumps(text_messages, indent=2))
    
    completions = gpt4omini.chat.completions.create(
        messages = text_messages,
        model = "gpt-4o-mini",
        temperature=0.01
    )
    
    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<enlarged_summary>(.*?)</enlarged_summary>", html_response, re.DOTALL):
        enlarged_summary: str = re.findall("<enlarged_summary>(.*?)</enlarged_summary>",
                                        html_response, re.DOTALL)[0]
    
    return enlarged_summary, token_count 

def qualitate_summary(
        content: str, 
        enlarged_summary: str, 
        gpt4omini, gpt4o_encoder) -> list[str| int]:

    prompt: str = hallucination_elimination_prompt.format(content , enlarged_summary)
    text_messages[1]["content"][0]["text"] = prompt
    
    completions = gpt4omini.chat.completions.create(
        messages = text_messages,
        model = "gpt-4o-mini",
        temperature=0.01
    )
    
    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<accurate_summary>(.*?)</accurate_summary>", html_response, re.DOTALL):
        accurate_summary: str = re.findall("<accurate_summary>(.*?)</accurate_summary>",
                                        html_response, re.DOTALL)[0]

    return accurate_summary, token_count 

def domain_extraction(accurate_summary: str, gpt4omini, gpt4o_encoder) -> list[dict | int]: 
    # infinite void 
    prompt: str = domain_generation_prompt.format(accurate_summary)
    text_messages[1]["content"][0]["text"] = prompt
    
    completions = gpt4omini.chat.completions.create(
        messages = text_messages,
        model = "gpt-4o-mini",
        temperature=0.01
    )
    
    html_response: str = completions.choices[0].message.content
    token_count: int = gpt4o_encoder.encode(html_response)
    if re.findall("<json>(.*?)</json>", html_response, re.DOTALL):
        attribute_json: str = re.findall("<json>(.*?)</json>",
                                        html_response, re.DOTALL)[0]
        if attribute_json:
            try:
                actual_json: dict = json.loads(attribute_json.lower())
            except:
                actual_json = {
                    "domain": "",
                    "subdomain": "",
                }
    
    return actual_json, token_count

def problem_extractor(content: str, summary_text: str, accurate_summary: str, gpt4omini, gpt4o_encoder) :
    prompt: str = difference_identification_prompt.format(content,
                                                      summary_text, accurate_summary)
    text_messages[1]["content"][0]["text"] = prompt
    
    completions = gpt4omini.chat.completions.create(
        messages = text_messages,
        model = "gpt-4o-mini",
        temperature=0.01
    )
    
    response: str = completions.choices[0].message.content
    token_count: int = len(gpt4o_encoder.encode(response))

    issues: list = [] 
    principle_types: list = [] 
    problems: list = []

    for text in response.split("\n"): 
        if text.startswith("HALLUCINATIONS") or text.startswith("ADDED IDEAS"): 
            issues.append("principle")
            principle_types.append("feedback")
            problems.append(text) 
        elif text.startswith("OTHER MODIFICATIONS"): 
            prompt: str = difference_classification_prompt.format(text)
            text_messages[1]["content"][0]["text"] = prompt
            
            completions = gpt4omini.chat.completions.create(
                messages = text_messages,
                model = "gpt-4o-mini",
                temperature=0.01
            )
        
            html_response: str = completions.choices[0].message.content
            token_count += len(gpt4o_encoder.encode(html_response))
            if re.findall("<issue>(.*?)</issue>", html_response, re.DOTALL):
                issue: str = re.findall("<issue>(.*?)</issue>", html_response, re.DOTALL)[0] 
        
                if issue == "principle": 
                    prompt: str = principle_type_classification_prompt.format(text)
                    text_messages[1]["content"][0]["text"] = prompt
                    
                    completions = gpt4omini.chat.completions.create(
                        messages = text_messages,
                        model = "gpt-4o-mini",
                        temperature=0.01
                    )
                
                    html_response: str = completions.choices[0].message.content
                    token_count += len(gpt4o_encoder.encode(html_response))

                    if re.findall("<issue>(.*?)</issue>", html_response, re.DOTALL):
                        principle_issue: str = re.findall("<issue>(.*?)</issue>", 
                                                        html_response, re.DOTALL)[0] 
                    else: 
                        print(html_response)
                        principle_issue: str = ""
        
                    issues.append(issue) 
                    principle_types.append(principle_issue) 
                    problems.append(text) 
        
        elif text: 
            problems.append(text) 
            issues.append("nuanced")
            principle_types.append(None) 

    return issues, principle_types, problems, token_count
        
    