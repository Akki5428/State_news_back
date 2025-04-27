from fastapi import APIRouter, HTTPException
from controllers.FormController import Addads, getAds,Addquery,getquery
from models.FormModel import Advertise, AdvertiseOut
from models.ContactModel import Contact, ContactOut
from bson import ObjectId

router = APIRouter()

@router.post("/advertise")
async def post_ad(ad: Advertise):
    return await Addads(ad)

@router.get("/advertise")
async def get_ads():
    return await getAds()

@router.get("/query")
async def get_query():
    return await getquery()

@router.post("/query")
async def post_query(query:Contact):
    return await Addquery(query)
