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
metadata = get_image_metadata("IMG_9358.jpg")
print(metadata['location'])
print(get_city_or_station(metadata['location']['lat'], metadata['location']['lng']))

metadata = get_image_metadata("IMG_4137.jpg")
print(metadata['location'])
time.sleep(1)
print(get_city_or_station(metadata['location']['lat'], metadata['location']['lng']))
