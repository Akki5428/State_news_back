from pydantic import BaseModel,Field,validator
from typing import List, Optional,Dict,Any
from bson import ObjectId
from datetime import datetime

class Achivment(BaseModel):
    userId: str
    badgeId: str
    earned_at: datetime = datetime.utcnow()

class AchivmentOut(Achivment):
    id:str = Field(alias="_id")


    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
    @validator("userId",pre=True,always=True)
    def convert_userId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
    @validator("badgeId",pre=True,always=True)
    def convert_badgeId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v

