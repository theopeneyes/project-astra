from pydantic import BaseModel 
from typing import List 

# generation context model 
class GenerationContext(BaseModel): 
    topics: List[str]
    context: str