from metadata_producers.test_9_prompts import *
from metadata_producers.test_9_agents import *
from data_loader.opeanai_formatters import text_message
import re
import json

# def json_validator(single_json: dict,summary:str, language: str, gpt4o_encoder, gpt4o, prompt, flag=True, reason=None):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, single_json, summary)
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     # print(llm_response)
#     if re.findall(r"<validator>(.*?)</validator>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<validator>(.*?)</validator>", llm_response, re.DOTALL)[0]
#         x = json.loads(summary)
#         return x
#         # print(x)


summary_x = '''Oxidation and reduction, often referred to together as redox reactions, are paired processes essential to many chemical and biological systems. In a redox reaction, one substance undergoes oxidation (loses electrons), while another undergoes reduction (gains electrons). This transfer of electrons alters the chemical structure and properties of the reacting species. For instance, in the reaction between hydrogen and oxygen, hydrogen is oxidized by losing electrons, and oxygen is reduced by gaining those electrons, forming water. Redox reactions are crucial in energy transfer within cells, particularly in processes like cellular respiration and photosynthesis, where they play a central role in ATP generation.

Oxidation is not limited to the gain of oxygen or loss of hydrogen, though historically, it was initially understood in that context. Modern chemistry defines oxidation as the loss of electrons, irrespective of whether oxygen is involved. This broader understanding applies to countless reactions across various fields, including industry and biological systems. For example, in batteries, redox reactions occur as the battery discharges, where one terminal experiences oxidation and the other reduction, generating electric current.

In everyday life, oxidation and reduction are evident in rusting iron, where iron oxidizes in the presence of oxygen and water to form iron oxide. The opposite reduction process is also observable in metallurgical refining, where metal ores are reduced to pure metals by removing oxygen. Redox reactions are thus integral to technological, environmental, and biological processes that impact both modern industry and life itself.
'''



def json_validator(single_json: dict,
                   language: str,
                   gpt4o_encoder,
                   gpt4o,
                   summary=summary_x,
                   prompt=validator_prompt,
                   reason=None):
    text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
    text_message[1]["content"][0]["text"] = prompt.format(language, single_json, summary)

    completion = gpt4o.chat.completions.create(
        messages=text_message,
        model="gpt-4o-mini",
        temperature=0.1
    )
    llm_response = completion.choices[0].message.content
    if re.findall(r"<validator>(.*?)</validator>", llm_response, re.DOTALL):
        summary = re.findall(r"<validator>(.*?)</validator>", llm_response, re.DOTALL)[0]
        ans = json.loads(summary)
        return ans

#         # x = {status: True/False,
#         #      reason: "blah blah blah"
#         #}