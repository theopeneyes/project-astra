from typing import Dict, Union  
import re 

def detect_language(img_encoding: str, 
                    format_converter: Dict[str, str], 
                    messages: Dict, 
                    text_extraction_prompt:str, 
                    language_detection_model, gpt4o_encoder, gpt4o) -> Union[str, int]: 

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
        language_label, _ = language_detection_model.predict(
            extracted_content)
    elif re.findall(r"<(.*?)>", response_content): 
        extracted_content = re.findall(r"<(.*?)>", response_content)[0]
        language_label, _ = language_detection_model.predict(
            extracted_content
        )
    else: 
        language_label, _ = language_detection_model.predict(
           response_content 
        )
    return format_converter[language_label[0].split("__")[-1]].lower(), token_count 
    