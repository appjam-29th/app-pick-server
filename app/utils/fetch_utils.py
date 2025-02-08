import requests
import re

def get_latest_app_icon(app_url: str) -> str:
    """
    앱스토어 URL에서 앱 ID를 추출하여 최신 아이콘 URL을 가져옴.
    """
    try:
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
