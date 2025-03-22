from models.BadgeModel import Badge,BadgeOut
from fastapi import HTTPException
from config.database import badge_collection,news_collection,achivment_collection
from bson import ObjectId
from datetime import datetime

async def addBadge(badge: Badge):
    badge = await badge_collection.insert_one(badge.dict())
    return {"message": "Badge added successfully"}

async def getBadges():
    badges = await badge_collection.find().to_list()
    return [BadgeOut(**badge) for badge in badges]

async def assignBadgeToUser(user_id: str):
    
    accepted_news_count = await news_collection.count_documents({"userId": ObjectId(user_id), "status": "published"})
    
    # Find all badges user is eligible for
    eligible_badges = await badge_collection.find({"totalAcceptedNewsCount": {"$lte": accepted_news_count}}).to_list()

    assigned_badges = []
    for badge in eligible_badges:
        badge_id = ObjectId(badge["_id"])
        
        # Check if user already has the badge
        existing_badge = await achivment_collection.find_one({"userId": user_id, "badgeId": badge_id})
        if not existing_badge:
            # Assign badge to user
            await achivment_collection.insert_one({
                "userId": user_id,
                "badgeId": badge_id,
                "earned_at": datetime.utcnow()
            })
            assigned_badges.append(badge["badgeName"])

    if assigned_badges:
        return {"message": "Badges assigned", "badges": assigned_badges}
    else:
        return {"message": "No new badges assigned"}


