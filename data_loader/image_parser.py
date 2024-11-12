from google.generativeai.types import HarmCategory, HarmBlockThreshold
from matplotlib import pyplot as plt 
from image_utils.encoder  import encode_image
from image_utils.decoder import decode_image

from typing import List
import PIL 

import re

def parse_images(gpt4o,    
              images: List[str], prompt: str,
              clause_prompt: str, validation_prompt: str, 
              messages: List, text_messages: List, gpt4o_encoder, language: str) -> List[str]:

    title: str | None = None
    new_prompt: str
    output: List[str] = []
    token_count = 0 
    for _, image_encoded in enumerate(images):
        image_encoded = image_encoded["img_b64"]
        image: PIL.Image = decode_image(image_encoded) 

        if title:
            new_prompt = prompt.format(clause_prompt.format(title, "title"), "", "")
        else:
            new_prompt = prompt.format("", "", "")

        # response = gemini.generate_content(
        #     [ new_prompt, image],
        #     safety_settings={
        #         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        #         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        #         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        #         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        #     },
        #     generation_config = config,
        # )

        # try:
        #     output.append(response.text)
        #     if re.findall(r"<title>(.*?)</title>", output[-1])[0] != title:
        #         title = re.findall(r"<title>(.*?)</title>", output[-1])[0]

        # except Exception as _:
        system_msg: str = messages[0]["content"][0]["text"]
        system_msg = system_msg.format(language)
        messages[0]["content"][0]["text"] = system_msg

        messages[1]["content"][0]["text"] = new_prompt 
        messages[1]["content"][1]["image_url"]["url"] = (
            f"data:image/jpeg;base64,{encode_image(image)}") 

        response = gpt4o.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        llm_response = response.choices[0].message.content
        token_count += len(gpt4o_encoder.encode(llm_response)) 
        try: 
            if re.findall(r"<title>(.*?)</title>", llm_response)[0] != title:
                title = re.findall(r"<title>(.*?)</title>", llm_response)[0]
                
        except Exception as E: 
            print(f"Caught the following response: {E} ")
            print(llm_response)
            plt.imshow(image)

        # validation for this response 

        validation_prompt = validation_prompt.format(system_msg, new_prompt, llm_response)
        text_messages[0]["content"][0]["text"] = system_msg
        text_messages[1]["content"][0]["text"] = validation_prompt
        response = gpt4o.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        validated_llm_response = response.choices[0].message.content
        token_count += len(gpt4o_encoder.encode(validated_llm_response)) 

        try: 
            output.append(validated_llm_response)
            if re.findall(r"<title>(.*?)</title>", output[-1])[0] != title:
                title = re.findall(r"<title>(.*?)</title>", output[-1])[0]
                
        except Exception as E: 
            print(f"Caught the following response: {E} ")
            print(validated_llm_response)
            plt.imshow(image)

    return output, token_count 


