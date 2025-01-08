import pandas as pd 
from .prompts import text_extraction_prompt
from .skeleton import messages 

def load_chapters(
    chapter_name: str, 
    chapter_json: dict[list], 
    df: pd.DataFrame, 
    content: list[dict], 
    language_code: str, 
    gpt4o, gpt4o_encoder) -> list[str]: 
    chapter_name = chapter_name.split(".json")[0].split("_")[1]
    title, _, origin, _ = df.loc[df.title == chapter_name].values.tolist()[0]

    headings: list = chapter_json[title]

    if headings: 
        headings_df = pd.DataFrame(sorted(
            headings, key = lambda heading: heading[2]), 
            columns = ["title", "section_number", "idx", "heading_type"]
        )
    else: 
        headings_df: pd.DataFrame = pd.DataFrame(columns=["title", "section_number", "idx", "heading_type"])

    token_count: int = 0
    responses: list = []

    for idx, image in enumerate(content):   
        headings_on_this_page: list[list[str]] = [] 
        if (origin + idx)  in headings_df.idx.values.tolist():  
            headings_on_this_page = (headings_df.loc[headings_df.idx == (origin + idx)]
            [["section_number", "title"]].values.tolist()) 

        headings_page_form: list[str] = [ ] 
        
        for section, heading in headings_on_this_page: 
            if section == "None": 
                section = ""

            headings_page_form.append(f"{section} {heading}".strip()) 

        prompt: str = text_extraction_prompt.format(
            title, str(headings_page_form)  
        ) 

        messages[0]["content"][0]["text"] = f"Your output should be in the language associated with the following language code: {language_code}"  
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
        responses.append(html_response) 
    
    return responses, token_count 
        