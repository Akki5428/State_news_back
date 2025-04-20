from pydantic import BaseModel,Field,validator
from bson import ObjectId
from typing import Optional,Dict,Any
from datetime import datetime
import bcrypt


class User(BaseModel):
    firstName:str
    lastName:str
    email:str
    password:str
    pressId:Optional[str] = None
    organization:Optional[str] = None
    proofId:Optional[str] = None
    workLink:Optional[str] = None
    role_id:str
    created_at:datetime = datetime.utcnow()
    status:str = "pending"
    rejectReason:Optional[str] = None 
    
    @validator("password",pre=True,always=True)
    def encrypt_password(cls,v):
        if v is None:
            return None
        return bcrypt.hashpw(v.encode("utf-8"),bcrypt.gensalt())


class UserOut(User):
    id:str = Field(alias="_id")
    role:Optional[Dict[str,Any]] = None

    @validator("id",pre=True,always=True)
    def convert_id(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v

    @validator("role", pre=True, always=True)
    def convert_role(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])  # Convert role _id to string
        return v

class UserLogin(BaseModel):
    email:str
    password:str  

class RejectedUser(BaseModel):
    id:str
    rejectReason: Optional[str] = None  

    
        
