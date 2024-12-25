messages: list[dict] = [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Generate your answer in English language.",
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


text_messages: list[dict] = [
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
