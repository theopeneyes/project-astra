class EmptyPDFException(Exception):
    def __init__(self):
        super().__init__("Your PDF is empty. Upload a non-empty PDF, you noob")


class CorruptPDFException(Exception):
    def __init__(self):
        super().__init__("The PDF you uploaded is corrupt.")

class UnsupportedPDFException(Exception):
    def __init__(self):
        pass

class IncorrectGCPBucketException(Exception):
    def __init__(self):
        super().__init__("The PDF was uploaded in an incorrect storage bucket. Please re-upload")