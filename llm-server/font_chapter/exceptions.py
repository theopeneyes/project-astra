class CSSParsingException(Exception): 
    def __init__(self, message: str):
        self.message = message 
        super().__init__(f"CSSParsingException: {message}") 