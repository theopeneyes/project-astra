import os 
import re
import json
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
token = os.getenv("HF_TOKEN")
from data_loader.opeanai_formatters import summary_message
from metadata_producers.test_9_prompts import *
from metadata_producers.test_validator import *

def topic_agent(single_json: dict,language: str, gpt4o_encoder, gpt4o,  prompt=topic_prompt, flag=True):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    
    if(flag==True):
        summary_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["Topic"])
    elif(flag==False):
        summary_message[1]["content"][0]["text"] = prompt.format(language, reason, single_json["text"], single_json["Topic"])


    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<topic>(.*?)</topic>", llm_response, re.DOTALL): 
        summary = re.findall(r"<topic>(.*?)</topic>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        if(json_validator(x, summary, "English", gpt4o_encoder, gpt4o, prompt=validator_prompt)["status"]==True):
            print("returning because true")
            return x
        else:
            print("trying to figure out, hold tight!")
            return x 

def concept_agent(single_json: dict,language: str, gpt4o_encoder, gpt4o,  prompt=concept_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"], single_json["Concept"])
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<concept>(.*?)</concept>", llm_response, re.DOTALL): 
        summary = re.findall(r"<concept>(.*?)</concept>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x


def subtopic_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=subtopic_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["Topic"], single_json["text"], single_json["Sub topic"] )
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<subtopic>(.*?)</subtopic>", llm_response, re.DOTALL): 
        summary = re.findall(r"<subtopic>(.*?)</subtopic>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x

def subconcept_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=subconcept_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["Concept"], single_json["text"], single_json["Sub concept"] )
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<subconcept>(.*?)</subconcept>", llm_response, re.DOTALL): 
        summary = re.findall(r"<subconcept>(.*?)</subconcept>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x


def rootconcept_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=rootconcept_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"], single_json["root_concept"])
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<rootconcept>(.*?)</rootconcept>", llm_response, re.DOTALL): 
        summary = re.findall(r"<rootconcept>(.*?)</rootconcept>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x


def majordomains_agent(single_json: dict, language:str, gpt4o_encoder, gpt4o, prompt=majordomains_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"], single_json["major_domains"])
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<majordomain>(.*?)</majordomain>", llm_response, re.DOTALL): 
        summary = re.findall(r"<majordomain>(.*?)</majordomain>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x

def attributes_and_connections_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=attributes_and_connections_prompt):

    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"], single_json["Attributes and connections"])
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<aandcs>(.*?)</aandcs>", llm_response, re.DOTALL): 
        summary = re.findall(r"<aandcs>(.*?)</aandcs>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x



def subdomains_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=subdomains_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"], single_json["sub_domains"])
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<subdomains>(.*?)</subdomains>", llm_response, re.DOTALL): 
        summary = re.findall(r"<subdomains>(.*?)</subdomains>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x

def formal_representations_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=formal_representations_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"], single_json["formal_representations"])
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<formal>(.*?)</formal>", llm_response, re.DOTALL): 
        summary = re.findall(r"<formal>(.*?)</formal>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x

def general_classification_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=formal_representations_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"])
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<category>(.*?)</category>", llm_response, re.DOTALL): 
        summary = re.findall(r"<category>(.*?)</category>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x
    
def subgeneral_exercises_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=subgeneral_exercises_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"])
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<exercises-cls>(.*?)</exercises-cls>", llm_response, re.DOTALL): 
        summary = re.findall(r"<exercises-cls>(.*?)</exercises-cls>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x

def subgeneral_illustration_agent(single_json: dict, language: str, gpt4o_encoder, gpt4o, prompt=subgeneral_illustration_prompt):
    summary_message[0]["content"][0]["text"] = summary_message[0]["content"][0]["text"].format(language)
    summary_message[1]["content"][0]["text"] = prompt.format(language, single_json["text"])
    completion = gpt4o.chat.completions.create(
        messages=summary_message, 
        model="gpt-4o-mini", 
        temperature=0.1
    )    
    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<illustration-cls>(.*?)</illustration-cls>", llm_response, re.DOTALL): 
        summary = re.findall(r"<illustration-cls>(.*?)</illustration-cls>", llm_response, re.DOTALL)[0]
        x = json.loads(summary)
        return x