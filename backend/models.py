from pydantic import BaseModel 
from fastapi.responses import Response 
from typing import List 

# generation context model 
class GenerationContext(BaseModel): 
    topics: List[str]
    context: str

# encoded images list 
class EncodedImages(BaseModel): 
    images: List[str]