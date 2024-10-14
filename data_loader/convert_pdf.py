from google import generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from typing import List
from prompts import (
    prompt, clause_prompt 
)

from IPython.display import Markdown 
import re

def parse_chapter(images: List, config, model) -> List[str]:
    title: str | None = None
    new_prompt: str
    output: List[str]

    for i, img in enumerate(images): 
        image = genai.upload_file(
            path=img,
            display_name = f"page {i}"
        )

        if title:
            new_prompt = prompt.format(clause_prompt.format(title))
        else:
            new_prompt = prompt.format("")

        response = model.generate_content(
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
        except ValueError as ve:
            Markdown(f"> got an error at page {i} " + str(ve))

        if re.findall(r"<title>(.*?)</title>", output[-1])[0] != title:
            title = re.findall(r"<title>(.*?)</title>", output[-1])[0]

    return output

