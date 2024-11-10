# huggingface client 
from huggingface_hub import InferenceClient 

# summarized document 
def summarize_texts(texts: str, language: str, token: str) -> str: 
    # TODO: Using an SLM to summarize the document, cannot make the language custom  
    client = InferenceClient(
        model="sshleifer/distilbart-cnn-12-6", 
        api_key=token
    )
    # summary output 
    return client.summarization(texts)["summary_text"]

