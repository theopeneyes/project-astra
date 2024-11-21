from typing import Dict, List, Tuple 
import re 

def get_relevant_count(js_object: Dict, 
                       messages: List[Dict], 
                       counting_prompt: str, 
                       gpt4o, gpt4o_encoder) -> Tuple[
                           Dict[
                            str, 
                            Dict[str, int|str]] | int
                        ]: 

    token_count: int = 0 
    relevant_documents: Dict[str, Dict[str, int| str]] = {}
    for js_key, js_value in js_object.items(): 
        messages[0]["content"][0]["text"] = counting_prompt.format(js_key, js_value)

        content = gpt4o.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
            temperature=0.01,
        )
        
        llm_response = content.choices[0].message.content
        token_count += len(gpt4o_encoder.encode(llm_response)) 

        if re.findall(r"<count>(.*?)</count>", llm_response, re.DOTALL)[0]: 
            try: 
                relevant_count = int(re.findall(
                    r"<count>(.*?)</count>", 
                    llm_response, 
                    re.DOTALL,  
                ))
            except Exception as _: 
                print(f"The word count for topic: {js_key} by llm is not an integer...\nView the response below")
                print(llm_response)
            
            relevant_documents[js_key] = {
                "text": js_value, 
                "count": relevant_count, 
                "llm_response": llm_response, 
            }
        else: 
            print(f"The llm couldn't produce an output in section: {js_key}. Response: ")
            print(llm_response)
        
    return relevant_documents


        