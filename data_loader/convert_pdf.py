from google.generativeai.types import HarmCategory, HarmBlockThreshold
from matplotlib import pyplot as plt 

from typing import List

import re
import os 
import PIL 
import streamlit 

import base64
import pdf2image as p2i 
from io import BytesIO

def encode_image(image: PIL.Image): 
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def parse_pdf(models: List, config,   
              pdf_path: str, prompt: str,
              clause_prompt: str,
              name_of_pdf: str,
              error_dir: str, 
              messages: List) -> List[str]:

    title: str | None = None
    new_prompt: str
    output: List[str] = []

    images: List[PIL.Image] = p2i.convert_from_path(
        pdf_path,
        dpi=200,
    )

     
    gemini, gpt4o = models 

    for i, image in enumerate(images):

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
                plt.savefig(os.path.join(error_dir, f"{name_of_pdf}_page_{i}.jpg"))

    return output


