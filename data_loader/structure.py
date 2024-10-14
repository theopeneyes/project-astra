import pandas as pd 
from typing import List, Dict 

def structure_html(output: List[str]) -> pd.DataFrame: 
    """
    output: List[str] 
    A list of html documents converted from a pdf page using the
    Gemini API.  

    returns: pd.DataFrame 
    Structures the output as a DataFrame to send to the 
    Data Tagger and Organizer 
    """
    title: str| None = None 
    heading: str | None  = None 
    text: List[str] = []  
    table_on: bool = False 
    table_content: List[str]
    df_json : List[Dict[str, str]] = []
    
    for html_page in output: 
        paragraph_count: int = 0  
        for html_tag in html_page.split("\n"): 
            if html_tag.startswith('```'): continue  
            elif html_tag.startswith("<table"): 
                table_on = True 
                table_content = []
                continue 
            elif table_on and html_tag.startswith("</table>"): 
                table_on = False
                table_content = "\n".join(table_content)
                text = ['table', table_content]
            elif table_on: 
                table_content.append(html_tag)
                continue 
            elif ( html_tag.startswith('<title>') and html_tag.split(">")[1].split("<")[0] != title) :
                title = html_tag.split(">")[1].split("<")[0] 
                continue  
            elif ( html_tag.startswith("<h1>") and html_tag.split(">")[1].split("<")[0] != heading): 
                heading = html_tag.split(">")[1].split("<")[0]
                continue
            elif html_tag.startswith("<p>") :
                text = ['text', html_tag.split(">")[1].split("<")[0]] 
                paragraph_count += 1
            elif html_tag.startswith("<diagram>"): 
                text = ['diagram', html_tag.split(">")[1].split("<")[0]] 
            elif html_tag.startswith("<chart>"): 
                text = ['chart', html_tag.split(">")[1].split("<")[0]]
            else: 
                continue 

            df_json.append({
                "heading_identifier": title,
                "heading_text": heading,
                "text": text[1],
                "text_type": text[0], 
                "paragraph_number": paragraph_count
            })
        
    return pd.DataFrame(df_json)