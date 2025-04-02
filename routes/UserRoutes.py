from fastapi import APIRouter
from controllers.user_controller import addUser,getAllUsers,loginUser,get_recentUser,get_AllUsers_byDate
from models.user_model import User,UserOut,UserLogin

router = APIRouter()

@router.post("/user/")
async def post_user(user:User):
    return await addUser(user)

@router.get("/users/")
async def get_users():
    return await getAllUsers()

@router.post("/user/login/")
async def login_user(user:UserLogin):
    return await loginUser(user)

@router.get("/user/recent/")
async def get_RecentUser():
    return await get_recentUser()

@router.get("/user/new/")
async def get_NewUser():
    return await get_AllUsers_byDate()