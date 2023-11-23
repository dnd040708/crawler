#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
from function.function import *
from common.header import http_header
import pandas as pd

def crawl_zone():
    count = 1
    result = ''
    seed_url = 'https://new.land.naver.com/api/regions/list?cortarNo=1100000000'
    with requests.Session() as session:
        resp = session.get(url = seed_url, headers=http_header)
        data = resp.json()
        for item in data['regionList']:
            model_kwargs = {
                'zonecd': item['cortarNo']
                ,'latitude': item['centerLat']
                ,'longitude': item['centerLon']
                ,'zonenm': item['cortarName']
                ,'zonetype': item['cortarType']
            }
            result = append_dict(count, result, model_kwargs)
            count += 1
    result.to_csv('./zone.csv', encoding= 'utf-8-sig', index = False)

crawl_zone()

def crawl_aptlist():
    seed_url = 'https://new.land.naver.com/api/regions/complexes?cortarNo=1141012000&realEstateType=APT%3AABYG%3AJGC%3APRE&order='
    with requests.Session() as session:
        resp = session.get(url = seed_url, headers=http_header)
        data = resp.json()
        for item in data['complexList']:
            print(item)


def crawl_apt_ho_list():
    seed_url = 'https://new.land.naver.com/api/articles/complex/118929?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page=1&complexNo=118929&buildingNos=&areaNos=&type=list&order=rank'
    with requests.Session() as session:
        resp = session.get(url = seed_url, headers=http_header)
        data = resp.json()
        for item in data['articleList']:
            print(item)

def crawl_apt_ho_list():
    seed_url = 'https://new.land.naver.com/api/complexes/118929/prices/real?complexNo=118929&tradeType=A1&year=6&priceChartChange=false&areaNo=3&addedRowCount=30&type=table'
    with requests.Session() as session:
        resp = session.get(url = seed_url, headers=http_header)
        data = resp.json()
        for item in data['realPriceOnMonthList']:
            for sub_item in item['realPriceList']:
                print(sub_item)