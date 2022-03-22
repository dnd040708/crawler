import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from Screenshot import Screenshot_Clipping
from selenium.webdriver.common.by import By
from datetime import datetime
import uuid
import re
########################################################################################################################
#
# request를 사용할 경우 첫 문단을 가져오지 못해 민원 내용을 다 가져오지 못해 selenium 사용
#
########################################################################################################################

seed_url = 'https://topis.seoul.go.kr/'
options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get(seed_url)

while True:
    today = datetime.now()
    print(today.strftime('%H:%M:%S'))
    if "09:00:00" == today.strftime('%H:%M:%S'):
        break
while True:
    element = driver.find_element(By.CLASS_NAME ,'ol-viewport')
    element_png = element.screenshot_as_png
    today = datetime.now()
    with open('test'+today.strftime('%H:%M:%S')+'.png', 'wb') as file:
            file.write(element_png)
    count += 1
    time.sleep(300)
driver.close()

