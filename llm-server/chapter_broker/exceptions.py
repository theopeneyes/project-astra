
class LLMTooDUMBException(Exception):

    def __init__(self, response):
        self.response = response 
        (super()
        .__init__(f"Lmao, LLM could not create contents tags in the response: {response}"))
