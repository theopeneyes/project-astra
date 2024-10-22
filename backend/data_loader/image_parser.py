from google.generativeai.types import HarmCategory, HarmBlockThreshold
from matplotlib import pyplot as plt 
from image_utils.encoder  import encode_image
from image_utils.decoder import decode_image

from typing import List
import PIL 

import re

def parse_images(models: List, config,   
              images: List[str], prompt: str,
              clause_prompt: str,
              messages: List) -> List[str]:

    title: str | None = None
    new_prompt: str
    output: List[str] = []
     
    gemini, gpt4o = models 

    for _, image_encoded in enumerate(images):
        image: PIL.Image = decode_image(image_encoded) 

        if title:
            new_prompt = prompt.format(clause_prompt.format(title, "title"), "", "")
        else:
            new_prompt = prompt.format("", "", "")

        response = gemini.generate_content(
            [ new_prompt, image],
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
            },
            generation_config = config,
        )

        try:
            output.append(response.text)
            if re.findall(r"<title>(.*?)</title>", output[-1])[0] != title:
                title = re.findall(r"<title>(.*?)</title>", output[-1])[0]

        except Exception as e:
            messages[0]["content"][0]["text"] = new_prompt 
            messages[0]["content"][1]["image_url"]["url"] = (
                f"data:image/jpeg;base64,{encode_image(image)}") 

            response = gpt4o.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            try: 
                output.append(response.choices[0].message.content)
                if re.findall(r"<title>(.*?)</title>", output[-1])[0] != title:
                    title = re.findall(r"<title>(.*?)</title>", output[-1])[0]
                    
            except Exception as E: 
                plt.imshow(image)

    return output


