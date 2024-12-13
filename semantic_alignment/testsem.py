from openai import OpenAI
from prompts import semantic_normalization_prompt, snp, snp2
import ast
import os
from dotenv import load_dotenv
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_key)
# ylist = ['Deep Learning', 'DL', 'Deep learning (DL)']
# xlist = ['NLP', 'natural language processing', 'natural language processing (NLP)', 'Deep Learning', 'DL', 'Deep learning (DL)', 'activation functions', 'tanh']
# zlist = xlist.append(ylist)
# prompt = snp2.format(xlist)




def semantic_normalizer(value_list: list, prompt=snp2, client=client):
    prompt = snp2.format(value_list)
    
    # get response from OpenAI API
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )

    # extract the actual output from API response
    y = completion.choices[0].message.content

    try:
        # convert the result(A string of a list, hopefully) into the datatype list
        z = ast.literal_eval(y)
        if(type(z)==list):
            return z
        
    except Exception as e:
        print(f"{e} occured!!")
        return 
    