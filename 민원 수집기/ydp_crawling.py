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
########################################################################################################################
#
# request를 사용할 경우 첫 문단을 가져오지 못해 민원 내용을 다 가져오지 못해 selenium 사용
#
########################################################################################################################

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
# 민원으로 이동

time.sleep(2)
driver.find_elements(By.LINK_TEXT, '공개 상담민원 조회')[0].click()
# 민원으로 이동

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
        # 민원 제목을 이용해 다음 링크를 찾을 경우 몇몇 링크가 들어가지 못하는 경우가 있어 민원 테이블 리스트 순서대로 들어가는 부분 추가

        time.sleep(2)
        html = driver.page_source
        sub_data = BeautifulSoup(html, 'html.parser')
        table_sw = 0
        model_kwargs['data_id'] = str(uuid.uuid4()).replace('-', '')
        for main_table in sub_data.find_all(class_='table-board bbs-table-view bbs-table-write'):
            if table_sw == 0:
                # 민원 테이블일 경우
                for sub_item in main_table.find_all('tr'):
                    if sub_item.find(colspan = "6") == None:
                        sub_item = sub_item.text.replace('\t','').strip()
                        sub_item = sub_item.split('\n')
                        for item_number in range(0, len(sub_item)):
                            if sub_item[item_number].find('작성일') != -1:
                                model_kwargs['post_date'] = sub_item[item_number+1]
                            # 작성일자
                    else:
                        model_kwargs['content'] = sub_item.text.replace('\t','').replace('\n',' ').strip()
                        # 민원 내용
            if table_sw == 1:
                # 민원 답변 테이블일 경우
                for sub_item in main_table.find_all('tr'):
                    if sub_item.find(colspan="6") == None:
                        sub_item = sub_item.text.replace('\t', '').strip()
                        sub_item = sub_item.split('\n')
                        for item_number in range(0, len(sub_item)):
                            if sub_item[item_number].find('담당부서') != -1:
                                model_kwargs['department'] = sub_item[item_number + 1]
                            # 담당 부서
            table_sw += 1
        driver.find_elements(By.LINK_TEXT, '목록')[0].click()
        # 링크 타기 전 페이지로 이동
        input_test(conn, model_kwargs=model_kwargs)
        page_count += 1
    driver.find_elements(By.CLASS_NAME, 'navi.navi-arrow.navi-arrow-single-right')[0].click()
    #다음 페이지로 이동
    time.sleep(2)
