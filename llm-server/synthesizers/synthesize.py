from typing import Dict, Tuple
from .prompts import strength_prompt 
from .skeleton import text_messages as text_message 
import re 

def synthesizer(
        topic: str, 
        text: str, 
        gpt4o, 
        gpt4o_encoder, 
    ) -> Tuple[str| None, str | int, int]: 


    converter: Dict[str, int] = {
        "high": 3, 
        "medium": 2, 
        "low": 1, 
        "minimal detail": 1,
        "limited detail": 2,
        "moderately detail": 3,
        "substantial detail": 4,
        "exceptional detail": 5, 
        "not related": 1,
        "weakly related": 2,
        "moderately related": 3,
        "strongly related": 4,
        "directly and fully related": 5, 
        "": 0, 
    }

    score: str = ""
    text_message[1]["content"][0]["text"] = strength_prompt.format(topic, text)
    completion = gpt4o.chat.completions.create(
        messages=[text_message[1]],
        model="gpt-4o-mini",
        temperature=0.01
    )

    llm_response = completion.choices[0].message.content
    token_count = len(gpt4o_encoder.encode(llm_response)) 

    if re.findall(r"<score>(.*?)</score>", llm_response, re.DOTALL): 
        score = re.findall(r"<score>(.*?)</score>", llm_response, re.DOTALL)[0]
    else: 
        print("score was not found within llm response: ")
        print("view your llm response down below\n", llm_response)
    
    try:
        score = int(score)
    except Exception as _: 
        print("Could not cast the provided score as integer.")
        print("Here is the llm response")
        print(f"{llm_response}")
        print(f"Here is the score extracted: {score}")
        score = converter[score.lower()]
        
    
    if score == "": 
        return (None, llm_response, token_count) 
    else: 
        return ("done", score, token_count)  

