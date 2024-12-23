from typing import Dict, List 

image_message: List[Dict] = [
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

text_message: str = [
  {
    "role": "system", 
    "content": [{
      "type": "text", 
      "text": "Generate the output in {} language."
    }]
  }, 
  
  {
    "role": "user", 
    "content": [{
      "type": "text", 
      "text": ""
    }]
  }
]
