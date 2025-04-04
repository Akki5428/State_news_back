from fastapi import APIRouter,HTTPException
from controllers.NewsController import addNews,getNews,getNewsById,getNewsByStateId,getNewsByCityId,deleteNews,approve_news,get_published_news,get_breaking_news,get_trending_news,get_popular_news,get_category_news,get_categoryByName_news,get_recent_news,get_news_sort_bydate,delete_news,get_approve_news,reject_news,update_news,get_recent_news_by_user
from models.NewsModel import News,ApproveNews,RejectedNews,UpdateNewsRequest
from bson import ObjectId

router = APIRouter()
@router.post("/news")
async def post_news(news:News):
    return await addNews(news)

@router.get("/news")
async def get_AllNews():
    return await getNews()

@router.get("/news/{news_id}")
async def get_NewsById(news_id:str):
    return await getNewsById(news_id)

@router.get("/news/state/{state_id}")
async def get_NewsByStateId(state_id:str):
    return await getNewsByStateId(state_id)

@router.get("/news/city/{city_id}")
async def get_NewsByCityId(city_id:str):
    return await getNewsByCityId(city_id)

@router.delete("/news/{news_id}")
async def delete_News(news_id:str):
    return await deleteNews(news_id)

@router.put("/news/{news_id}/approve")
async def approve_News(news_id:str,approve:ApproveNews):
    return await get_approve_news(news_id,approve)

@router.get("/news/published/")
async def get_PublishedNews():
    return await get_published_news()

@router.get("/news/breaking/")
async def get_BreakingNews():
    return await get_breaking_news()

@router.get("/news/trending/")
async def get_TrendingNews():
    return await get_trending_news()

@router.get("/news/popular/")
async def get_PopularNews():
    return await get_popular_news()

@router.get("/news/category/")
async def get_CategoryNews():
    return await get_category_news()

@router.get("/news/category/{category_name}")
async def get_CategoryByNameNews(category_name:str):
    return await get_categoryByName_news(category_name)

@router.get("/news/recent/")
async def get_recentNews():
    return await get_recent_news()

@router.get("/news/new/")
async def get_newsSortbyDate():
    return await get_news_sort_bydate()

@router.delete("/news/delete/{news_id}")
async def deleteNews(news_id:str):
    return await delete_news(news_id)

@router.patch("/news/approve/{news_id}")
async def approveNews(news_id:str):
    return await approve_news(news_id)

@router.patch("/news/rejected/")
async def rejectNews(news:RejectedNews):
    return await reject_news(news)

@router.put("/news/update/")
async def updateNews(news:UpdateNewsRequest):
    return await update_news(news)

@router.get("/news/recent/user/{user_id}")
async def get_RecentNewsByUser(user_id:str):
    return await get_recent_news_by_user(user_id)

