from pydantic import BaseModel
from typing import List, Optional

class Attraction(BaseModel):
    id: int
    name: str
    category: str
    description: str
    address: str
    transport: str
    mrt: str
    lat: float
    lng: float
    images: List[str]

class AttractionResponse(BaseModel):
    nextPage: Optional[int]
    data: List[Attraction]

class MRTResponse(BaseModel):
    data: List[str]

class ErrorResponse(BaseModel):
    error: bool
    message: str
