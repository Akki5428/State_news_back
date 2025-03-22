from fastapi import HTTPException
from models.CommentModel import Comment
from config.database import news_collection,comment_collection
from bson import ObjectId


async def interact_with_news(data: Comment):
    valid_interactions = ["Like", "Dislike", "Comment", "Report"]
    
    # Validate all interactions
    for interaction in data.interaction_type:
        if interaction not in valid_interactions:
            raise HTTPException(status_code=400, detail=f"Invalid interaction type: {interaction}")

    # Check if news exists
    news = await news_collection.find_one({"_id": ObjectId(data.newsId)})
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    
    if "Comment" in data.interaction_type:
        data.comment_text = data.comment_text
    else:
        data.comment_text = None
    
    res = await comment_collection.insert_one(data.dict())

    return {"message": "Interactions added successfully"}
