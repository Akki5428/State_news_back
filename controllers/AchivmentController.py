from fastapi import HTTPException
from models.AchivmentModel import Achivment, AchivmentOut
from bson import ObjectId
from config.database import achivment_collection

async def addAchivment(achivment: Achivment):
    existing_achievement = await achivment_collection.find_one({
        "userId": ObjectId(achivment.userId),
        "badgeId": ObjectId(achivment.badgeId)
    })

    achivment = achivment.dict()
    achivment["userId"] = ObjectId(achivment["userId"])
    achivment["badgeId"] = ObjectId(achivment["badgeId"])

    if existing_achievement:
        raise HTTPException(status_code=400, detail="User already earned this badge")

    achivment = await achivment_collection.insert_one(achivment)
    return {"message": "Achivment added successfully"}

async def getUserAchivments(userId: str):
    achievements = await achivment_collection.find({"userId": ObjectId(userId)}).to_list()
    print(achievements)
    return [AchivmentOut(**achivement) for achivement in achievements]