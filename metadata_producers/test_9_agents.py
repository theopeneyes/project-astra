import os 
import re
import json
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
token = os.getenv("HF_TOKEN")
from data_loader.opeanai_formatters import text_message
from metadata_producers.test_9_prompts import *
from metadata_producers.test_validator import json_validator

# def topic_agent(single_json: dict,
#                 language: str,
#                 gpt4o_encoder,
#                 gpt4o,
#                 prompt=topic_prompt,
#                 flag=False, reason=None):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
    
#     if(flag==True):
#         text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["Topic"])
#     elif(flag==False):
#         text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["Topic"])


#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if(re.findall(r"<topic>(.*?)</topic>", llm_response, re.DOTALL)): 
#         summary = re.findall(r"<topic>(.*?)</topic>", llm_response, re.DOTALL)[0]
#         x = json.loads(summary)
#         if(json_validator(x, summary, "English", gpt4o_encoder, gpt4o, prompt=validator_prompt)["status"]==True):
#             print("returning because true")
#             return x
#         else:
#             print("trying to figure out, hold tight!")
#             return x 


# def topic_agent(single_json: dict,
#                 language: str,
#                 gpt4o_encoder,
#                 gpt4o,
#                 prompt,
#                 reason=None,
#                 count = 0):
    

#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["Topic"])
#     completion = gpt4o.chat.completions.create(
#         messages=text_message,
#         model="gpt-4o-mini",
#         temperature=0.1
#     )
#     llm_response = completion.choices[0].message.content
#     # print(llm_response)
#     token_count = len(gpt4o_encoder.encode(llm_response))

#     if(re.findall(r"<topic>(.*?)</topic>", llm_response, re.DOTALL)):
#         summary = re.findall(r"<topic>(.*?)</topic>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary)
        
#         if (type(single_json["Topic"])== list or dict):
#             isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)
#             if(isValid["status"]==True):
#                 return ans
#             else:
#                 if(count>=2):
#                     return ans
#                 else:
#                     count+=1
#                     ans = topic_agent(single_json, "English", gpt4o_encoder, gpt4o, reason=isValid["reason"], count=count+1)                
#         else:
#             return ans



# def concept_agent(single_json: dict,
#                 language: str,
#                 gpt4o_encoder,
#                 gpt4o, 
#                 prompt=concept_prompt, 
#                 reason=None,
#                 count=0):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["Concept"])

#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(r"<concept>(.*?)</concept>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<concept>(.*?)</concept>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary)
        
#         if (type(single_json["Concept"])== list or dict):
#             isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)
#             if(isValid["status"]==True):
#                 return ans
#             else:
#                 if(count>=2):
#                     return ans
#                 else:
#                     count+=1
#                     ans = concept_agent(single_json, "English", gpt4o_encoder, gpt4o, reason=isValid["reason"], count=count+1)

#         else:
#             return ans




