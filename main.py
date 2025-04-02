from fastapi import FastAPI
from routes.role_route import router as role_route
from routes.UserRoutes import router as user_route
from routes.StateRoutes import router as state_route
from routes.CityRoutes import router as city_route 
from routes.AreaRoutes import router as area_route 
from routes.NewsRotues import router as news_route 
from routes.CommentRoutes import router as comment_route
from routes.BadgeRoute import router as badge_route
from routes.AchivmentRoutes import router as achivment_route
from routes.DashboardRoutes import router as dash_route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(role_route)
app.include_router(user_route)
app.include_router(state_route)
app.include_router(city_route)
app.include_router(area_route)
app.include_router(news_route)
app.include_router(comment_route)
app.include_router(badge_route)
app.include_router(achivment_route)
app.include_router(dash_route)