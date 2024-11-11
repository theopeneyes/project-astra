from metadata_producers.generate_list import generateList
from metadata_producers.prompts import about_list_generation_prompt,depth_list_generation_prompt, about_metadata_prompt, classification_prompt
from metadata_producers.append_about_data import classify_about
from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv("HF_TOKEN")


from metadata_producers.append_about_data import append_about
summary = "A carburettor is a component in internal combustion engines that combines air and fuel to enable combustion. It operates by pulling in air through an intake, generating a vacuum that draws fuel into the air stream through a nozzle. This mixture of fuel and air is then sent to the engine's cylinders for ignition. The carburettor regulates fuel intake based on engine demand, ensuring efficient combustion. While widely used in older engines, carburettors have been mostly replaced by fuel injection systems, which provide greater accuracy in fuel delivery, enhancing engine efficiency and lowering emissions."

listgen = generateList(summary=summary, about_list_generation_prompt=about_list_generation_prompt, depth_list_generation_prompt=depth_list_generation_prompt, language="english", token=token)
print(listgen)

print("###########################################################")
json_list = {}
pratyush_json = {
        "heading_identifier":"Carburetor",
        "heading_text":"Introduction",
        "sub_heading_text":None,
        "text_type":"text",
        "paragraph_number":1,
        "text":"A carburettor is a device in internal combustion engines that mixes air and fuel for combustion. It functions by drawing in air through the intake, creating a vacuum that pulls fuel into the airflow via a nozzle. This air-fuel mixture is then directed to the engine cylinders for ignition. The carburettor adjusts fuel flow based on engine speed and load, optimizing combustion efficiency. Although common in older engines, carburettors are largely replaced by fuel injection systems, which offer more precise control over fuel delivery, improving performance and reducing emissions."
    }

classified = classify_about(token=token, single_json=pratyush_json, generated_list=listgen, classification_prompt=classification_prompt, language="english")

print(classified)