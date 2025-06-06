from pydantic import BaseModel 
from fastapi import UploadFile
from typing import List 

#Absolute underlying base model 
class AbsoluteBaseModel(BaseModel): 
    filename: str 
    email_id: str 

class RequestModel(AbsoluteBaseModel):
    pass 

class ResponseModel(BaseModel): 
    time: float 
    token_count: int

# sending uri's along with user email 
class DataLoaderModel(AbsoluteBaseModel): 
    uri: str 
    language: str 

# output from data loader 
class StructuredJSONModel(AbsoluteBaseModel): 
    page_count: int 
    time: float 
    token_count: int 

# output from data classifier
class DataClassifierModel(AbsoluteBaseModel): 
    page_number: int 

# summarization model 
class SummarizationRequestModel(RequestModel): 
    chapter_name: str 
    language_code: str 

class SummarizationResponseModel(AbsoluteBaseModel, ResponseModel): 
    status: bool 

# generation context model 
class GenerationContext(AbsoluteBaseModel): 
    question_type: str
    chapter_name: str 
    topic_name: str 
    language: str

# encoded images list 
class EncodedImages(AbsoluteBaseModel): 
    images: List[str]

# Image model 
class DataMapPlotInputModel(BaseModel): 
    X_col: List[float]
    Y_col: List[float] 
    labels: List[str]
    
class DetectedLanguageResponseModel(AbsoluteBaseModel, ResponseModel): 
    detected_language: str
    confidence: float 
    
class GeneratedImageModel(BaseModel):
    encoded_image: str 

class SummaryChapterRequestModel(RequestModel): 
    chapter_name: str 
    language_code: str 

class SummaryChapterResponseModel(AbsoluteBaseModel, ResponseModel): 
    chapter_name: str 
    language_code: str 

class RewriteJSONRequestModel(RequestModel):
    node_id: int  
    language_code: str 
    chapter_name: str 

class RewriteJSONResponseModel(AbsoluteBaseModel, ResponseModel):
    language_code: str 
    node_id: int 

class ConvertPDFModel(AbsoluteBaseModel): 
    pass 

class ConvertPDFOutputModel(AbsoluteBaseModel): 
    time: float # in seconds 

class PushToJsonResponseModel(AbsoluteBaseModel): 
    time: float 

class SynthesisContentInputModel(AbsoluteBaseModel): 
    node_id: int 

class ModificationInputModel(AbsoluteBaseModel): 
    branch_name: str 

class ModificationOutputModel(ModificationInputModel):
    time: float 
    token_count: int 

class SynthesisContentRequestModel(RequestModel): 
    node_id: int 
    branch_name: str
    chapter_name: str 

class SynthesisContentResponseModel(AbsoluteBaseModel, ResponseModel): 
    node_id: int
    branch_name: str 

class MetaDataEditModel(AbsoluteBaseModel): 
    pass 

class MetaDataEditResponseModel(AbsoluteBaseModel): 
    time: float 
    
class LLMGenerationRequestModel(AbsoluteBaseModel):  
    language: str

class ContentsRequestModel(AbsoluteBaseModel): 
    number_of_pages: int 
    language_code: str 

class ContentsResponseModel(AbsoluteBaseModel): 
    first_page: int
    last_page: int 
    time: float
    token_count: int

class ChapterIdentificationRequestModel(AbsoluteBaseModel): 
    last_page: int 
    first_page: int 
    language_code: str 

class ChapterIdentificationResponseModel(AbsoluteBaseModel): 
    token_count: int 
    time: float 

class StatusRequestModel(BaseModel): 
    email_id: str 

class ReformRequestModel(AbsoluteBaseModel): 
    pass 

class ReformResponseModel(AbsoluteBaseModel): 
    time : float

class PDFUploadResponseModel(AbsoluteBaseModel): 
    time: float 

class ChapterLoaderRequestModel(AbsoluteBaseModel): 
    chapter_name: str 
    language_code: str 

class ChapterLoaderResponseModel(AbsoluteBaseModel, ResponseModel): 
    chapter_name: str 

class FontForChapterDetectionRequestModel(RequestModel): 
    pass 

class FontForChapterDetectionResponseModel(AbsoluteBaseModel, ResponseModel): 
    pass 

class JSONEditorRequestModel(RequestModel): 
    chapter_name: str
    node_id: int
    user_modified_json: str

class JSONEditorResponseModel(AbsoluteBaseModel, ResponseModel): 
    chapter_name: str 
    node_id: int

class TextNodeRequestModel(RequestModel): 
    chapter_name: str 
    node_id: int 


class TextNodeResponseModel(AbsoluteBaseModel): 
    chapter_name: str 
    node_id: int
    json_content: str
    time: float

class RectificationRequestModel(RequestModel): 
    chapter_name: str 

class RectificationResponseModel(AbsoluteBaseModel): 
    time: float 
    chapter_name: str 

class PdfPageCountRequestModel(RequestModel): 
    pass 

class PdfPageCountResponseModel(AbsoluteBaseModel): 
    time: float
    page_count : int 

class FinalBookListRequest(BaseModel): 
    email_id: str

class FinalBookListResponse(BaseModel): 
    email_id: str
    book_list: list[str]

class RunSubprocessRequest(BaseModel): 
    email_id: str 
    files: List[str] 

class SubprocessInitiatedResponse(BaseModel): 
    files: List[str]
    email_id: str 

class EmailRequest(BaseModel): 
    email: str

class QNATopicWiseRequest(BaseModel): 
    email_id: str 
    filename: str 

class GetExcelRequest(BaseModel): 
    email_id: str 
    filename: str 



