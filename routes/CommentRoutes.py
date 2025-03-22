from fastapi import APIRouter
from models.CommentModel import Comment 
from controllers.CommentController import interact_with_news    

router = APIRouter()

@router.post("/news/interact")
async def news_interaction(data: Comment):
    return await interact_with_news(data)