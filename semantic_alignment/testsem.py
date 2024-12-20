from openai import OpenAI
from prompts import  snp2_revised
import json
import os
import re
from dotenv import load_dotenv
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)



# ylist = ['Deep Learning', 'DL', 'Deep learning (DL)']
xlist = ['Machine learning', 'Machine Learning (ML)', 'ML', 'neurons']
# zlist = xlist.append(ylist)
# prompt = snp2.format(xlist)
def semantic_normalizer(value_list: list, prompt, client):
    # copy the list
    json_copy = value_list

    # de-duplicate it
    json_copy = list(dict.fromkeys(json_copy))

    prompt = snp2_revised.format(value_list)
    
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

        # extract json from string of output using regex.
        match = re.search(r'\{.*\}', y, re.DOTALL)
        
        if match:
            json_string = match.group(0)
        else:
            print("Regex is stupid and couldnt do its job.")
            return


        # convert the result(A string of a dict, hopefully) into the datatype dict
        z = json.loads(json_string)
        return z
        
    except Exception as e:
        print(e) # log the error
        print("Error encountered from the result sent by OpenAI. cant do anything here")
        return 
    

updated_list = []
for item in xlist:
    normalized_value = abs.get(item, item)  # Get normalized value or keep the original if not in the map
    updated_list.append(normalized_value)
    
# print(updated_list)