from fastapi import APIRouter
from controllers.DashboardController import get_dashboard_stats

router = APIRouter()

@router.get("/dash/stats/")
async def fetch_dashboard_data():
    return await get_dashboard_stats()
