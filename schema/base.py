import pydantic
from typing import Optional

class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True

class BaseId(BaseModel):
    id: Optional[int]

class RequiredBaseId(BaseModel):
    id: int