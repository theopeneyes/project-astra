import json 
import re 

def classify_about(single_json: dict, 
                   generated_list: dict,
                   messages: dict,  
                   classification_prompt: str, 
                   language: str, gpt4o, gpt4o_encoder):

    token_count : int = 0 
    try: 

        messages[0]["content"][0]["text"] = messages[0]["content"][0]["text"].format(language)
        messages[1]["content"][0]["text"] = classification_prompt.format(
            language, 
            single_json["text"], 
            generated_list[0]["concept"], 
            generated_list[0]["sub_concept"], generated_list[0]["concept"], 
            generated_list[0]["topic"], 
            generated_list[0]["sub_topic"], generated_list[0]["topic"], 
            generated_list[1]["root_concept"], 
            generated_list[1]["major_domains"], 
            generated_list[1]["sub_domains"], 
            generated_list[1]["attributes_and_connections"], 
            generated_list[1]["formal_representations"], 
        )

        completion = gpt4o.chat.completions.create(
            messages=messages, 
            model="gpt-4o-mini", 
            temperature=0.1
        )

        llm_response: str = completion.choices[0].message.content

    except Exception as E: 
        print("Got a key as follows : " + str(E))
        print("The generated list is as follows: ")
        print(json.dumps(generated_list, indent=4)) 
        llm_response = ""

    token_count: int = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<json>(.*?)</json>", llm_response, re.DOTALL): 
        classified_json = re.findall(r"<json>(.*?)</json>", llm_response, re.DOTALL)[0]
    else: 
        print("No JSON was found in the LLM response. The llm response can be found below.")
        print(llm_response)
        classified_json = "{}"

    clean_json = json.loads(classified_json)
    result = {** single_json, **clean_json}
    return result, token_count 

