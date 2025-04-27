from models.FormModel import Advertise,AdvertiseOut
from models.ContactModel import Contact,ContactOut
from bson import ObjectId
from config.database import advertise_collection,contact_collection
from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from util.send_email import send_mail


async def Addads(ad:Advertise):
    ad.dict()
    ads = await advertise_collection.insert_one(ad)
    # print("Hello")
    user_email = ad["email"]
    subject="🗞️ Welcome! Here’s Today’s Top Highlight"
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
    
    send_mail(user_email, subject, body, None)
    
    
    return JSONResponse(content={"message":"Ad Message added"},status_code=201)


async def getAds():
    ads = await advertise_collection.find().to_list()
    return [AdvertiseOut(**ad) for ad in ads]

async def Addquery(query:Contact):
    query = query.dict()
    queries = await contact_collection.insert_one(query)
    # print("Hello")
    # user_email = query["email"]
    # subject="🗞️ Welcome! Here’s Today’s Top Highlight"
    # body = """
    #     <h2>📰 Welcome to State-City News Portal</h2>
    #     <p>Dear Reader,</p>
    #     <img src="https://res.cloudinary.com/dmwmbomir/image/upload/v1745178043/ijkvzblo1uwg4awrji6p.jpg" alt="News Image" style="max-width: 100%; height: auto;" />

    #     <p>Thank you for signing up with <strong>StateBuzz: State-City News</strong> – your go-to platform for reliable and real-time news updates from every state and city across India.</p>
        
    #     <p>Here’s what you can expect:</p>
    #     <ul>
    #         <li>🌍 Local & National News</li>
    #         <li>🗳️ Live Election Coverage</li>
    #         <li>📸 Exclusive Reports with Images</li>
    #         <li>📢 Citizen Journalism Features</li>
    #     </ul>

    #     <p>Attached is today’s top highlight. Stay informed and engaged!</p>
    #     <br>
    #     <p>Best regards,<br><em>StateBuzz: State-City News Team</em></p>
    #     """
    
    # send_mail(user_email, subject, body, None)
    
    
    return JSONResponse(content={"message":"Query Message added"},status_code=201)

async def getquery():
    query = await contact_collection.find().to_list()
    
    return [ContactOut(**q) for q in query]
