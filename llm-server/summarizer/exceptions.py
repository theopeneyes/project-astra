class SummaryNotFoundException(Exception): 
    llm_response: str 
    text_content: str 
    
    def __init__(self, llm_response: str, text_content: str): 
        self.llm_response = llm_response 
        self.text_content = text_content
        super().__init__(f"Could not find the summary tags in the response: {llm_response}. The text content found in the input: {text_content}")