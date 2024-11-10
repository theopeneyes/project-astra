from typing import Dict 

import re 

def detect_language(img_encoding: str, messages: Dict, language_detection_prompt:str, gpt4o) -> str: 
    messages[1]["content"][0]["text"] = language_detection_prompt 
    messages[1]["content"][1]["image_url"]["url"] = (
        f"data:image/jpeg;base64,{img_encoding}") 

    response = gpt4o.chat.completions.create(
        model="gpt-4o-mini",
        messages=[messages[1]],
    )

    # extracting the output from the language 
    response_content = response.choices[0].message.content
    if re.findall(r"<language>(.*?)</language>", response_content):
        language: str = re.findall(r"<language>(.*?)</language>", response_content)[0]

    return language  
    