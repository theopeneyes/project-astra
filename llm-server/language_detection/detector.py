import re 
from .skeleton import messages
from .prompts import text_extraction_prompt

def detect_language(img_encoding: str, 
                    translator, 
                    gpt4o, gpt4o_encoder) -> list[str, int]: 

    messages[1]["content"][0]["text"] = text_extraction_prompt 
    messages[1]["content"][1]["image_url"]["url"] = (
        f"data:image/jpeg;base64,{img_encoding}") 

    response = gpt4o.chat.completions.create(
        model="gpt-4o-mini",
        messages=[messages[1]],
    )

    # extracting the output from the language 
    response_content: int = response.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(response_content)) 

    extracted_content: str = ""
    if re.findall(r"<content>(.*?)</content>", response_content): 
        extracted_content = re.findall(r"<content>(.*?)</content>", response_content)[0]
    elif re.findall(r"<(.*?)>", response_content): 
        extracted_content = re.findall(r"<(.*?)>", response_content)[0]
    else: 
        extracted_content = response_content  
    
    language_response: str = translator.detect_language(extracted_content)
    return language_response.get("confidence"), language_response.get("language"), token_count
    