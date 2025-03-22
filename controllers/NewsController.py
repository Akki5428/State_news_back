from models.NewsModel import News,NewsOut,ApproveNews
from bson import ObjectId
from config.database import city_collection,state_collection,news_collection,user_collection,role_collection
from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse


async def addNews(news:News):
    news = news.dict()
    news["cityId"] = ObjectId(news["cityId"])
    news["stateId"] = ObjectId(news["stateId"]) 
    news["userId"] = ObjectId(news["userId"])
    pub_news = await news_collection.insert_one(news)
    print(pub_news)
    return JSONResponse(content={"message":"News Added"},status_code=201)

async def getNews():
    news = await news_collection.find().to_list()
    for n in news:
        if "cityId" in n and isinstance(n["cityId"], ObjectId):
            n["cityId"] = str(n["cityId"])
        
        if "stateId" in n and isinstance(n["stateId"], ObjectId):  
            n["stateId"] = str(n["stateId"])

        if "userId" in n and isinstance(n["userId"], ObjectId):
            n["userId"] = str(n["userId"])
 
        city = await city_collection.find_one({"_id":ObjectId(n["cityId"])})

        if city:
            city["_id"] = str(city["_id"])
            n["city"] = city
        
        state = await state_collection.find_one({"_id":ObjectId(n["stateId"])})
        if state:
            state["_id"] = str(state["_id"])
            n["state"] = state

        user = await user_collection.find_one({"_id":ObjectId(n["userId"])})
        if user:
            user["_id"] = str(user["_id"])
            n["user"] = user

    return [NewsOut(**n) for n in news]

async def getNewsById(news_id:str):
    news = await news_collection.find_one({"_id":ObjectId(news_id)})
 
    if "cityId" in news and isinstance(news["cityId"], ObjectId):
        news["cityId"] = str(news["cityId"])
        
    if "stateId" in news and isinstance(news["stateId"], ObjectId):  
        news["stateId"] = str(news["stateId"])

    if "userId" in news and isinstance(news["userId"], ObjectId):
        news["userId"] = str(news["userId"])
        
    city = await city_collection.find_one({"_id":ObjectId(news["cityId"])})
    if city:
        city["_id"] = str(city["_id"])
        news["city"] = city
        
    state = await state_collection.find_one({"_id":ObjectId(news["stateId"])})
    if state:
        state["_id"] = str(state["_id"])
        news["state"] = state

    user = await user_collection.find_one({"_id":ObjectId(news["userId"])})
    if user:
        role = await role_collection.find_one({"_id":ObjectId(user["role_id"])})
        if role:
            role["_id"] = str(role["_id"])
            user["role"] = role
        user["_id"] = str(user["_id"])
        news["user"] = user


    return NewsOut(**news)

async def getNewsByStateId(state_id:str):
    news = await news_collection.find_one({"stateId":ObjectId(state_id)})
 
    if "cityId" in news and isinstance(news["cityId"], ObjectId):
        news["cityId"] = str(news["cityId"])
        
    if "stateId" in news and isinstance(news["stateId"], ObjectId):  
        news["stateId"] = str(news["stateId"])

    if "userId" in news and isinstance(news["userId"], ObjectId):
        news["userId"] = str(news["userId"])
        
    city = await city_collection.find_one({"_id":ObjectId(news["cityId"])})
  
    if city:
        city["_id"] = str(city["_id"])
        news["city"] = city
        print(city)
        
    state = await state_collection.find_one({"_id":ObjectId(news["stateId"])})
    if state:
        state["_id"] = str(state["_id"])
        news["state"] = state

    user = await user_collection.find_one({"_id":ObjectId(news["userId"])})
    if user:
        role = await role_collection.find_one({"_id":ObjectId(user["role_id"])})
        if role:
            role["_id"] = str(role["_id"])
            user["role"] = role
        user["_id"] = str(user["_id"])
        news["user"] = user


    return NewsOut(**news)

async def getNewsByCityId(city_id:str):
    news = await news_collection.find_one({"cityId":ObjectId(city_id)})
 
    if "cityId" in news and isinstance(news["cityId"], ObjectId):
        news["cityId"] = str(news["cityId"])
        
    if "stateId" in news and isinstance(news["stateId"], ObjectId):  
        news["stateId"] = str(news["stateId"])

    if "userId" in news and isinstance(news["userId"], ObjectId):
        news["userId"] = str(news["userId"])
        
    city = await city_collection.find_one({"_id":ObjectId(news["cityId"])})
  
    if city:
        city["_id"] = str(city["_id"])
        news["city"] = city
        print(city)
        
    state = await state_collection.find_one({"_id":ObjectId(news["stateId"])})
    if state:
        state["_id"] = str(state["_id"])
        news["state"] = state

    user = await user_collection.find_one({"_id":ObjectId(news["userId"])})
    if user:
        role = await role_collection.find_one({"_id":ObjectId(user["role_id"])})
        if role:
            role["_id"] = str(role["_id"])
            user["role"] = role
        user["_id"] = str(user["_id"])
        news["user"] = user


    return NewsOut(**news)

async def deleteNews(news_id:str):
    news = await news_collection.delete_one({"_id":ObjectId(news_id)})
    if news.deleted_count == 1:
        return JSONResponse(content={"message":"News Deleted"},status_code=200)
    else:
        return JSONResponse(content={"message":"News not found"},status_code=404)
    
def approve_news(news_id: str, approval: ApproveNews):
    if approval.status not in ["published", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    update_data = {"status": approval.status, "approvedBy": approval.adminId}
    if approval.status == "rejected":
        update_data["rejectReason"] = approval.rejectReason
    
    news_collection.update_one({"_id": ObjectId(news_id)}, {"$set": update_data})
    return {"message": f"News {approval.status} successfully"}