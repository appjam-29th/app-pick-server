from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
import os
import openai
import requests
import re
import json

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정 (환경 변수에서 가져옴)
openai.api_key = os.getenv("OPENAI_API_KEY")

# FastAPI 인스턴스 생성
app = FastAPI()

# 사용자 요청 모델 (앱 추천을 위한 정보)
class UserRequest(BaseModel):
    category: List[str]  # 카테고리 리스트
    gender: str  # 성별
    age_group: str  # 연령대
    values: List[str]  # 앱 추구 가치
    favorite_app: str  # 최애 앱


# 최신 앱 아이콘 URL 가져오기 (iTunes API 활용)
def get_latest_app_icon(app_url: str) -> str:
    """
    앱스토어 URL에서 앱 ID를 추출하여 최신 아이콘 URL을 가져옴.
    """
    try:
        # 앱스토어 URL에서 앱 ID 추출
        match = re.search(r"id(\d+)", app_url)
        if not match:
            return app_url  # 앱스토어 링크가 아니면 원래 URL 반환
        
        app_id = match.group(1)
        lookup_url = f"https://itunes.apple.com/lookup?id={app_id}"
        response = requests.get(lookup_url, timeout=5)
        data = response.json()

        if data.get("resultCount", 0) > 0:
            return data["results"][0].get("artworkUrl512", app_url)  # 최신 아이콘 URL 반환
    except Exception as e:
        print(f"iTunes API 오류: {e}")
    return app_url  # 실패 시 원래 URL 반환


# 이미지 URL 유효성 검사 (404 방지)
def validate_image_url(image_url: str) -> str:
    """
    이미지 URL이 정상적으로 응답하는지 확인.
    만약 404가 발생하면 기본 아이콘 URL을 반환.
    """
    try:
        response = requests.head(image_url, allow_redirects=True, timeout=3)
        if response.status_code == 200:
            return image_url
    except requests.RequestException:
        pass
    return "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"  # 기본 아이콘


# AI를 이용한 앱 추천
async def get_app_recommendations_with_ai(user_request: UserRequest) -> List[Dict[str, str]]:
    """
    사용자 요청 정보를 바탕으로 AI가 앱을 추천하고, 최신 아이콘 URL을 업데이트하여 반환.
    """
    prompt = f"""
    사용자 정보:
    - 카테고리: {', '.join(user_request.category)}
    - 성별: {user_request.gender}
    - 연령대: {user_request.age_group}
    - 앱 추구 가치: {', '.join(user_request.values)}
    - 최애 앱: {user_request.favorite_app}

    위 정보를 바탕으로 앱스토어의 앱을 5개 추천해주세요. JSON 형식으로 응답하세요.
    ```json
    [
        {{"앱 이름": "앱1", "앱 URL": "앱1의 URL", "앱 아이콘 URL": "앱1의 아이콘 URL", "강점": "앱1의 강점"}},
        {{"앱 이름": "앱2", "앱 URL": "앱2의 URL", "앱 아이콘 URL": "앱2의 아이콘 URL", "강점": "앱2의 강점"}},
        {{"앱 이름": "앱3", "앱 URL": "앱3의 URL", "앱 아이콘 URL": "앱3의 아이콘 URL", "강점": "앱3의 강점"}},
        {{"앱 이름": "앱4", "앱 URL": "앱4의 URL", "앱 아이콘 URL": "앱4의 아이콘 URL", "강점": "앱4의 강점"}},
        {{"앱 이름": "앱5", "앱 URL": "앱5의 URL", "앱 아이콘 URL": "앱5의 아이콘 URL", "강점": "앱5의 강점"}}
    ]
    ```
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            n=1,
            temperature=0.7,
        )

        ai_output = response['choices'][0]['message']['content'].strip()
        print(f"AI 응답: {ai_output}")

        # JSON 블록 찾기
        json_match = re.search(r"\[\s*\{.*?\}\s*\]", ai_output, re.DOTALL)
        if json_match:
            apps = json.loads(json_match.group())

            # AI가 5개의 앱을 반환했는지 검증
            if isinstance(apps, list) and len(apps) == 5:
                for app in apps:
                    app["앱 아이콘 URL"] = validate_image_url(get_latest_app_icon(app["앱 URL"]))  # 최신 아이콘으로 업데이트 후 검증
                return apps

            return {"error": "AI가 5개의 앱을 제공하지 않았습니다."}
        else:
            return {"error": "AI 응답에서 JSON 형식을 찾을 수 없습니다."}
    except Exception as e:
        return {"error": f"AI 응답 처리 중 오류 발생: {e}"}


# FastAPI 엔드포인트
@app.get("/")
async def root():
    return {"message": "앱 추천 서비스를 환영합니다!"}

@app.post("/recommend_apps/")
async def recommend_apps(request: UserRequest):
    recommendations = await get_app_recommendations_with_ai(request)
    return recommendations
