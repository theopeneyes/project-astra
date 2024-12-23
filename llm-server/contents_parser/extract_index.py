import re 

from .exceptions import LLMTooDUMBException
from .prompts import index_breakdown_prompt
from .skeleton import content_parser_message as messages 
from html_table_parser import HTMLTableParser

def extract_index(image, gpt4o, gpt4o_encoder) -> list[list[str]]: 
    """
    Input: 
    image: Image of the contents page  
    gpt4o: Openai Client object 

    Functionality: 
    Convert all the identified index pages into a table of contents with identified chapter/sections/headings 
    as individual line items within the table. 
    """

    messages[1]["content"][0]["text"] = index_breakdown_prompt
    messages[1]["content"][1]["image_url"]["url"] = (
        f"data:image/jpeg;base64,{image['img_b64']}")

    completions = gpt4o.chat.completions.create(
        messages = messages,
        model = "gpt-4o",
        temperature=0.01
    )

    html_response: str = completions.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(html_response)) 

    if re.findall(r"<contents>(.*?)</contents>", html_response, re.DOTALL):
       content = re.findall(r"<contents>(.*?)</contents>", html_response, re.DOTALL)[0]
       parser = HTMLTableParser()
       parser.feed(content)
    else: 
        raise LLMTooDUMBException(response = html_response)
   
    # potential issue with the first column not being ["section number", "title", "page number"] 
    return parser.tables[0][1:], token_count
    

    

    
