from typing import Dict, List 

def segregator(final_json: List) -> List[Dict]:  
    topics: Dict[str, str] = {} 
    concepts: Dict[str, str] = {} 
    headings: Dict[str, str] = {} 
    
    for _, js_object in enumerate(final_json):
        if "topic" in js_object.keys(): 
            topic_text = topics.get(js_object["topic"], "")
            topics[js_object["topic"]] = topic_text + js_object["text"] 
    
        if "heading_text" in js_object.keys(): 
            heading_text = headings.get(js_object["heading_text"], "")
            headings[js_object["heading_text"]] = heading_text + js_object["text"] 
    
        if "concept" in js_object.keys(): 
            concept_text = concepts.get(js_object["concept"], "")
            concepts[js_object["concept"] ]= concept_text + js_object["text"] 

    return [
        topics, 
        concepts, 
        headings, 
    ]