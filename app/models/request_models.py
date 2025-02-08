from pydantic import BaseModel
from typing import List

class UserRequest(BaseModel):
    category: List[str]
    gender: str
    age_group: str
    values: List[str]
    favorite_app: str
