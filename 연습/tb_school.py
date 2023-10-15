import requests
import api_key 

seed_url = 'http://api.data.go.kr/openapi/tn_pubr_public_elesch_mskul_lc_api'
params = {
    'serviceKey' : api_key.api_key,
    'pageNo' : '2000',
    'numOfRows' : '100',
    'type' : 'json',
}

page = 1
with requests.Session() as session:
    while True:
        params['pageNo'] = str(page)
        resp = session.get(url = seed_url, params=params)
        data = resp.json()
        if data['response']['header']['resultMsg'] == 'NODATA_ERROR':
            break
        for item in data['response']['body']['items']:
            print(item)
        page += 1