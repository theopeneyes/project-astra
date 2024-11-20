from metadata_producers.generate_list import generateList
from metadata_producers.prompts import about_list_generation_prompt,depth_list_generation_prompt, about_metadata_prompt, classification_prompt, general_classification_prompt
from metadata_producers.append_about_data import classify_about
from metadata_producers.general_classifier import general_classifier_test
from metadata_producers.sub_general_classification import sub_general_classifier_exercises, sub_general_classifier_illustration
from data_loader.opeanai_formatters import messages, summary_message
from metadata_producers.test_9_agents import *
from metadata_producers.test_9_prompts import *
from metadata_producers.test_validator import *
#####
import tiktoken
from openai import OpenAI

from tools.translation_nllb import nllb_translate
from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv("HF_TOKEN")
api_key = os.getenv("OPENAI_API_KEY")
gpt4o = OpenAI(api_key=api_key)
gpt4o_encoder = tiktoken.encoding_for_model("gpt-4o-mini")






# from metadata_producers.append_about_data import append_about
summary = '''Oxidation and reduction, often referred to together as redox reactions, are paired processes essential to many chemical and biological systems. In a redox reaction, one substance undergoes oxidation (loses electrons), while another undergoes reduction (gains electrons). This transfer of electrons alters the chemical structure and properties of the reacting species. For instance, in the reaction between hydrogen and oxygen, hydrogen is oxidized by losing electrons, and oxygen is reduced by gaining those electrons, forming water. Redox reactions are crucial in energy transfer within cells, particularly in processes like cellular respiration and photosynthesis, where they play a central role in ATP generation.

Oxidation is not limited to the gain of oxygen or loss of hydrogen, though historically, it was initially understood in that context. Modern chemistry defines oxidation as the loss of electrons, irrespective of whether oxygen is involved. This broader understanding applies to countless reactions across various fields, including industry and biological systems. For example, in batteries, redox reactions occur as the battery discharges, where one terminal experiences oxidation and the other reduction, generating electric current.

In everyday life, oxidation and reduction are evident in rusting iron, where iron oxidizes in the presence of oxygen and water to form iron oxide. The opposite reduction process is also observable in metallurgical refining, where metal ores are reduced to pure metals by removing oxygen. Redox reactions are thus integral to technological, environmental, and biological processes that impact both modern industry and life itself.
'''
# listgen = generateList(summary, about_list_generation_prompt, depth_list_generation_prompt, "English", summary_message, gpt4o_encoder, gpt4o)
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
jsonnnnn = {'heading_identifier': 'Oxidation', 'heading_text': 'diagram 4.1:', 'sub_heading_text': None, 'text_type': 'text', 'paragraph_number': 1, 'text': 'Experiment Design: Design a simple experiment to demonstrate a redox reaction using household items (e.g., vinegar and a steel wool pad). Explain how oxidation and reduction occur in your experiment.', 'Concept': 'Redox reactions', 'Sub concept': 'Involve electron transfer', 'Topic': 'Chemistry', 'Sub topic': 'Electron transfer in reactions', 'root_concept': 'Redox reactions', 'major_domains': 'Chemistry', 'sub_domains': 'Electron transfer', 'Attributes and connections': {'Redox reactions': ['Involve electron transfer', 'Result in oxidation and reduction', 'Alter chemical structure', 'Essential for energy transfer'], 'Oxidation': ['Loss of electrons', 'Can involve oxygen', 'Forms oxidized species'], 'Reduction': ['Gain of electrons', 'Can involve oxygen', 'Forms reduced species'], 'Electron transfer': ['Catalyzes redox reactions', 'Fundamental to redox chemistry'], 'Cellular respiration': ['Involves redox reactions', 'Generates ATP', 'Occurs in mitochondria'], 'Photosynthesis': ['Involves redox reactions', 'Converts light energy to chemical energy', 'Occurs in chloroplasts'], 'Battery technology': ['Utilizes redox reactions', 'Generates electric current', 'Involves electrodes'], 'Metallurgy': ['Involves redox reactions', 'Refines metals', 'Removes oxygen from ores']}, 'formal_representations': {'Diagram': 'Chemical equation', 'Model': 'Electron flow diagram'}, 'general_classification': 'Exercises'}


jsonnnn2 ={
    'concept': 'redox reactions',
    'sub_concept': 'oxidation and reduction processes',
    'topic': 'chemical and biological systems',
    'sub_topic': [
      'electron transfer',
      'cellular respiration',
      'photosynthesis',
      'energy transfer',
      'industrial applications',
      'rusting of iron',
      'metallurgical refining'
    ],
    'root_concept': 'Redox reactions',
    'major_domains': [
      'Chemistry',
      'Biochemistry',
      'Environmental Science',
      'Industrial Processes'
    ],
    'sub_domains': [
      'Oxidation',
      'Reduction',
      'Cellular Respiration',
      'Photosynthesis',
      'Battery Technology',
      'Metallurgical Refining'
    ],
    'Attributes and connections': {
      'Oxidation': [
        'Loss of electrons',
        'Gain of oxygen',
        'Loss of hydrogen'
      ],
      'Reduction': [
        'Gain of electrons',
        'Loss of oxygen',
        'Gain of hydrogen'
      ],
      'Applications': [
        'Energy transfer',
        'Electric current generation',
        'Rusting',
        'Metal refining'
      ]
    },
    'formal_representations': {
      'Chemical Equations': [
        'H2 + O2 -> H2O',
        'Fe + O2 + H2O -> Fe2O3'
      ],
      'Diagrams': [
        'Electron transfer diagrams',
        'Redox potential diagrams'
      ],
      'Models': [
        'Battery discharge model',
        'Cellular respiration model'
      ]
    }
  }


# #creating a json with all topics and shi
# fat_json = generateList(summary, about_list_generation_prompt,depth_list_generation_prompt, "English", summary_message, gpt4o_encoder, gpt4o)

# string = "પાંચ લીટર મોકલાવું મારા વ્હાલા?"

# # testes = nllb_translate(string, "Gujarati", "English")
# # print(testes)
# print(fat_json)

res = topic_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, topic_prompt)
print(res)

res2 = concept_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, concept_prompt)
print(res2)

res3 = subtopic_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, subtopic_prompt)
print(res3)

res4 = subconcept_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, subconcept_prompt)
print(res)

res5 = rootconcept_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, rootconcept_prompt)
print(res5)

res6 = majordomains_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, majordomains_prompt)
print(res6)

res7 = attributes_and_connections_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, attributes_and_connections_prompt)
print(res7)

res8 = subdomains_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, prompt=subdomains_prompt)
print(res8)

res9 = formal_representations_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, prompt=formal_representations_prompt)
print(res9)

res10 = general_classification_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, general_classification_prompt)
print(res10)

res11 = subgeneral_exercises_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, prompt=subgeneral_exercises_prompt)
print(res11)

res12 = subgeneral_illustration_agent(jsonnnnn, "English", gpt4o_encoder, gpt4o, prompt=subgeneral_illustration_prompt)
print(res12)


final_json = {**res, **res2, **res3, **res4, **res5, **res6, **res7, **res8, **res9, **res11, **res12}
print(final_json)


##############
print("==============================")
valid = json_validator(res6, summary, "English", gpt4o_encoder, gpt4o, validator_prompt, flag=False)
