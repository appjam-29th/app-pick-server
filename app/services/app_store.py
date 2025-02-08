import json
import httpx
from pathlib import Path
from bs4 import BeautifulSoup

DATA_FILE = Path("data.json")
BASE_URL = "https://rss.applemarketingtools.com/api/v2/kr/apps"

async def fetch_app_description(app_url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(app_url)
            if response.status_code != 200:
                return "설명 없음"
            soup = BeautifulSoup(response.text, "html.parser")
            description_tag = soup.find("h2", class_="product-header__subtitle app-header__subtitle")
            return description_tag.text.strip() if description_tag else "설명 없음"
        except httpx.HTTPError:
            return "설명 없음"

async def get_apps(category: str, count: int = 10):
    """
    카테고리별 앱 리스트를 가져오는 API
    - category: 'top-free', 'top-paid', 'top-grossing' 중 하나
    - count: 가져올 앱 개수 (기본값: 10, 최대 100)
    - 앱 설명을 웹 스크래핑하여 추가
    """
    if category not in ["top-free", "top-paid", "top-grossing"]:
        raise httpx.HTTPException(status_code=400, detail="Invalid category. Use 'top-free', 'top-paid', or 'top-grossing'.")

    if count <= 0 or count > 100:
        raise httpx.HTTPException(status_code=400, detail="Count must be between 1 and 100.")

    url = f"{BASE_URL}/{category}/{count}/apps.json"

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise httpx.HTTPException(status_code=response.status_code, detail="Failed to fetch data from App Store")

    data = response.json()
    if "feed" not in data or "results" not in data["feed"]:
        raise httpx.HTTPException(status_code=404, detail="No apps found")

    apps = []
    for app in data["feed"]["results"]:
        app_url = app.get("url", "")
        genres = app.get("genres", [])  # 장르 정보 확인

        # 기본적으로 genres[0] 사용, 없으면 웹 스크래핑 시도
        app_description = genres[0] if genres else await fetch_app_description(app_url)

        apps.append({
            "app_id": app.get("id"),
            "app_name": app.get("name"),
            "app_image": app.get("artworkUrl100"),
            "app_store_url": app.get("url"),
            "app_description": app_description
        })

    return apps