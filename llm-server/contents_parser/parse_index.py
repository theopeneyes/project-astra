from .extract_index import extract_index
from .skeleton import content_parser_message as messages 
from .prompts import content_detection_prompt
from .exceptions import LLMTooDUMBException, IndexPageNotFoundException


import re 

def parse_index(images: list, number_of_pages: int, gpt4o, gpt4o_encoder): 
    """
    Inputs: 
    images: list -> List of all images extracted from the book. 
    number_of_pages: int -> First n pages to search for the index 
    gpt4o: openai client for text generation 

    Finds the index page and parses it for content of the book  
    """
    first_page: int  = 0 
    last_page: int = number_of_pages 
    contents_detected: bool = False
    token_count: int = 0 
    index_contents: list = []

    for idx, image in enumerate(images[:number_of_pages]):
        messages[1]["content"][0]["text"] = content_detection_prompt
        messages[1]["content"][1]["image_url"]["url"] = (
            f"data:image/jpeg;base64,{image['img_b64']}")

        completions = gpt4o.chat.completions.create(
            messages = messages,
            model = "gpt-4o",
            temperature=0.01
        )

        html_response: str = completions.choices[0].message.content
        token_count += len(gpt4o_encoder.encode(html_response)) 

        if re.findall(r"<contents>(.*?)</contents>", html_response):
            status : bool = re.findall(r"<contents>(.*?)</contents>", html_response)[0] == "True"
            if not contents_detected and status:
                # first contents page
                contents_detected = True
                first_page = idx 
                page_content, parsed_token_count = extract_index(image, gpt4o, gpt4o_encoder)
                token_count += parsed_token_count
                index_contents.extend(page_content)
            elif contents_detected and not status:
                contents_detected = False
                last_page = idx 
                break
            elif contents_detected: 
                page_content, parsed_token_count = extract_index(image, gpt4o, gpt4o_encoder)
                token_count += parsed_token_count
                index_contents.extend(page_content)
                
        else:
            raise LLMTooDUMBException(response=html_response)
        
    if not index_contents: 
        raise IndexPageNotFoundException(number_of_pages=number_of_pages)

    return first_page, last_page, index_contents, token_count 
