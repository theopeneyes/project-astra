# huggingface client 
from huggingface_hub import InferenceClient 
from typing import List

# summarized document 
def summarize_texts(texts: str, token: str) -> str: 
    client = InferenceClient(
        model="sshleifer/distilbart-cnn-12-6", 
        api_key=token
    )
    # summary output 
    return client.summarization(texts)["summary_text"]

