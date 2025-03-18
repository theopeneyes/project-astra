import datetime 
import json 

async def generate_qna_for_topic(topic_name: str, texts: list[str], gpt4o, gpt4o_encoder):
    """
    Asynchronously generate question-answers for a given topic.
    
    Args:
        topic_name: The name of the topic
        texts: List of text contents for this topic
        gpt4o: gpt client 
        gpt4o_encoder: encoder to count tokens generated. 
        
    Returns:
        Tuple of (topic_name, generated_qna_data)
    """

    combined_text = " ".join(texts)
    
    total_tokens = len(gpt4o_encoder.encode(combined_text))
    
    if total_tokens > 2000:
        truncated_text = combined_text
        while len(gpt4o_encoder.encode(truncated_text)) > 2000:
            truncated_text = truncated_text[:int(len(truncated_text) * 0.9)]
        
        text_for_processing = truncated_text
        input_tokens = len(gpt4o_encoder.encode(text_for_processing))
    else:
        text_for_processing = combined_text
        input_tokens = total_tokens
    
    prompt = f"""
    I need you to generate 10 question-answer pairs based on the following text about {topic_name}. 
    The questions should:
    1. Cover key concepts, facts, and insights from the text
    2. Be clearly answerable from the content provided
    3. Range from basic recall to more analytical or interpretive questions
    4. Be concise and focused
    
    The answers should:
    1. Be comprehensive yet concise
    2. Directly address the question asked
    3. Use information exclusively from the provided text
    4. Be factually accurate
    
    Please format your response as a JSON array of objects, where each object has a "question" field and an "answer" field.
    
    Here's the text:
    
    {text_for_processing}
    
    Generate exactly 10 question-answer pairs in the following JSON format:
    [
        {{"question": "What is...", "answer": "The text explains that..."}},
        ...and so on for all 10 pairs
    ]
    
    Only return the JSON array without any additional text or explanations.
    """
    prompt_tokens = len(gpt4o_encoder.encode(prompt))
    
    try:
        response = await gpt4o.chat.completions.create(
            model="gpt-4o-mini",  
            temperature=0.2, 
            messages=[
                {"role": "system", "content": "You are an expert at generating educational question-answer pairs from text content."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}  
        )
        qna_text = response.choices[0].message.content
        completion_tokens = len(gpt4o_encoder.encode(qna_text))
        qna_data = json.loads(qna_text)
        
        if isinstance(qna_data, dict) and not isinstance(qna_data, list):
            for key, value in qna_data.items():
                if isinstance(value, list) and len(value) > 0:
                    qna_data = value
                    break
        
        for item in qna_data:
            item["topic"] = topic_name
            item["generated_at"] = datetime.datetime.now().isoformat()
        
        return (topic_name, qna_data, completion_tokens, prompt_tokens)
        
    except Exception as e:
        return (topic_name, [])