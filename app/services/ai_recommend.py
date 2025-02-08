import openai
import os
import json
import re
from utils.fetch_utils import get_latest_app_icon, validate_image_url

openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_app_recommendations_with_ai(user_request):
    prompt = f"""
    사용자 정보:
    - 카테고리: {', '.join(user_request.category)}
    - 성별: {user_request.gender}
    - 연령대: {user_request.age_group}
    - 앱 추구 가치: {', '.join(user_request.values)}
    - 최애 앱: {user_request.favorite_app}

    위 정보를 바탕으로 한국 앱스토어의 앱을 5개 추천해주세요. JSON 형식으로 응답하세요.
    ```json
    [
        {{"앱 이름": "앱1", "앱 URL": "앱1의 앱스토어 URL", "앱 아이콘 URL": "앱1의 아이콘 URL", "강점": "앱1의 강점"}},
        {{"앱 이름": "앱2", "앱 URL": "앱2의 앱스토어 URL", "앱 아이콘 URL": "앱2의 아이콘 URL", "강점": "앱2의 강점"}},
        {{"앱 이름": "앱3", "앱 URL": "앱3의 앱스토어 URL", "앱 아이콘 URL": "앱3의 아이콘 URL", "강점": "앱3의 강점"}},
        {{"앱 이름": "앱4", "앱 URL": "앱4의 앱스토어 URL", "앱 아이콘 URL": "앱4의 아이콘 URL", "강점": "앱4의 강점"}},
        {{"앱 이름": "앱5", "앱 URL": "앱5의 앱스토어 URL", "앱 아이콘 URL": "앱5의 아이콘 URL", "강점": "앱5의 강점"}}
    ]
    ```
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )

        ai_output = response['choices'][0]['message']['content'].strip()

        json_match = re.search(r"\[\s*\{.*?\}\s*\]", ai_output, re.DOTALL)
        if json_match:
            apps = json.loads(json_match.group())

            if isinstance(apps, list) and len(apps) == 5:
                for app in apps:
                    app["앱 아이콘 URL"] = validate_image_url(get_latest_app_icon(app["앱 URL"]))
                return apps

            return {"error": "AI가 5개의 앱을 제공하지 않았습니다."}
        else:
            return {"error": "AI 응답에서 JSON 형식을 찾을 수 없습니다."}
    except Exception as e:
        return {"error": f"AI 응답 처리 중 오류 발생: {e}"}
