from pydantic import BaseModel,Field,validator
from typing import List, Optional,Dict,Any
from bson import ObjectId  
from datetime import datetime

class News(BaseModel):
    userId: str
    title: str
    content: str
    category: str
    stateId: str
    cityId: str
    images: Optional[List[str]] = None
    status: str = "inProgress"  # Default status when created
    rejectReason: Optional[str] = None
    approvedBy: Optional[str] = None
    api_source: Optional[str] = None
    news_date: datetime = datetime.utcnow()
    views: int = 0
    likes: int = 0
    commentsCount: int = 0
    isBreaking: bool = False # Admin marks this OR automated detection
    isTrending: bool = False # Based on engagement

class NewsOut(News):
    id : str = Field(alias="_id")
    city: Optional[Dict[str,Any]] = None
    state: Optional[Dict[str,Any]] = None
    user: Optional[Dict[str,Any]] = None

    @validator("id", pre=True, always=True) 
    def convert_objectId(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
class ApproveNews(BaseModel):
    status: str  # "published" or "rejected"
    adminId: str  # Admin user ID
    rejectReason: Optional[str] = None

class RejectedNews(BaseModel):
    id:str
    rejectReason: Optional[str] = None

class UpdateNewsRequest(BaseModel):
    id: str
    title: Optional[str] = None
    content: Optional[str] = None
    removeImages: Optional[List[str]] = []  # List of image URLs to remove

class UpdateNews_Request(BaseModel):
    id: str
    status:str
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    stateId: Optional[str] = None
    cityId: Optional[str] = None
    isBreaking: Optional[bool] = None
    removeImages: Optional[List[str]] = []  # URLs of images to remove
    newImages: Optional[List[str]] = [] 
    images: Optional[List[str]] = [] 
     # URLs of new images to add

