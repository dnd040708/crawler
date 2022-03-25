import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import uuid
import re
########################################################################################################################
#
# 지도 정보 크롤링 프로그램
#
########################################################################################################################

seed_url = 'https://topis.seoul.go.kr/map/openTrafficMap.do'
options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get(seed_url)

while True:
    today = datetime.now()
    if "17:10:00" == today.strftime('%H:%M:%S'):
        break
# 일정 시간 이후 시작
while True:
    element = driver.find_element(By.CLASS_NAME ,'ol-viewport')
    element_png = element.screenshot_as_png
    # 사진으로 저장할 canvas class 명

    today = datetime.now()
    print(today.strftime('%H:%M:%S'))
    with open('0325'+today.strftime('%H%M%S')+'.png', 'wb') as file:
            file.write(element_png)
    time.sleep(270)
    button = driver.find_element(By.CLASS_NAME, "ol-zoom-out")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(10)
    button = driver.find_element(By.CLASS_NAME, "ol-zoom-in")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(20)
    # 5분 마다 수집
    # 줌인 줌아웃으로 지도 갱신
driver.close()

