import requests 
from typing import Dict 

FILE_ID: str = '1kTXuGtEUyZDrb4g7-2MxiXBgWW9WBaJT'
def download_secrets(file_id : str) -> Dict[str, str] : 
    URL: str  = f"https://drive.google.com/uc?id={file_id}" 

    # get the string content 
    content = requests.get(url=URL).content.decode("utf-8")
    secrets: Dict[str, str] = {}
    for items in content.split("\n"): 
        if "=" in items: 
            key_name, secret = items.split("=")
            secrets[key_name] = secret 

    return secrets 
    

