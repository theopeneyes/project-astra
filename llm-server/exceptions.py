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

class FileTooLargeException(Exception):
    def __init__(self):
        super().__init__("The file size is too large to be processed within the given lead time.")
        
class PDFNetworkIssue(Exception):
    def __inti__(self):
        super().__init__("PDF not uploded due to network Problem, Kindly reuplode it ")

# class EmptyPDFException(Exception):
#     def __init__(self):
#         super().__init__("Your PDF is empty. Upload a non-empty PDF, you noob")

class SavePDFExeption(Exception):
    def __init__(self):
        super().__init__("Voila! Your PDF didn't save.")

class InvalidPDFExeption(Exception):
    def __init__(self):
        super().__init__("Your PDf is not valid.Uplod a valid PDF")

class ConversionTimeoutExeption(Exception):
    def __init__(self):
        super().__init__("your PDF is Too Large To use or Too Complex, Use a Simpler One")

class UnsupportedContentExeption(Exception):
    def __init__(self):
        super().__init__("Your PDf contains Unsupported Element, ether remove it or Uplde new one")

class APILimitsExeption(Exception):
    def __init__(self):
        super().__init__("API Rate Limit exceeded. Please try again later.")

class PageCountMismatchException(Exception):
    def __init__(self):
        super().__init__("The number of images does not match the number of pages in the PDF.")

class InvalidImageFormatException(Exception):
    def __init__(self):
        super().__init__("The images are in an invalid or inconsistent format. Please use Other.")

class InsufficientPermissionsException(Exception):
    def __init__(self):
        super().__init__("Insufficient permissions to write to the storage bucket. Please check your access rights.")

class ImageSaveFailureException(Exception):
    def __init__(self):
        super().__init__("The image could not be saved due to network issues or failures. Please try again.")

class MissingImagesException(Exception):
    def __init__(self):
        super().__init__("Some pages were not converted to images. Please check the conversion process.")

class IncorrectImageFormatException(Exception):
    def __init__(self):
        super().__init__("The image resolution or format is incorrect. Please ensure consistency across all pages.")

class PartialImageException(Exception):
    def __init__(self):
        super().__init__("Some images are only partial, not representing the full page. Please check the conversion process.")

class CorruptedImageFileException(Exception):
    def __init__(self):
        super().__init__("The image files are corrupted or unreadable after conversion. Please try again.")

class ErrorHandlingFailureException(Exception):
    def __init__(self):
        super().__init__("Error handling failed during the process. Please check the system's error handling mechanisms.")

class NotificationAndLogsException(Exception):
    def __init__(self):
        super().__init__("Notification or logging failed. Please check the system's logging and notification mechanisms.")
        
class HandlingMixedLangException(Exception):
    def __init__(self):
        super().__init__("The PDF contains multiple languages. Please upload a PDF with a single language.")