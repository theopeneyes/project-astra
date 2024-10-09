from typing import Dict  

#TODO: have a local folder to keep this models in a directory instead of downloading from 
# http everytime a request is made. 

SLM_MODELS: Dict[str, str] = {
    "gemma2b": "google/gemma-2-2b", # 2B parameters  
    "phi2":"microsoft/phi-2", # 2.7B parameters 
    "phi3.5":"microsoft/Phi-3.5-mini-instruct", # 3.8B parameters 
    "alibaba": "alibaba-pai/Qwen2-1.5B-Instruct-Exp", # 1.5B parameters 
    "granite": "ibm/PowerLM-3b",  # 3B parameters 
    "llama": "meta-llama/Llama-3.2-1B-Instruct" # 1B parameters 
} 
