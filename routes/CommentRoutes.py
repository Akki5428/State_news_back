from fastapi import APIRouter
from models.CommentModel import Comment 
from controllers.CommentController import add_comment,get_all_comments,get_recent_comments

router = APIRouter()

# @router.post("/news/interact")
# async def news_interaction(data: Comment):
#     return await interact_with_news(data)

@router.post("/comment/add")
async def addComment(data: Comment):
    return await add_comment(data)

@router.get("/comments")
async def getComments():
    return await get_all_comments()

@router.get("/comments/recent/{id}")
async def getRecentComments(id:str):
    return await get_recent_comments(id)