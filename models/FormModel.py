from pydantic import BaseModel,Field,validator
from typing import List, Optional,Dict,Any
from bson import ObjectId
from datetime import datetime

class Advertise(BaseModel):
    fullName:str 
    email:str
    duration:str
    companyName:str
    placement:str
    adType:str
    message:Optional[str] = None
    created_at: datetime = datetime.utcnow()

class AdvertiseOut(Advertise):
    id:str = Field(alias="_id")

    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    