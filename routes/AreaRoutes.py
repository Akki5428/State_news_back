from fastapi import APIRouter, HTTPException
from controllers.AreaController import addArea, getArea, getAreaByCityId
from models.AreaModel import Area, AreaOut
from bson import ObjectId

router = APIRouter()

@router.post("/area")
async def post_area(area: Area):
    return await addArea(area)

@router.get("/area")
async def get_area():
    return await getArea()

@router.get("/area/{city_id}")
async def get_area_by_city_id(city_id: str):
    return await getAreaByCityId(city_id)
