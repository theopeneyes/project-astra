content_parser_message: list[dict] = [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "",
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


content_parser_text_message: list[dict] = [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "",
        },
      ]
    }
]
