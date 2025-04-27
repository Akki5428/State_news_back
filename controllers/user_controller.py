from models.user_model import User,UserOut,UserLogin,RejectedUser,ResetPasswordReq
from bson import ObjectId
from config.database import user_collection,role_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from util.send_email import send_mail
from datetime import datetime,timedelta
import jwt
import bcrypt


async def addUser(user:User):
    user = user.dict()
    if user["role_id"] == "67cf074ecbd63e6e033ef9e6":
        print(user["status"])
        user["status"] = "approved"
    user["role_id"] = ObjectId(user["role_id"])
    result = await user_collection.insert_one(user)

    user_email = user["email"]
    subject="🗞️ Welcome! Here’s Today’s Top Highlight"
    body=""

    if user["role_id"] == "67cf074ecbd63e6e033ef9e6":
        body = """
        <h2>📰 Welcome to State-City News Portal</h2>
        <p>Dear Reader,</p>
        <img src="https://res.cloudinary.com/dmwmbomir/image/upload/v1745178043/ijkvzblo1uwg4awrji6p.jpg" alt="News Image" style="max-width: 100%; height: auto;" />

        <p>Thank you for signing up with <strong>StateBuzz: State-City News</strong> – your go-to platform for reliable and real-time news updates from every state and city across India.</p>
        
        <p>Here’s what you can expect:</p>
        <ul>
            <li>🌍 Local & National News</li>
            <li>🗳️ Live Election Coverage</li>
            <li>📸 Exclusive Reports with Images</li>
            <li>📢 Citizen Journalism Features</li>
        </ul>

        <p>Attached is today’s top highlight. Stay informed and engaged!</p>
        <br>
        <p>Best regards,<br><em>StateBuzz: State-City News Team</em></p>
        """
    else:
        body = """
        <h2>📰 Welcome to State-City News Portal</h2>
        <p>Dear User,</p>
        <img src="https://res.cloudinary.com/dmwmbomir/image/upload/v1745178043/ijkvzblo1uwg4awrji6p.jpg" alt="News Image" style="max-width: 100%; height: auto;" />

        <p>Thank you for signing up with <strong>StateBuzz: State-City News</strong> – your go-to platform for reliable and real-time news updates from every state and city across India.</p>
        
        <p>Here’s what you can expect:</p>
        <ul>
            <li>📰 Submit News Articles</li>
            <li>🛠️ Manage & Edit Your News Posts</li>
            <li>💬 Add and Manage Comments</li>
            <li>📊 Access Your Personal Dashboard</li>
        </ul>

        <p><strong>Please note:</strong> It may take some time for your account to be approved by our admin team. Once approved, you will receive a confirmation email.</p>

        <p>We appreciate your patience and look forward to your valuable contributions!</p>

        <br />
        <p>Best regards,<br /><em>StateBuzz: State-City News Team</em></p>
        """

    send_mail(user_email, subject, body, None)
    
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

    if foundUser is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    foundUser["_id"] = str(foundUser["_id"])
    foundUser["role_id"] = str(foundUser["role_id"])
    
    
    print(request.password)
    print(foundUser["password"])

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
    users = await user_collection.find({"role_id": { "$ne": ObjectId("67cf06f9cbd63e6e033ef9e2") }}).sort("created_at",-1).to_list(length=None)

    for user in users:
        # Convert role_id from ObjectId to str before validation
        if "role_id" in user and isinstance(user["role_id"], ObjectId):
            user["role_id"] = str(user["role_id"])
        
        # Fetch role details
        role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})  
        
        if role:
            role["_id"] = str(role["_id"])  # Convert role _id to string
            user["role"] = role

        print(user)

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
    user_email = user["email"]
    subject="Welcome! Your Account is Now Live!"
    body="""
    <p>Dear Journalist,</p>

    <p>We’re thrilled to welcome you to <strong>StateBuzz</strong> as an approved contributor!</p>

    <p>Your dedication to sharing meaningful news is what drives our platform forward. As part of the journalist community, you now have access to exclusive tools and features to help you bring impactful stories to life.</p>

    <p><strong>Here's what you can do:</strong></p>
    <ul>
        <li>📝 Submit and publish your news articles</li>
        <li>🛠️ Manage and edit your submitted content anytime</li>
        <li>💬 Respond to and moderate reader comments</li>
        <li>📊 Track your article views and engagement on your personal dashboard</li>
    </ul>

    <p>If you have any questions or need support, our team is always here to help.</p>

    <p>Let’s inform, inspire, and impact — together.</p>

    <br />
    <p>Warm regards,<br /><em>The StateBuzz Team</em></p>

    """

    if user:
        print(user)
        await user_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "approved"}}
        )
        send_mail(user_email, subject, body, None)
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
    
SECRET_KEY = "Royal"

def generate_token(email: str):
    
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
 
async def forgotPassword(email: str):
    foundUser = await user_collection.find_one({"email": email})
    if not foundUser:
        raise HTTPException(status_code=404, detail="Email not found")
    
    token = generate_token(email)
    resetLink = f"http://localhost:5173/resetpassword/{token}"
    body = f"""
    <html>
        <h1>HELLO THIS IS RESET PASSWORD LINK. IT EXPIRES IN 1 HOUR</h1>
        <a href="{resetLink}">RESET PASSWORD</a>
    </html>
    """
    subject = "RESET PASSWORD"
    send_mail(email, subject, body)
    return {"message": "Reset link sent successfully"}

async def resetPassword(data: ResetPasswordReq):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms="HS256")  # Payload: {"sub": "email...", "exp": ...}
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=421, detail="Token is not valid")
        
        hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        await user_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
        
        return {"message": "Password updated successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, 
            detail="The reset password link has expired. Please request a new one."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token provided")