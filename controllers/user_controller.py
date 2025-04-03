from models.user_model import User,UserOut,UserLogin,RejectedUser
from bson import ObjectId
from config.database import user_collection,role_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt


async def addUser(user:User):
    result = await user_collection.insert_one(user.dict())
    
    return {"Message":"user created successfully"}
    

# async def getAllUsers():
#     users = await user_collection.find().to_list()
#     print("users",users)
#     return [UserOut(**user) for user in users]

async def getAllUsers():
    users = await user_collection.find().to_list(length=None)

    for user in users:
        # Convert role_id from ObjectId to str before validation
        if "role_id" in user and isinstance(user["role_id"], ObjectId):
            user["role_id"] = str(user["role_id"])
        
        # Fetch role details
        role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})  
        
        if role:
            role["_id"] = str(role["_id"])  # Convert role _id to string
            user["role"] = role

    return [UserOut(**user) for user in users]


async def loginUser(request:UserLogin):    
    foundUser = await user_collection.find_one({"email":request.email})

    foundUser["_id"] = str(foundUser["_id"])
    foundUser["role_id"] = str(foundUser["role_id"])
    
    if foundUser is None:
        raise HTTPException(status_code=404,detail="User not found")

    if "password" in foundUser and bcrypt.checkpw(request.password.encode(),foundUser["password"].encode()):
        role = await role_collection.find_one({"_id":ObjectId(foundUser["role_id"])})
        foundUser["role"] = role
        print("foud",foundUser)
        return {"message":"user login success","user":UserOut(**foundUser)}
    else:
        raise HTTPException(status_code=404,detail="Invalid password")

async def get_recentUser():
    recent_user = await user_collection.find().sort("created_at", -1).limit(5).to_list(5)
    
    for user in recent_user:
        # Convert role_id from ObjectId to str before validation
        if "role_id" in user and isinstance(user["role_id"], ObjectId):
            user["role_id"] = str(user["role_id"])
        
        # Fetch role details
        role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})  
        
        if role:
            role["_id"] = str(role["_id"])  # Convert role _id to string
            user["role"] = role
   
    return [UserOut(**user) for user in recent_user]


async def get_AllUsers_byDate():
    users = await user_collection.find().sort("created_at",-1).to_list(length=None)

    for user in users:
        # Convert role_id from ObjectId to str before validation
        if "role_id" in user and isinstance(user["role_id"], ObjectId):
            user["role_id"] = str(user["role_id"])
        
        # Fetch role details
        role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})  
        
        if role:
            role["_id"] = str(role["_id"])  # Convert role _id to string
            user["role"] = role

    return [UserOut(**user) for user in users]


async def get_user_byId(id:set):
    user = await user_collection.find_one({"_id":ObjectId(id)})

    if user is None:
        raise HTTPException(status_code=404,detail="User not found")

    if "role_id" in user and isinstance(user["role_id"], ObjectId):
            user["role_id"] = str(user["role_id"])
        
        # Fetch role details
    role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})  
        
    if role:
        role["_id"] = str(role["_id"])  # Convert role _id to string
        user["role"] = role
    
    return UserOut(**user)


async def delete_user(id:str):
    res = await user_collection.delete_one({"_id" : ObjectId(id)})

    if res:
        print(res)
    else:
        raise HTTPException(status_code=404,detail="User not Found")

async def approve_user(id:str):
    user = await user_collection.find_one({"_id" : ObjectId(id)})
    print(user)
    print(id)
    if user:
        print(user)
        await user_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "approved"}}
        )
        return JSONResponse(content={"message":"User is Approved"},status_code=201)
    else:
        raise HTTPException(status_code=404,detail="User not Found")
    
async def block_user(id:str):
    user = await user_collection.find_one({"_id" : ObjectId(id)})
    print(user)
    print(id)
    if user:
        print(user)
        if user["status"] == "approved":
            await user_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "block"}}
            )
            return JSONResponse(content={"message":"User is Blocked"},status_code=201)
        else:
            await user_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "approved"}}
            )
            return JSONResponse(content={"message":"User is UnBlocked"},status_code=201)
    else:
        raise HTTPException(status_code=404,detail="User not Found")
 

async def reject_user(reject:RejectedUser):
    user = await user_collection.find_one({"_id" : ObjectId(reject.id)})
    print(user)
    print(reject.id)
    if user:
        print(user)
        await user_collection.update_one(
        {"_id": ObjectId(reject.id)},
        {"$set": {"status": "rejected", "rejectReason": reject.rejectReason}}
        )
        return JSONResponse(content={"message":"User is Rejected"},status_code=201)
    else:
        raise HTTPException(status_code=404,detail="User not Found")

    
