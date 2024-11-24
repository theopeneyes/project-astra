from typing import List, Dict 

def edit_metadata(final_json: List[Dict], 
                  heading_json: Dict, 
                  concept_json: Dict, 
                  topic_json: Dict, 
                ) -> List[Dict]: 

    edited_final_json: List[Dict] = []
    
    for _, js_object in enumerate(final_json): 
        try: 
            topic_count = topic_json[js_object["topic"]]["count"]
            heading_count = heading_json[js_object["heading_text"]]["count"]
            concept_count = concept_json[js_object["concept"]]["count"]

            js_object["topic_word_count"] = topic_count 
            js_object["concept_word_count"] = concept_count
            js_object["heading_word_count"] = heading_count 

            edited_final_json.append(js_object)
        except Exception as e: 
            print("Error occured bro")
            pass 
    
    return edited_final_json
    
    



