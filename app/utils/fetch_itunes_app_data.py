import requests

def fetch_itunes_app_data(app_name, country="KR"):
    """
    iTunes Search API를 사용하여 앱 이름으로 검색 후 가장 관련 있는 앱 정보를 반환.
    """
    url = f"https://itunes.apple.com/search"
    params = {
        "term": app_name,
        "country": country,
        "media": "software",
        "limit": 1  # 가장 연관된 앱 1개만 가져옴
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            app_info = data["results"][0]
            return {
                "앱 이름": app_info.get("trackName"),
                "앱 URL": app_info.get("trackViewUrl"),
                "앱 아이콘 URL": app_info.get("artworkUrl512"),
                "앱 ID": app_info.get("trackId")
            }
    return None  # 검색 결과가 없을 경우
