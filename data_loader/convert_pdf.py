from google import generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from matplotlib import pyplot as plt 

from typing import List

from IPython.display import Markdown 
import re
import os 
import PIL 

def parse_pdf(models: List, config, 
              image_dir: str, prompt: str,
              clause_prompt: str,
              name_of_pdf: str,
              error_dir: str) -> List[str]:

    title: str | None = None
    new_prompt: str
    output: List[str] = []

    gemini, gpt = models 

    for i, img in enumerate(os.listdir(image_dir)):
        image = genai.upload_file(
            path=os.path.join(image_dir, img),
            display_name = f"page {i}"
        )

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
            print("ERROR RUN PLEASE")
            Markdown(f"> got an error at page {i} " + str(e))
            plt.imshow(PIL.Image.open(os.path.join(image_dir, img)))
            plt.savefig(os.path.join(error_dir, f"{name_of_pdf}_page_{i}.jpg"))

        print(response.text)

    return output


