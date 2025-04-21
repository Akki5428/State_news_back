from fastapi import APIRouter
from controllers.user_controller import addUser,getAllUsers,loginUser,get_recentUser,get_AllUsers_byDate,get_user_byId,approve_user,delete_user,block_user,reject_user,forgotPassword,resetPassword
from models.user_model import User,UserOut,UserLogin,RejectedUser,ResetPasswordReq

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

@router.get("/user/{user_id}")
async def get_userById(user_id:str):
    return await get_user_byId(user_id)

@router.patch("/user/approve/{user_id}")
async def approveUser(user_id:str):
    return await approve_user(user_id)

@router.patch("/user/block/{user_id}")
async def blockUser(user_id:str):
    return await block_user(user_id)

@router.delete("/user/{user_id}")
async def deleteUser(user_id:str):
    return await delete_user(user_id)

@router.put("/user/rejected/")
async def rejectUser(reject:RejectedUser):
    return await reject_user(reject)

@router.post("/user/forget/{email}")
async def forgetPassword(email:str):
    return await forgotPassword(email)

@router.post("/user/reset/")
async def reset_Password(data:ResetPasswordReq):
    return await resetPassword(data)