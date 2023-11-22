#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
from common.api_key import *
import pandas as pd

seed_url = 'http://api.data.go.kr/openapi/tn_pubr_public_elesch_mskul_lc_api'
params = {
    'serviceKey' : api_key['school'],
    'pageNo' : '20000',
    'numOfRows' : '100',
    'type' : 'json',
    'cddcCode' : '7010000' # 서울특별시교육청 코드
}

def append_dict(count, target_pandas, input_dict):
    if count == 1:
        target_pandas = pd.DataFrame([input_dict])
    else:
        target_pandas = pd.concat([target_pandas, pd.DataFrame([input_dict])])
    return target_pandas

def crawl():
    page = 1
    count = 1
    result = ''
    with requests.Session() as session:
        while True:
            params['pageNo'] = str(page)
            resp = session.get(url = seed_url, params=params)
            data = resp.json()
            if data['response']['header']['resultMsg'] == 'NODATA_ERROR':
                result.to_csv('./school.csv', encoding= 'utf-8-sig', index = False)
                break
            for item in data['response']['body']['items']:
                model_kwargs = {
                    'schoolid': item['schoolId']
                    ,'schoolnm': item['schoolNm']
                    ,'schoolse': item['schoolSe']
                    ,'fonddate': item['fondDate']
                    ,'fondtype': item['fondType']
                    ,'bnhhse': item['bnhhSe']
                    ,'opersttus': item['operSttus']
                    ,'lnmadr': item['lnmadr']
                    ,'rdnmadr': item['rdnmadr']
                    ,'cddccode': item['cddcCode']
                    ,'cddcnm': item['cddcNm']
                    ,'edcsport': item['edcSport']
                    ,'edcsportNm': item['edcSportNm']
                    ,'creatdate': item['creatDate']
                    ,'changedate': item['changeDate']
                    ,'latitude': item['latitude']
                    ,'longitude': item['longitude']
                    ,'referencedate': item['referenceDate']
                    ,'insttcode': item['insttCode']
                }
                result = append_dict(count, result, model_kwargs)
                count += 1
            page += 1

crawl()
