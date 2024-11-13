from typing import List, Dict 


def generate_response(
    messages: List[Dict], 
    prompt: str, 
    validation_prompt: str, 
    topics: List[str], 
    context: List[str],
    language: str,  
    gpt4o_encoder, 
    gpt4o) -> str: 

    prompt = prompt.format(
        str(topics), 
        context, 
    )

    messages[0]["content"][0]["text"] = messages[0]["content"][0]["text"].format(language)
    messages[1]["content"][0]["text"] = prompt

    completion = gpt4o.chat.completions.create(
        messages=messages, 
        model="gpt-4o-mini", 
        temperature=0.1
    )

    llm_response = completion.choices[0].message.content
    token_count: int = len(gpt4o_encoder.encode(llm_response)) 

    # validation of the output 
    system_prompt = messages[0]["content"][0]["text"] 
    validation_prompt = validation_prompt.format(system_prompt, prompt, llm_response)
    messages[1]["content"][0]["text"] = validation_prompt

    completion = gpt4o.chat.completions.create(
        messages=messages, 
        model="gpt-4o-mini", 
        temperature=0.1
    )

    validated_llm_response = completion.choices[0].message.content
    token_count +=  len(gpt4o_encoder.encode(validated_llm_response)) 

    return validated_llm_response, token_count 



    