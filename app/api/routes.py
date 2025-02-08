from fastapi import APIRouter, HTTPException
from models.request_models import UserRequest
from services.ai_recommend import get_app_recommendations_with_ai
from services.app_store import get_apps

router = APIRouter()

@router.post("/recommend_apps/")
async def recommend_apps(request: UserRequest):
    return await get_app_recommendations_with_ai(request)

@router.get("/top_apps/")
async def apps(category: str, count: int = 10):
    return await get_apps(category, count)
