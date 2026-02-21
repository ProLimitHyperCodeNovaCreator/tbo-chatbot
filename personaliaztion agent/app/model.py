from pydantic import BaseModel
from typing import List

class Option(BaseModel):
    option_id: str
    base_score: float
    price_bucket: str
    distance_bucket: str
    rating_bucket: str
    supplier_id: str
    refundable: bool

class PersonalizeRequest(BaseModel):
    user_id: str
    options: List[Option]
