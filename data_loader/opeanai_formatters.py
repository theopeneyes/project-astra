from typing import Dict, List 

messages: List[Dict] = [
    {
      "role": "system", 
      "content": [
        {
          "type": "text", 
          "text": "Generate your answer in {} language.", 
        }, 
      ]
    }, 
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "", 
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,{}", 
          }
        }
      ]
    }
]