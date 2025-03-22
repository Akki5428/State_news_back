from fastapi import APIRouter,HTTPException
from controllers.CityController import addCity,getCity,getCityByStateId
from models.CityModel import City,CityOut
from bson import ObjectId

router = APIRouter()
@router.post("/city")
async def post_city(city:City):
    return await addCity(city)

@router.get("/city")
async def get_city():
    return await getCity()

@router.get("/city/{state_id}")
async def get_city_by_state_id(state_id:str):
    return await getCityByStateId(state_id)