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

# output from data classifier
class DataClassifierModel(AbsoluteBaseModel): 
    page_number: int 

# summarization model 
class SummarizationInputModel(AbsoluteBaseModel): 
    chapter_title: str 
    language: str 

class SummarizationOutputModel(AbsoluteBaseModel): 
    status: bool 

# generation context model 
class GenerationContext(AbsoluteBaseModel): 
    topics: List[str]
    context: str
    question_type: str

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
    
class GeneratedImageModel(BaseModel):
    encoded_image: str 

class SummaryChapterModel(AbsoluteBaseModel): 
    chapter_name: str 
    language: str 

class RewriteJSONFileModel(AbsoluteBaseModel):
    node_id: int  
    language: str 