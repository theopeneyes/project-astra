# this file will contain all the fastapi endpoints 
from fastapi import FastAPI 
from dotenv import load_dotenv # for the purposes of loading hidden environment variables
from prompt_design import prompts_csv # to get the collection of prompts  
from huggingface_hub import login 
from transformers import pipeline 
from transformers.pipelines.base import Pipeline 

import models as md
import pandas as pd 

import os 
import uvicorn

# loads the variables in the .env file 
load_dotenv()

# environment variables: configured in .env file
# these variables will be instantiated once the server starts and 
# the value won't be updated until you restart the server 
PROMPT_FILE_ID: str = os.getenv("FILE_ID", None) # file_id to fetch remote prompt design sheet
HF_TOKEN: str = os.getenv("HF_TOKEN", None)
MODEL: str = os.getenv("MODEL", None)

# model pipeline
pipe: Pipeline = pipeline(
    "text-generation", 
    md.SLM_MODELS[MODEL], 
    max_new_tokens=256, 
)

# prompt_design csv: 
PROMPT_DESIGN: pd.DataFrame = prompts_csv(PROMPT_FILE_ID) 

# logging in to huggingface with fine-grained token
login(token=HF_TOKEN)

# testing phase therefore `debug=True`
app = FastAPI(debug=True, title="project-astra")

#Endpoints 
@app.post("/get_classification")
def get_classification(hashcode: str) -> pd.DataFrame: 
    pass  

if __name__ == '__main__': 
    # add event listeners here 
    
    # launch server 
    uvicorn.run(port=4000)
    
