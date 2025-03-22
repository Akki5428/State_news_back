from models.AreaModel import Area,AreaOut
from bson import ObjectId
from config.database import city_collection,area_collection
from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse


async def addArea(area:Area):
    savedArea = await area_collection.insert_one(area.dict())
    return JSONResponse(content={"message":"Area added"},status_code=201)


async def getArea():
    areas = await area_collection.find().to_list()
    
    for area in areas:
        if "city_id" in area and isinstance(area["city_id"], ObjectId):
            area["city_id"] = str(area["city_id"])
        
        city = await city_collection.find_one({"_id":ObjectId(area["city_id"])})    
        if city:
            city["_id"] = str(city["_id"])
            area["city"] = city
    
    return [AreaOut(**area) for area in areas]


async def getAreaByCityId(city_id: str):
    print("city id", city_id)
    areas = await area_collection.find({"city_id": city_id}).to_list()
    for area in areas:
        if "city_id" in area and isinstance(area["city_id"], ObjectId):
            area["city_id"] = str(area["city_id"])
        
        city = await city_collection.find_one({"_id": ObjectId(area["city_id"])})
        if city:
            city["_id"] = str(city["_id"])
            area["city"] = city
    
    return [AreaOut(**area) for area in areas]
    
    