# def subtopic_agent(single_json: dict, 
#                    language: str, 
#                    gpt4o_encoder, 
#                    gpt4o, 
#                    prompt=subtopic_prompt, 
#                    reason=None,
#                    count=0):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, single_json["Topic"], reason, single_json["text"], single_json["Sub topic"])
    
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(r"<subtopic>(.*?)</subtopic>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<subtopic>(.*?)</subtopic>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary)


#         if (type(single_json["Sub topic"])== list or dict):
#             isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)
#             if(isValid["status"]==True):
#                 return ans
#             else:
#                 if(count>=2):
#                     return ans
#                 else:    
#                     count+=1
#                     ans = subtopic_agent(single_json, "English", gpt4o_encoder, gpt4o, reason=isValid["reason"], count=count+1)

#         else:
#             return ans
        
# def subconcept_agent(single_json: dict, 
#                      language: str, 
#                      gpt4o_encoder, 
#                      gpt4o, 
#                      prompt=subconcept_prompt,
#                      reason=None,
#                      count=0):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, single_json["Concept"], reason, single_json["text"], single_json["Sub concept"])

#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(r"<subconcept>(.*?)</subconcept>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<subconcept>(.*?)</subconcept>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary) 
#         if (type(single_json["Sub concept"])== list or dict):
#             isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)
#             if(isValid["status"]==True):
#                 return ans
#             else:
#                 if(count>=2):
#                     return ans
#                 else:    
#                     count+=1
#                     ans = subconcept_agent(single_json, "English", gpt4o_encoder, gpt4o, reason=isValid["reason"], count=count+1)

#         else:
#             return ans

        


# def rootconcept_agent(single_json: dict, 
#                       language: str, 
#                       gpt4o_encoder, 
#                       gpt4o, 
#                       prompt=rootconcept_prompt, 
#                       reason=None,
#                       count=0):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["root_concept"])
    
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(r"<rootconcept>(.*?)</rootconcept>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<rootconcept>(.*?)</rootconcept>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary)
#         if (type(single_json["root_concept"])== list or dict):
#             isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)
#             if(isValid["status"]==True):
#                 return ans
#             else:
#                 pass
#                 if(count>=2):
#                     return ans
#                 else:    
#                     count+=1
#                     ans = rootconcept_agent(single_json, "English", gpt4o_encoder, gpt4o, reason=isValid["reason"], count=count+1)

#         else:
#             return ans



# def majordomains_agent(single_json: dict, 
#                        language:str, 
#                        gpt4o_encoder, 
#                        gpt4o, 
#                        prompt=majordomains_prompt,
#                        reason=None,
#                        count=0):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["major_domains"])
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(r"<majordomain>(.*?)</majordomain>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<majordomain>(.*?)</majordomain>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary)
#         if (type(single_json["major_domains"])== list or dict):
#             isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)

#             if(isValid["status"]==True):
#                 return ans
#             else:
#                 if(count>=2):
#                     return ans
#                 else:    
#                     count+=1
#                     ans = majordomains_agent(single_json, "English", gpt4o_encoder, gpt4o, reason=isValid["reason"], count=count+1)

#         else:
#             return ans






# def attributes_and_connections_agent(single_json: dict,
#                                     language: str, 
#                                     gpt4o_encoder, 
#                                     gpt4o, 
#                                     prompt=attributes_and_connections_prompt,
#                                     reason=None,
#                                     count=0):

#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["Attributes_and_connections"])
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(r"<aandcs>(.*?)</aandcs>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<aandcs>(.*?)</aandcs>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary)
#         if (type(single_json["Attributes_and_connections"])== list or dict):
#             isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)

#             if(isValid["status"]==True):
#                 return ans
#             else:
#                 if(count>=2):
#                     return ans
#                 else:    
#                     count+=1
#                     ans = attributes_and_connections_agent(single_json, "English", gpt4o_encoder, gpt4o, reason=isValid["reason"], count=count+1)
#         else:
#             return ans
    





# def classification_agent(single_json: dict, 
#                      agent_type: str, 
#                      language: str, 
#                      prompt: str, 
#                      gpt4o_encoder, 
#                      gpt4o, 
#                      reason=None):
#     '''
#     Functionality: Takes a json, classifies it, and verifies it, and if wrongly classified, re classifies it.
    
#     Input: the JSON, the metadata to be classified, prompt, gpt encoder, gpt4o

#     returns: the JSON itself after processing it.
#     '''       
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json[agent_type])
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    

#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(rf"<{agent_type}>(.*?)</{agent_type}>", llm_response, re.DOTALL): 
#         summary = re.findall(rf"<{agent_type}>(.*?)</{agent_type}>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary)
#         count: int = 0
#         status: bool = False 

#         while(count < 3 and not status): 

#             isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)
#             if isValid["status"] == "True": 
#                 status = True
#             else: 
#                 text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#                 text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json[agent_type])
#                 completion = gpt4o.chat.completions.create(
#                     messages=text_message, 
#                     model="gpt-4o-mini", 
#                     temperature=0.1
#                 )    

#                 llm_response = completion.choices[0].message.content
#                 token_count += len(gpt4o_encoder.encode(llm_response)) 

#                 if re.findall(rf"<{agent_type}>(.*?)</{agent_type}>", llm_response, re.DOTALL): 
#                     summary = re.findall(rf"<{agent_type}>(.*?)</{agent_type}>", llm_response, re.DOTALL)[0]
#                     ans = json.loads(summary)

#             count += 1
        
#     return ans, token_count  
        
# def formal_representations_agent(single_json: dict, 
#                                  language: str, 
#                                  gpt4o_encoder, 
#                                  gpt4o, 
#                                  prompt=formal_representations_prompt,
#                                  reason=None,
#                                  count=0):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["formal_representations"])
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(r"<formal>(.*?)</formal>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<formal>(.*?)</formal>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary)

#         if isinstance(single_json["formal_representations"], (list, dict)):
#             isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)
#             if(isValid["status"]==True):
#                 return ans
#             else:
#                 return ans
#                 print(isValid)
#                 print("75")
#                 if(count>=2):
#                     return ans
#                 else:    
#                     count+=1
#                     ans = formal_representations_agent(single_json, "English", gpt4o_encoder, gpt4o, reason=isValid["reason"], count=count+1)

#         else:
#             return ans



# def general_classification_agent(single_json: dict, 
#                                  language: str, 
#                                  gpt4o_encoder, 
#                                  gpt4o, 
#                                  prompt=formal_representations_prompt,
#                                  reason=None,
#                                  count=0):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"])
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 
#     print(llm_response)
#     if re.findall(r"<ctr>(.*?)</ctr>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<ctr>(.*?)</ctr>", llm_response, re.DOTALL)[0]
#         x = json.loads(summary)
#         return x
        
        
    
# def subgeneral_exercises_agent(single_json: dict, 
#                                language: str, 
#                                gpt4o_encoder, 
#                                gpt4o, 
#                                prompt=subgeneral_exercises_prompt,
#                                reason=None,
#                                count=0):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"])
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(r"<exercises-cls>(.*?)</exercises-cls>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<exercises-cls>(.*?)</exercises-cls>", llm_response, re.DOTALL)[0]
#         ans = json.loads(summary)
#         return ans
#         isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)
#         if(isValid["status"]==True):
#             return ans
#         else:
#             return ans
#             print(isValid)
#             print("75")
#             if(count>=2):
#                 return ans
#             else:    
#                 count+=1
#                 ans = formal_representations_agent(single_json, "English", gpt4o_encoder, gpt4o, reason=isValid["reason"], count=count+1)

#     else:
#         return ans

    



        

# def subgeneral_illustration_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=subgeneral_illustration_prompt):
#     text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
#     text_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"])
#     completion = gpt4o.chat.completions.create(
#         messages=text_message, 
#         model="gpt-4o-mini", 
#         temperature=0.1
#     )    
#     llm_response = completion.choices[0].message.content
#     token_count = len(gpt4o_encoder.encode(llm_response)) 

#     if re.findall(r"<illustration-cls>(.*?)</illustration-cls>", llm_response, re.DOTALL): 
#         summary = re.findall(r"<illustration-cls>(.*?)</illustration-cls>", llm_response, re.DOTALL)[0]
#         x = json.loads(summary)
#         return x

import re, json
def classification_agent(single_json: dict,
                     agent_type: str,
                     language: str,
                     prompt: str,
                     gpt4o_encoder,
                     gpt4o,
                     reason=None):
    '''
    Functionality: Takes a json, classifies it, and verifies it, and if wrongly classified, re classifies it.

    Input: the JSON, the metadata to be classified, prompt, gpt encoder, gpt4o

    returns: the JSON itself after processing it.
    '''
    text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
    text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json[agent_type])
    completion = gpt4o.chat.completions.create(
        messages=text_message,
        model="gpt-4o-mini",
        temperature=0.1
    )
    ans=None
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response))
    print(llm_response)
    if re.findall(rf"<{agent_type}>(.*?)</{agent_type}>", llm_response, re.DOTALL):
        summary = re.findall(rf"<{agent_type}>(.*?)</{agent_type}>", llm_response, re.DOTALL)[0]
        ans = json.loads(summary)
        count: int = 0
        status: bool = False
        print(ans)
        while(count < 3 and not status):

            isValid = json_validator(ans, "English", gpt4o_encoder, gpt4o)
            print(isValid)
            if isValid["status"] == "True":
                status = True
            else:
                text_message[0]["content"][0]["text"] = text_message[0]["content"][0]["text"].format(language)
                text_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json[agent_type])
                completion = gpt4o.chat.completions.create(
                    messages=text_message,
                    model="gpt-4o-mini",
                    temperature=0.1
                )

                llm_response = completion.choices[0].message.content
                token_count += len(gpt4o_encoder.encode(llm_response))

                if re.findall(rf"<{agent_type}>(.*?)</{agent_type}>", llm_response, re.DOTALL):
                    summary = re.findall(rf"<{agent_type}>(.*?)</{agent_type}>", llm_response, re.DOTALL)[0]
                    ans = json.loads(summary)

            count += 1

    return ans, token_count