from typing import List, Dict 
from pprint import pprint 

def edit_metadata(final_json: List[Dict], 
                  heading_json: Dict, 
                  concept_json: Dict, 
                  topic_json: Dict, 
                ) -> List[Dict]: 

    edited_final_json: List[Dict] = []
    
    for _, js_object in enumerate(final_json): 
        try: 

            category: str = ('null' if (js_object['topic'] == None) or (js_object["topic"] == 'None') 
                             else js_object['topic']) 
            topic_count = topic_json[category]["count"]
            js_object["topic_word_count"] = topic_count 

        except Exception as e: 
            if "topic" in js_object:
                print("Topic: ", js_object["topic"])
                print("Topics listed in topics: ") 
                pprint(list(topic_json.keys())) 


        try: 

            category: str = ('null' if (js_object['concept'] == None) or (js_object["concept"] == 'None') 
                             else js_object['concept']) 
            concept_count = concept_json[category]["count"]
            js_object["concept_word_count"] = concept_count 

        except Exception as e: 
            if "concept" in js_object: 
                js_object["concept_word_count"] = 0
                print("Concept: ", js_object["concept"])
                print("Concepts listed in concepts: ") 
                pprint(list(concept_json.keys())) 

        try: 
            category: str = ('null' if (js_object['heading_text'] == None) or (js_object["heading_text"] == 'None') 
                             else js_object['heading_text']) 

            heading_count = heading_json[category]["count"]
            js_object["heading_word_count"] = heading_count 

        except Exception as e: 
            if "heading_text" in js_object: 
                js_object["heading_word_count"] = 0
                print("Headings: ", js_object["heading_text"])
                print("Headings listed in heading texts: ") 
                pprint(list(heading_json.keys())) 

        edited_final_json.append(js_object) 

    return edited_final_json

# blob = bucket.blob(os.path.join(
#     user_email, 
#     "final_json", 
#     f"{pdf_name}.json"
# ))    

# concept_blob = bucket.blob(os.path.join(
#     user_email, 
#     "books", 
#     pdf_name, 
#     "concept.json"
# ))

# topic_blob = bucket.blob(os.path.join(
#     user_email, 
#     "books", 
#     pdf_name, 
#     "topic.json"
# ))

# heading_text_blob = bucket.blob(os.path.join(
#     user_email, 
#     "books", 
#     pdf_name, 
#     "heading_text.json"
# ))

# with blob.open("r") as f: 
#     final_json = json.load(fp=f)

# with concept_blob.open("r") as f: 
#     concept_json = json.load(fp=f) 

# with topic_blob.open("r") as f: 
#     topic_json = json.load(fp=f) 

# with heading_text_blob.open("r") as f: 
#     heading_text = json.load(fp=f) 

# metadata = edit_metadata(final_json=final_json, heading_json=heading_text, concept_json=concept_json, topic_json=topic_json)

# with open("./machine_learning.json", "w") as f: 
#     json.dump(metadata, fp=f)

