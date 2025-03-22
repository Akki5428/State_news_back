from pydantic import BaseModel,Field,validator
from bson import ObjectId


class Role(BaseModel):
    role:str

class RoleOut(Role):
    id:str = Field(alias="_id")

    @validator("id",pre=True,always=True)
    def convert_id(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v

    
        
