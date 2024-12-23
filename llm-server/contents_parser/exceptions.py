class LLMTooDUMBException(Exception):

    def __init__(self, response):
        self.response = response 
        (super()
        .__init__(f"Lmao, LLM could not create contents tags in the response: {response}"))

class IndexPageNotFoundException(Exception): 
    def __init__(self, number_of_pages): 
        self.number_of_pages = number_of_pages
        (super()
         .__init__(f"Index page was not found in the first {self.number_of_pages} pages"))