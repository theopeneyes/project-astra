from .llms import llms 
from typing import List, Dict 


def generate_response(
    messages: List[Dict], 
    prompt: str, 
    topics: List[str], 
    context: List[str], 
    groqAi) -> str: 

    prompt = prompt.format(
        str(topics), 
        context.context, 
    )

    messages[0]["content"] = messages[0]["content"].format(context.language)
    messages[1]["content"] = messages[1]["content"].format(prompt)

    completion = groqAi.chat.completions.create(
        messages=messages, 
        model="mixtral-8x7b-32768"
    )
    return completion.choices[0].message.content



    