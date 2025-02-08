def get_app_recommendation_prompt(user_request):
    return f"""
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
        {{"앱 이름": "앱5", "앱 URL": "앱5의 앱스토어 URL", "앱 아이콘 URL": "앱5의 아이콘 URL", "강점": "앱5의 강점"}},
    ]
    ```
    """
