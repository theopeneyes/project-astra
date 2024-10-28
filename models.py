from pydantic import BaseModel 
from typing import List 

# sending uri's along with user email 
class DataLoaderModel(BaseModel): 
    email_id: str 
    uri: str 
    filename: str 

# output from data loader 
class StructuredJSONModel(BaseModel): 
    email_id: str 
    filename: str
    page_count: int 

# output from data classifier
class DataClassifierModel(BaseModel): 
    filename: str
    email_id: str 
    page_number: int 
    
# generation context model 
class GenerationContext(BaseModel): 
    topics: List[str]
    context: str
    question_type: str

# encoded images list 
class EncodedImages(BaseModel): 
    images: List[str]