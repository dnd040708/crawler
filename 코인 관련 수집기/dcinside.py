import os
import time
import requests
from bs4 import BeautifulSoup
from dbconnect2 import db_con, insert_dcinsde
import uuid
import re

model_kwargs = {
    'source_name' : 'DC inside',
    'biz_kind' : 'post'
}
http_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'gall.dcinside.com',
    'Referer': 'http://gall.dcinside.com/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}
page = 1
params = {
    'id' : 'bitcoins_new1',
    'page': page
}

seed_url = 'https://gall.dcinside.com/board/lists'
conn = db_con()
with requests.Session() as session:
    while True:
        resp = session.get(url=seed_url, headers=http_header, params=params)
        if resp.status_code == 200:
            data = BeautifulSoup(resp.text, 'html.parser')
            for item in data.find_all(class_="ub-content us-post"):
                model_kwargs['data_id'] =  str(uuid.uuid4()).replace('-', '')
                try:
                    model_kwargs['title'] = item.find(class_="gall_tit ub-word").text.replace('\n','')
                    url = 'https://gall.dcinside.com' + item.find(class_="gall_tit ub-word").find('a').attrs['href']
                    model_kwargs['url'] = url[:url.find('&page')]
                    model_kwargs['view_count'] = item.find(class_="gall_count").text
                    model_kwargs['post_date'] = item.find(class_="gall_date").attrs['title']
                    model_kwargs['like_count'] = item.find(class_="gall_recommend").text
                    model_kwargs['content'] = None
                    model_kwargs['comment_count'] = None
                    model_kwargs['dislike_count'] = None
                    print(model_kwargs)
                except:
                    None
        page += 1
        params = {
            'id': 'bitcoins_new1',
            'page': page
        }
        time.sleep(1)