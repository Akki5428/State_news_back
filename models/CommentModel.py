from pydantic import BaseModel,Field,validator
from typing import List, Optional,Dict,Any
from bson import ObjectId
from datetime import datetime

class Comment(BaseModel):
    newsId: str
    userId: str
    rId: str
    # interaction_type: List[str]
    comment_text: str
    created_at: datetime = datetime.utcnow()

class CommentOut(Comment):
    id:str = Field(alias="_id")
    news: Optional[Dict[str,Any]] = None
    user: Optional[Dict[str,Any]] = None

    @validator("id",pre=True,always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    