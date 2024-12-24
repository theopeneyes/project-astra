from .prompts import identification_prompt
from .skeleton import message as messages 
from .exceptions import LLMTooDUMBException

import re 

def segment_breakdown(images: list, index_content: list[list[str]], last_page: int, first_page: int, gpt4o, gpt4o_encoder) -> list[dict|list|int]: 
    content_to_page: dict = {}
    content_to_df: list = [] 
    index: int = last_page - 1
    token_count: int = 0

    for _, index_item in enumerate(index_content):
        # within the book, look for the chapter
        section, title, heading_type, page_no = index_item
        if page_no != 'no-page-number': 
            assumed_page_number: int = int(page_no)
            start_index: int = first_page + assumed_page_number - 5
            end_index: int = start_index + 11
        else: 
            start_index: int = index + 1
            end_index: int = -1
        
        for j, image in enumerate(images[start_index:end_index]):
            index = j + start_index
            section = "" if section == 'no-section-number' else section 
            prompt: str = identification_prompt.format(title, section)
            messages[1]["content"][0]["text"] = prompt
            messages[1]["content"][1]["image_url"]["url"] = (
                f"data:image/jpeg;base64,{image['img_b64']}")

            completions = gpt4o.chat.completions.create(
                messages = messages,
                model = "gpt-4o",
                temperature=0.01
            )

            html_response: str = completions.choices[0].message.content
            token_count += len(gpt4o_encoder.encode(html_response))
            if re.findall(r"<contents>(.*?)</contents>", html_response, re.DOTALL):
                content = re.findall(r"<contents>(.*?)</contents>", html_response, re.DOTALL)[0]
                if content == "True":
                    content_to_page[title] = [section, index, heading_type]
                    content_to_df.append([title, section, index, heading_type]) 
                    break
            else: 
                raise LLMTooDUMBException(response=html_response)

    return content_to_df, content_to_page, token_count 