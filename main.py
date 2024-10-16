# this file will contain all the fastapi endpoints 
from fastapi import FastAPI 
from dotenv import load_dotenv # for the purposes of loading hidden environment variables
from prompt_design import prompts_csv # to get the collection of prompts  

from typing import Dict, List 

import pandas as pd 
from google import generativeai as genai

import os 
import uvicorn

# loads the variables in the .env file 
load_dotenv()

# environment variables: configured in .env file
# these variables will be instantiated once the server starts and 
# the value won't be updated until you restart the server 
PROMPT_FILE_ID: str = os.getenv("FILE_ID", None) # file_id to fetch remote prompt design sheet
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", None) # gemini api key 
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", None) # openai api key 

genai.configure(api_key=GEMINI_API_KEY)

config = genai.GenerationConfig(
    temperature=0,
    top_p = 0.98,
    top_k = 5,
)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# prompt_design csv: 
PROMPT_DESIGN: pd.DataFrame = prompts_csv(PROMPT_FILE_ID) 

# testing phase therefore `debug=True`
app = FastAPI(debug=True, title="project-astra")

# logger 
def logger(response: Dict[str, str] | Exception):
    # posts this response or exception to a database that is meant to store logs 
    pass 

#Endpoints 
@app.post("/data_loader")
def data_loader() -> List[Dict[str, str| int]]: 
    pass 
    
if __name__ == '__main__': 
    # add event listeners here 
    
    # launch server 
    uvicorn.run(port=4000)
    
