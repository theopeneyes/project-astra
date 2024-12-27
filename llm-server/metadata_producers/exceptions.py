class AboutListNotGeneratedException(Exception): 
    llm_response: str 
    def __init__(self, llm_response: str): 
        self.llm_response = llm_response 
        super().__init__(f"About list was not generated. Here is the llm_response: {llm_response}")

class DepthListNotGeneratedException(Exception): 
    llm_response: str 
    def __init__(self, llm_response: str): 
        self.llm_response = llm_response 
        super().__init__(f"Depth list not generated. Here is the llm_response") 