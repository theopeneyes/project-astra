from metadata_producers.generate_list import generateList
from metadata_producers.prompts import about_list_generation_prompt,depth_list_generation_prompt, about_metadata_prompt, classification_prompt, general_classification_prompt
from metadata_producers.append_about_data import classify_about
from metadata_producers.general_classifier import general_classifier_test
from metadata_producers.sub_general_classification import sub_general_classifier_exercises, sub_general_classifier_illustration
from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv("HF_TOKEN")


from metadata_producers.append_about_data import append_about
summary = '''Oxidation and reduction, often referred to together as redox reactions, are paired processes essential to many chemical and biological systems. In a redox reaction, one substance undergoes oxidation (loses electrons), while another undergoes reduction (gains electrons). This transfer of electrons alters the chemical structure and properties of the reacting species. For instance, in the reaction between hydrogen and oxygen, hydrogen is oxidized by losing electrons, and oxygen is reduced by gaining those electrons, forming water. Redox reactions are crucial in energy transfer within cells, particularly in processes like cellular respiration and photosynthesis, where they play a central role in ATP generation.

Oxidation is not limited to the gain of oxygen or loss of hydrogen, though historically, it was initially understood in that context. Modern chemistry defines oxidation as the loss of electrons, irrespective of whether oxygen is involved. This broader understanding applies to countless reactions across various fields, including industry and biological systems. For example, in batteries, redox reactions occur as the battery discharges, where one terminal experiences oxidation and the other reduction, generating electric current.

In everyday life, oxidation and reduction are evident in rusting iron, where iron oxidizes in the presence of oxygen and water to form iron oxide. The opposite reduction process is also observable in metallurgical refining, where metal ores are reduced to pure metals by removing oxygen. Redox reactions are thus integral to technological, environmental, and biological processes that impact both modern industry and life itself.
'''
# listgen = generateList(summary=summary, about_list_generation_prompt=about_list_generation_prompt, depth_list_generation_prompt=depth_list_generation_prompt, language="english", token=token)
# print(listgen)

print("###########################################################")
json_list = {}
pratyush_json = {
        "heading_identifier":"Oxidation",
        "heading_text":"diagram 4.1:",
        "sub_heading_text":None,
        "text_type":"text",
        "paragraph_number":1,
        "text":''' 
        “The following chart illustrates the growth stages of a butterfly, from egg to adult, with each stage labeled and described.”
        '''
    }
jsonnnnn = {'heading_identifier': 'Oxidation', 'heading_text': 'diagram 4.1:', 'sub_heading_text': None, 'text_type': 'text', 'paragraph_number': 1, 'text': 'When iron is exposed to oxygen and water, it undergoes oxidation and forms iron oxide, commonly known as rust. This is a typical example of oxidation in metals', 'Concept': 'Redox reactions', 'Sub concept': 'Involve electron transfer', 'Topic': 'Chemistry', 'Sub topic': 'Electron transfer in reactions', 'root_concept': 'Redox reactions', 'major_domains': 'Chemistry', 'sub_domains': 'Electron transfer', 'Attributes and connections': {'Redox reactions': ['Involve electron transfer', 'Result in oxidation and reduction', 'Alter chemical structure', 'Essential for energy transfer'], 'Oxidation': ['Loss of electrons', 'Can involve oxygen', 'Forms oxidized species'], 'Reduction': ['Gain of electrons', 'Can involve oxygen', 'Forms reduced species'], 'Electron transfer': ['Catalyzes redox reactions', 'Fundamental to redox chemistry'], 'Cellular respiration': ['Involves redox reactions', 'Generates ATP', 'Occurs in mitochondria'], 'Photosynthesis': ['Involves redox reactions', 'Converts light energy to chemical energy', 'Occurs in chloroplasts'], 'Battery technology': ['Utilizes redox reactions', 'Generates electric current', 'Involves electrodes'], 'Metallurgy': ['Involves redox reactions', 'Refines metals', 'Removes oxygen from ores']}, 'formal_representations': {'Diagram': 'Chemical equation', 'Model': 'Electron flow diagram'}, 'general_classification': 'Exercises'}

# classified = classify_about(token=token, single_json=pratyush_json, generated_list=listgen, classification_prompt=classification_prompt, language="english")

# print(classified)
    
# general = general_classifier_test(classified)
# print(general)

# exercises_cls = sub_general_classifier_exercises(jsonnnnn)
# print(exercises_cls)
illustration_cls = sub_general_classifier_illustration(jsonnnnn)
print(illustration_cls)