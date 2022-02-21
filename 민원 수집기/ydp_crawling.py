import os
import time
import requests
from bs4 import BeautifulSoup
from dbconnect2 import db_con, input_test
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import uuid
import re

ignore = re.compile(
    '[\n\r\t\xa0\U0001F90D-\U0001F9FF\u202f\U00002600-\U00002C5F\U00002000-\U00002BFF]')
def ignore_text(text):
    return ignore.sub(' ', text).strip()
model_kwargs = {
    'source_name' : '영등포'
}
seed_url = 'https://eminwon.ydp.go.kr/emwp/gov/mogaha/ntis/web/emwp/cmmpotal/action/EmwpMainMgtAction.do'
options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get(seed_url)
time.sleep(2)
driver.find_elements(By.LINK_TEXT, '민원신청 및 조회')[0].click()
time.sleep(2)
driver.find_elements(By.LINK_TEXT, '공개 상담민원 조회')[0].click()
time.sleep(120)
conn = db_con()
count_d = 0
while True:
    html = driver.page_source
    data = BeautifulSoup(html, 'html.parser')
    url = ''
    page_count = 1
    for item in data.find_all(class_='td-list'):
        time.sleep(2)
        url = ignore_text(item.text)
        print(url)
        model_kwargs['title'] = url
        '#dataSetTb > table > tbody > tr:nth-child(9) > td.td-list > a'
        try:
            driver.find_elements(By.CSS_SELECTOR, '#dataSetTb > table > tbody > tr:nth-child('+str(page_count)+') > td.td-list > a')[0].click()
        except:
            driver.find_elements(By.LINK_TEXT,url)[0].click()
        time.sleep(2)
        html = driver.page_source
        sub_data = BeautifulSoup(html, 'html.parser')
        table_sw = 0
        model_kwargs['data_id'] = str(uuid.uuid4()).replace('-', '')
        for main_table in sub_data.find_all(class_='table-board bbs-table-view bbs-table-write'):
            if table_sw == 0:
                for sub_item in main_table.find_all('tr'):
                    if sub_item.find(colspan = "6") == None:
                        sub_item = sub_item.text.replace('\t','').strip()
                        sub_item = sub_item.split('\n')
                        for item_number in range(0, len(sub_item)):
                            if sub_item[item_number].find('작성일') != -1:
                                model_kwargs['post_date'] = sub_item[item_number+1]
                    else:
                        model_kwargs['content'] = sub_item.text.replace('\t','').replace('\n',' ').strip()
            if table_sw == 1:
                for sub_item in main_table.find_all('tr'):
                    if sub_item.find(colspan="6") == None:
                        sub_item = sub_item.text.replace('\t', '').strip()
                        sub_item = sub_item.split('\n')
                        for item_number in range(0, len(sub_item)):
                            if sub_item[item_number].find('담당부서') != -1:
                                model_kwargs['department'] = sub_item[item_number + 1]
            table_sw += 1
        driver.find_elements(By.LINK_TEXT, '목록')[0].click()
        input_test(conn, model_kwargs=model_kwargs)
        page_count += 1
    driver.find_elements(By.CLASS_NAME, 'navi.navi-arrow.navi-arrow-single-right')[0].click()
    time.sleep(2)

'''http_header = {
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
seed_url = 'https://eminwon.ydp.go.kr/emwp/gov/mogaha/ntis/web/emwp/cns/action/EmwpCnslWebAction.do'
params = {
    'method': 'selectCnslWebPage',
    'menu_id': 'EMWPCnslWebInqL',
    'jndinm': 'EmwpCnslWebEJB',
    'methodnm': 'selectCnslWebPage',
    'context': 'NITS'
}
params_sub = {
    'bbs_se': 301,
    'method': 'selectCnslWebShow',
    'jndinm': 'EmwpCnslWebEJB',
    'methodnm': 'selectCnslWebShow',
    'context': 'NTIS',
    'cnsl_qna_no': 202201260909246739,
    'pageIndex': '',
    'token':'',
    'duration_search_yn':'',
    'menu_id': 301,
    'pt_field': 'mw_cnsl_sj',
    'pt_keyword':'',
    'pt_dept':'',
    'pt_deal_state':'',
    'pageSize': 20
}
with requests.Session() as session:
    resp = session.post(url=seed_url, verify=False, params=params_sub)
    data = BeautifulSoup(resp.text, 'html.parser')
    print(data.find_all('colspan="6"'))'''
