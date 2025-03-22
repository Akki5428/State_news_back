from pydantic import BaseModel,Field,validator
from typing import List, Optional,Dict,Any
from bson import ObjectId

class Badge(BaseModel):
    badgeName: str
    totalAcceptedNewsCount: int

class BadgeOut(Badge):
    id:str = Field(alias="_id")

    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v