from datetime import datetime, timedelta
from config.database import user_collection,news_collection

async def get_dashboard_stats():
    users = await user_collection.find().to_list()
    news = await news_collection.find().to_list()

    total_users = len(users)
    total_news = len(news)
    print(news[0]["status"])
    pending_news = len([n for n in news if n["status"] == "pending"])

    # Calculate new registrations in the last 2 days
    two_days_ago = datetime.utcnow() - timedelta(days=3)

    new_registrations = len([u for u in users if u["created_at"] and datetime.strptime(u["created_at"], "%Y-%m-%dT%H:%M:%SZ") >= two_days_ago])
    # print(datetime.strptime(users[0]["created_at"], "%Y-%m-%dT%H:%M:%S"),two_days_ago)
    print(datetime.strptime(users[0]["created_at"], "%Y-%m-%dT%H:%M:%SZ"),two_days_ago)

    return {
        "total_users": total_users,
        "total_news": total_news,
        "pending_news": pending_news,
        "new_registrations": new_registrations
    }
