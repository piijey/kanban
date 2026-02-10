import requests
import time

def get_city_or_station(lat, lng, language='ja'):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'format': 'json',
        'lat': lat,
        'lon': lng,
        'language': language,
        'zoom': 10,  # 市区町村レベル
        'addressdetails': 1
    }
    response = requests.get(url, params=params, headers={'User-Agent': 'my-app'})
    data = response.json()
    
    # 国別に必要な情報を抽出
    address = data.get('address', {})
    
    # 優先度順に検索（駅 > 市区町村 > 郡）
    result = {
        'country': address.get('country'),           # 国
        'country_code': address.get('country_code'), # 国コード
        'province': address.get('province'),         # 都道府県
        'city': address.get('city'),                 # 市区町村
        'station': address.get('highway'),           # 駅（highwayフィールド）
        'district': address.get('city_district') or address.get('neighbourhood'),  # 区・町名
    }
    return result

# 使用例
# print(get_city_or_station(34.6937, 135.7834))  # 日本
# print(get_city_or_station(21.0285, 105.8542))  # ベトナム

from xlsx2json import get_image_metadata

for filename in [
        "IMG_9358.JPG",  # {'lat': 34.6937, 'lng': 135.7834} {'country': '日本', 'country_code': 'jp', 'province': '奈良県', 'city': '奈良市', 'station': None, 'district': None}
        "IMG_4137.JPG",  # {'lat': 21.224, 'lng': 105.7961} {'country': 'Việt Nam', 'country_code': 'vn', 'province': None, 'city': 'Thành phố Hà Nội', 'station': None, 'district': 'Xã Nội Bài'}
        "IMG_5093.JPG",  # 香港國際機場 {'lat': 22.318, 'lng': 113.937} {'country': '中国', 'country_code': 'cn', 'province': None, 'city': '香港 Hong Kong', 'station': None, 'district': None}
        "IMG_2082.JPG",  # 上海浦东国际机场 {'lat': 31.1548, 'lng': 121.8057} {'country': '中国', 'country_code': 'cn', 'province': None, 'city': None, 'station': None, 'district': None}
    ]:

    time.sleep(0.5)
    metadata = get_image_metadata(f"docs/images/{filename}")
    print(metadata['location'])
    print(get_city_or_station(metadata['location']['lat'], metadata['location']['lng']))
    print()
