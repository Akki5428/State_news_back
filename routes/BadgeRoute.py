from fastapi import APIRouter
from models.BadgeModel import Badge,BadgeOut
from controllers.BadgeController import addBadge,getBadges,assignBadgeToUser

router = APIRouter()    

@router.post("/badge/create")
async def add_Badge(badge:Badge):
    return await addBadge(badge)

@router.get("/badges")
async def get_Badges():
    return await getBadges()

@router.post("/badge/assign/{userId}")
async def assign_Badge(userId:str):
    return await assignBadgeToUser(userId)
