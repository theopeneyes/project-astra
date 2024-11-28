from pydantic import BaseModel 
from typing import List 

#Absolute underlying base model 
class AbsoluteBaseModel(BaseModel): 
    filename: str 
    email_id: str 

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
class SummarizationInputModel(AbsoluteBaseModel): 
    chapter_title: str 
    language: str 

class SummarizationOutputModel(AbsoluteBaseModel): 
    status: bool 
    token_count: int
    time: float 

# generation context model 
class GenerationContext(BaseModel): 
    topics: List[str]
    context: str
    question_type: str
    language: str

# encoded images list 
class EncodedImages(AbsoluteBaseModel): 
    images: List[str]

# Image model 
class DataMapPlotInputModel(BaseModel): 
    X_col: List[float]
    Y_col: List[float] 
    labels: List[str]
    
class DetectedLanguageModel(AbsoluteBaseModel): 
    detected_language: str
    time: float
    token_count: int
    
class GeneratedImageModel(BaseModel):
    encoded_image: str 

class SummaryChapterModel(AbsoluteBaseModel): 
    chapter_name: str 
    language: str 

class SummaryChapterOutputModel(SummaryChapterModel): 
    time: float 
    token_count: int 

class RewriteJSONFileModel(AbsoluteBaseModel):
    node_id: int  
    language: str 

class RewriteJSONFileOutputModel(RewriteJSONFileModel):
    time: float 
    token_count: int  

class ConvertPDFModel(AbsoluteBaseModel): 
    uri: str 

class ConvertPDFOutputModel(AbsoluteBaseModel): 
    uri: str 
    time: float # in seconds 

class PushToJSONModel(AbsoluteBaseModel): 
    time: float 

class SynthesisContentInputModel(AbsoluteBaseModel): 
    node_id: int 

class ModificationInputModel(AbsoluteBaseModel): 
    branch_name: str 

class ModificationOutputModel(ModificationInputModel):
    time: float 
    token_count: int 


class SynthesisContentInputModel(AbsoluteBaseModel): 
    node_id: int 
    branch_name: str

class SynthesisContentOutputModel(AbsoluteBaseModel): 
    node_id: int
    branch_name: str 
    time: float 
    token_count: int 

class MetaDataEditModel(AbsoluteBaseModel): 
    pass 

class MetaDataEditResponseModel(AbsoluteBaseModel): 
    time: float 
    
 