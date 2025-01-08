class EmptyPDFException(Exception):
    def __init__(self):
        super().__init__("Your PDF is empty. Upload a non-empty PDF, you noob")