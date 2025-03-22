from fastapi import APIRouter
from controllers.AchivmentController import addAchivment, getUserAchivments
from models.AchivmentModel import Achivment

router = APIRouter()

@router.post("/achivments/create")
async def create_achivment(achivment: Achivment):
    return await addAchivment(achivment)

@router.get("/achivments/{userId}")
async def get_user_achivments(userId: str):
    return await getUserAchivments(userId)