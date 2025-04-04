from fastapi import APIRouter
from controllers.DashboardController import get_dashboard_stats,get_journ_dashboard_stats

router = APIRouter()

@router.get("/dash/stats/")
async def fetch_dashboard_data():
    return await get_dashboard_stats()

@router.get("/dash/journ/stats/{id}")
async def fetch_journ_dashboard_data(id:str):
    return await get_journ_dashboard_stats(id)
