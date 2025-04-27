from fastapi import HTTPException
from models.CommentModel import Comment,CommentOut
from config.database import news_collection,comment_collection,user_collection
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
    
    data = data.dict()
    # Insert the comment into the database
    data["newsId"] = ObjectId(data["newsId"])
    data["userId"] = ObjectId(data["userId"])
    data["rId"] = ObjectId(data["rId"])
    data["parentCommentId"] = ObjectId(data["parentCommentId"]) if data["parentCommentId"] else None
    res = await comment_collection.insert_one(data)
    
    return {"message": "Comment added successfully"}

async def get_all_comments():
    comments = await comment_collection.find().sort("created_at",-1).to_list()

    for c in comments:
        c["userId"] = str(c["userId"])
        c["newsId"] = str(c["newsId"])
        c["rId"] = str(c["rId"])
        c["parentCommentId"] = str(c["parentCommentId"]) if c["parentCommentId"] else None

        news = await news_collection.find_one({"_id": ObjectId(c["newsId"])})

        print(news)
        if news:
            news["_id"] = str(news["_id"])
            news["userId"] = str(news["userId"])
            news["stateId"] = str(news["stateId"])
            news["cityId"] = str(news["cityId"])
            c["news"] = news
        
        user = await user_collection.find_one({"_id": ObjectId(c["userId"])})
        if user:
            user["_id"] = str(user["_id"])
            user["role_id"] = str(user["role_id"])
            c["user"] = user
    return [CommentOut(**comment) for comment in comments]

async def get_recent_comments(id:str):
    comments = await comment_collection.find({"rId":ObjectId(id),"parentCommentId": None}).sort("created_at", -1).limit(5).to_list(5)
    for c in comments:
        c["userId"] = str(c["userId"])
        c["newsId"] = str(c["newsId"])
        c["rId"] = str(c["rId"])
        c["parentCommentId"] = str(c["parentCommentId"]) if c["parentCommentId"] else None

        news = await news_collection.find_one({"_id": ObjectId(c["newsId"])})
        if news:
            news["_id"] = str(news["_id"])
            news["userId"] = str(news["userId"])
            news["stateId"] = str(news["stateId"])
            news["cityId"] = str(news["cityId"])
            c["news"] = news
        
        user = await user_collection.find_one({"_id": ObjectId(c["userId"])})
        if user:
            user["_id"] = str(user["_id"])
            user["role_id"] = str(user["role_id"])
            c["user"] = user
    return [CommentOut(**comment) for comment in comments]

async def get_user_comments(id:str):
    comments = await comment_collection.find({"rId":ObjectId(id)}).sort("created_at", -1).to_list()
    for c in comments:
        c["userId"] = str(c["userId"])
        c["newsId"] = str(c["newsId"])
        c["rId"] = str(c["rId"])
        c["parentCommentId"] = str(c["parentCommentId"]) if c["parentCommentId"] else None

        news = await news_collection.find_one({"_id": ObjectId(c["newsId"])})
        if news:
            news["_id"] = str(news["_id"])
            news["userId"] = str(news["userId"])
            news["stateId"] = str(news["stateId"])
            news["cityId"] = str(news["cityId"])
            c["news"] = news
        
        user = await user_collection.find_one({"_id": ObjectId(c["userId"])})
        if user:
            user["_id"] = str(user["_id"])
            user["role_id"] = str(user["role_id"])
            c["user"] = user
    return [CommentOut(**comment) for comment in comments]

async def get_comment_by_news(id:str):
    news = await news_collection.find({"userId":ObjectId(id)}).to_list()
    result = []

    for n in news:
        news_id = str(n["_id"])
        comments = await comment_collection.find({"newsId":ObjectId(news_id)}).to_list()

        formatted_comments = []
        for c in comments:
            
            try:
                user = await user_collection.find_one({"_id":ObjectId(c["userId"])})
                user["_id"] = str(user["_id"])
                user["role_id"] = str(user["role_id"])
            except Exception as e:
                print(f"Error fetching user: {e}")
                user = None
            
            formatted_comments.append({
                "id": str(c["_id"]),
                "user": user,  # You can use c.get("userid", "Unknown") if unsure
                "text": c["comment_text"],
                "created_at": c["created_at"],
                "parentCommentId": str(c["parentCommentId"]),
            })


        result.append({
            "id": news_id,
            "title": n["title"],
            "comments": formatted_comments
        })

    return result

async def get_comment_by_news_only(id:str):
    # news = await news_collection.find({"_id":ObjectId(id)}).to_list()
    result = []

    # for n in news:
    news_id = str(id)
    comments = await comment_collection.find({"newsId":ObjectId(news_id)}).to_list()

    formatted_comments = []
    for c in comments:
            user = await user_collection.find_one({"_id":ObjectId(c["userId"])})
            user["_id"] = str(user["_id"])
            formatted_comments.append({
                "id": str(c["_id"]),
                "user": user,  # You can use c.get("userid", "Unknown") if unsure
                "text": c["comment_text"],
                "created_at": c["created_at"],
                "parentCommentId": str(c["parentCommentId"]),
            })


    result.append({
            "comments": formatted_comments
    })

    print(result)

    return result
