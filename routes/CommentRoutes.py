from fastapi import APIRouter
from models.CommentModel import Comment 
from controllers.CommentController import add_comment,get_all_comments,get_recent_comments,get_user_comments,get_comment_by_news,get_comment_by_news_only

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

@router.get("/comments/user/{id}")
async def getUserComments(id:str):
    return await get_user_comments(id)

@router.get("/comments/news/{id}")
async def getCommentbyNews(id:str):
    return await get_comment_by_news(id)

@router.get("/comments/newsonly/{id}")
async def getCommentbyNewsOnly(id:str):
    return await get_comment_by_news_only(id)

