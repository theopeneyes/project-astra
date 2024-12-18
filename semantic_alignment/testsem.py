from openai import OpenAI
from prompts import  snp2_revised
import ast
import os
from dotenv import load_dotenv
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

print() 
# ylist = ['Deep Learning', 'DL', 'Deep learning (DL)']
xlist = ['NLP', 'natural language processing', 'natural language processing (NLP)', 'Deep Learning', 'DL', 'Deep learning (DL)', 'activation functions', 'tanh']
# zlist = xlist.append(ylist)
# prompt = snp2.format(xlist)
def semantic_normalizer(value_list: list, ylist, prompt, client):
    # copy the list
    json_copy = value_list

    # de-duplicate it
    json_copy = list(dict.fromkeys(json_copy))

    prompt = snp2_revised.format(ylist)
    
    # get response from OpenAI API
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )

    
    try:
        # extract the actual output from API response
        y = completion.choices[0].message.content
        # convert the result(A string of a dict, hopefully) into the datatype dict
        z = ast.literal_eval(y)
        print(type(z))
        if(type(z)==dict):
            return z
        
    except Exception as e:
        print(e) # log the error
        return 
    
print(semantic_normalizer(xlist, xlist, snp2_revised, client=client))
    