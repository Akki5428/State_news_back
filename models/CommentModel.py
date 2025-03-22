from pydantic import BaseModel,Field,validator
from typing import List, Optional,Dict,Any
from bson import ObjectId
from datetime import datetime

class Comment(BaseModel):
    newsId: str
    userId: str
    interaction_type: List[str]
    comment_text: str
    created_at: datetime = datetime.utcnow()

class CommentOut(Comment):
    id:str = Field(alias="_id")

    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    