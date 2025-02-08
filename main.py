from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
import os
import openai

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정 (환경 변수에서 가져옴)
openai.api_key = os.getenv("OPENAI_API_KEY")

# FastAPI 인스턴스 생성
app = FastAPI()

# 사용자 요청 모델 (앱 추천을 위한 카테고리, 성별, 연령대, 앱 추구 가치, 최애 앱 등 추가)
class UserRequest(BaseModel):
    category: List[str]  # 카테고리 리스트
    gender: str  # 성별
    age_group: str  # 연령대
    values: List[str]  # 앱 추구 가치
    favorite_app: str  # 최애 앱

import re

async def get_app_recommendations_with_ai(user_request: UserRequest) -> List[Dict[str, str]]:
    prompt = f"""
    사용자 정보:
    - 카테고리: {', '.join(user_request.category)}
    - 성별: {user_request.gender}
    - 연령대: {user_request.age_group}
    - 앱 추구 가치: {', '.join(user_request.values)}
    - 최애 앱: {user_request.favorite_app}

    위 정보를 바탕으로 앱스토어의 앱을 5개 추천해주세요. 각 앱은 아래 JSON 형식으로 제공해 주세요:
    ```json
    [
        {{"앱 이름": "앱1", "앱 URL": "앱1의 URL", "앱 아이콘 URL": "앱1의 아이콘 URL", "강점": "앱1의 강점"}},
        {{"앱 이름": "앱2", "앱 URL": "앱2의 URL", "앱 아이콘 URL": "앱2의 아이콘 URL", "강점": "앱2의 강점"}},
        {{"앱 이름": "앱3", "앱 URL": "앱3의 URL", "앱 아이콘 URL": "앱3의 아이콘 URL", "강점": "앱3의 강점"}},
        {{"앱 이름": "앱4", "앱 URL": "앱4의 URL", "앱 아이콘 URL": "앱4의 아이콘 URL", "강점": "앱4의 강점"}},
        {{"앱 이름": "앱5", "앱 URL": "앱5의 URL", "앱 아이콘 URL": "앱5의 아이콘 URL", "강점": "앱5의 강점"}}
    ]
    ```
    위 형식을 그대로 따라 출력해 주세요. JSON을 올바르게 생성하세요.
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
            import json
            apps = json.loads(json_match.group())  # JSON 변환
            if isinstance(apps, list) and len(apps) == 5:
                return apps
            else:
                return {"error": "AI가 5개의 앱을 제공하지 않았습니다."}
        else:
            return {"error": "AI 응답에서 JSON 형식을 찾을 수 없습니다."}

    except Exception as e:
        return {"error": f"AI 응답 처리 중 오류 발생: {e}"}


@app.get("/")
async def root():
    return {"message": "앱 추천 서비스를 환영합니다!"}

@app.post("/recommend_apps/")
async def recommend_apps(request: UserRequest):
    recommendations = await get_app_recommendations_with_ai(request)
    return recommendations
