from fastapi import HTTPException
from models.CommentModel import Comment,CommentOut
from config.database import news_collection,comment_collection
from bson import ObjectId


# async def interact_with_news(data: Comment):
#     valid_interactions = ["Like", "Dislike", "Comment", "Report"]
    
#     # Validate all interactions
#     for interaction in data.interaction_type:
#         if interaction not in valid_interactions:
#             raise HTTPException(status_code=400, detail=f"Invalid interaction type: {interaction}")

#     # Check if news exists
#     news = await news_collection.find_one({"_id": ObjectId(data.newsId)})
#     if not news:
#         raise HTTPException(status_code=404, detail="News not found")
    
#     if "Comment" in data.interaction_type:
#         data.comment_text = data.comment_text
#     else:
#         data.comment_text = None
    
#     res = await comment_collection.insert_one(data.dict())

#     return {"message": "Interactions added successfully"}

async def add_comment(data: Comment):
    news = await news_collection.find_one({"_id": ObjectId(data.newsId)})
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    
    # Insert the comment into the database
    res = await comment_collection.insert_one(data.dict())
    
    return {"message": "Comment added successfully"}

async def get_all_comments():
    comments = await comment_collection.find().sort("created_at",-1).to_list()

    for c in comments:
        c["userId"] = str(c["userId"])
        c["newsId"] = str(c["newsId"])
        c["rId"] = str(c["rId"])
    return [CommentOut(**comment) for comment in comments]

async def get_recent_comments(id:str):
    comments = await comment_collection.find({"rId":ObjectId(id)}).sort("created_at", -1).limit(5).to_list(5)
    for c in comments:
        c["userId"] = str(c["userId"])
        c["newsId"] = str(c["newsId"])
        c["rId"] = str(c["rId"])
    return [CommentOut(**comment) for comment in comments]
