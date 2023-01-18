from pydantic import BaseModel
from typing import Optional, List, Dict
class Car(BaseModel):
    make: Optional[str]
    model: Optional[str]
    year: Optional[int] 
    price: Optional[float]
    engine: Optional[str] = "V4"
    autonomous: Optional[bool]
    sold: Optional[List[str]]
