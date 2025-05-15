import datetime 
import json 

def generate_qna_for_topic_sync(topic_name: str, texts: list[str], gpt4o, gpt4o_encoder):
    """
    Asynchronously generate question-answers for a given topic.
    
    Args:
        topic_name: The name of the topic
        texts: List of text contents for this topic
        gpt4o: gpt client 
        gpt4o_encoder: encoder to count tokens generated. 
        
    Returns:
        Tuple of (topic_name, generated_qna_data, completion_tokens, prompt_tokens)
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
    
    question_types = [
        "trueFalse", 
        "fillInTheBlanks", 
        "shortQuestionAnswer", 
        "multipleChoice", 
        "computationQuestion", 
        "softwareCodeQuestion"
    ]
    
    all_qna_data = []
    total_completion_tokens = 0
    total_prompt_tokens = 0
    
    for question_type in question_types:
        # Customize prompt based on question type
        options_instruction = ""
        json_format = ""
        
        if question_type == "multipleChoice":
            options_instruction = """
            For "multipleChoice": Create questions with 4 options (A, B, C, D) where only one is correct.
            The options should be provided as an array in the "options" field containing exactly 4 strings.
            """
            json_format = """
            [
                {"question": "...", "answer": "...", "question_type": "multipleChoice", "options": ["Option A", "Option B", "Option C", "Option D"]},
                {"question": "...", "answer": "...", "question_type": "multipleChoice", "options": ["Option A", "Option B", "Option C", "Option D"]},
                {"question": "...", "answer": "...", "question_type": "multipleChoice", "options": ["Option A", "Option B", "Option C", "Option D"]}
            ]
            """
        else:
            options_instruction = f"""
            For "{question_type}": Include an empty "options" array in the JSON response.
            """
            json_format = f"""
            [
                {{"question": "...", "answer": "...", "question_type": "{question_type}", "options": []}},
                {{"question": "...", "answer": "...", "question_type": "{question_type}", "options": []}},
                {{"question": "...", "answer": "...", "question_type": "{question_type}", "options": []}}
            ]
            """
        
        type_instructions = {
            "trueFalse": "Create true/false statements that test understanding of key concepts",
            "fillInTheBlanks": "Create sentences with key terms or concepts missing",
            "shortQuestionAnswer": "Create questions requiring brief explanatory answers",
            "multipleChoice": "Create questions with 4 options (A, B, C, D) where only one is correct",
            "computationQuestion": "Create questions requiring mathematical or logical calculations",
            "softwareCodeQuestion": "Create questions about code implementation, debugging, or optimization"
        }
        
        prompt = f"""
        I need you to generate 3 questions based on the following text about {topic_name}.
        
        The questions should be specifically of type: {question_type}
        
        Based on the question type:
        - {type_instructions[question_type]}
        {options_instruction}
        
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
        
        Here's the text:
        
        {text_for_processing}
        
        Generate exactly 3 questions of type {question_type} in the following JSON format:
        {json_format}
        
        Only return the JSON array without any additional text or explanations.
        """
        prompt_tokens = len(gpt4o_encoder.encode(prompt))
        total_prompt_tokens += prompt_tokens
        
        try:
            response = gpt4o.chat.completions.create(
                model="gpt-4o-mini",  
                temperature=0.1, 
                messages=[
                    {"role": "system", "content": "You are an expert at generating educational question-answer pairs from text content."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}  
            )
            qna_text = response.choices[0].message.content
            completion_tokens = len(gpt4o_encoder.encode(qna_text))
            total_completion_tokens += completion_tokens
            
            try:
                qna_data = json.loads(qna_text)
                
                if isinstance(qna_data, dict) and not isinstance(qna_data, list):
                    for _, value in qna_data.items():
                        if isinstance(value, list) and len(value) > 0:
                            qna_data = value
                            break
                
                for item in qna_data:
                    item["topic"] = topic_name
                    # Ensure question_type is set
                    item["question_type"] = question_type
                    # Ensure options exist
                    if "options" not in item:
                        item["options"] = [] if question_type != "multipleChoice" else ["Option A", "Option B", "Option C", "Option D"]
                    item["generated_at"] = datetime.datetime.now().isoformat()
                
                all_qna_data.extend(qna_data)
                
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for question type {question_type}")
                continue
                
        except Exception as err:
            print(f"Error occurred for question type {question_type}: {str(err)}")
            continue
    
    print(f"Generated {len(all_qna_data)} questions for topic: {topic_name}")
    
    return (topic_name, all_qna_data, total_completion_tokens, total_prompt_tokens)