from datetime import datetime, timedelta
from config.database import user_collection,news_collection
from bson import ObjectId

async def get_dashboard_stats():
    users = await user_collection.find({"role_id": { "$ne": ObjectId("67cf06f9cbd63e6e033ef9e2") }}).to_list()
    news = await news_collection.find().to_list()

    # print(users[0]["status"])
    total_users = len(users)
    total_news = len(news)
    # print(news[0]["status"])
    pending_news = len([n for n in news if n["status"] == "inProgress"])
    pending_user = len([u for u in users if u["status"] == "pending"])

    # Calculate new registrations in the last 2 days
    two_days_ago = datetime.utcnow() - timedelta(days=5)

    # new_registrations = len([u for u in users if u["created_at"] and u["created_at"] >= two_days_ago])
    # print(datetime.strptime(users[0]["created_at"], "%Y-%m-%dT%H:%M:%S"),two_days_ago)
    # print(datetime.strptime(users[0]["created_at"], "%Y-%m-%dT%H:%M:%SZ"),two_days_ago)

    return {
        "total_users": total_users,
        "total_news": total_news,
        "pending_news": pending_news,
        # "new_registrations": new_registrations
        "pending_user": pending_user,
    }

async def get_journ_dashboard_stats(id:str):
    news = await news_collection.find({"userId":ObjectId(id)}).to_list()
    n = [x["views"] for x in news if x["status"] == "published"]
    print(n)

    total_news = len(news)
    print(news[0]["status"])
    publshied_news = len([n for n in news if n["status"] == "published"])
    draft_news = len([n for n in news if n["status"] == "draft"])
    total_views = sum(n.get("views", 0) for n in news if n["status"] == "published")   

    return {
        "total_news": total_news,
        "publshied_news": publshied_news,
        "draft_news": draft_news,
        "total_views": total_views
    }
