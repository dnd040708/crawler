import os
import time
import requests
from bs4 import BeautifulSoup
import re
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


'''
http_header = [
    'User-Agent',
    '123'
]
str1 = '{0[0]},{0[1]'
str1 += '}'
print(str1.format(http_header))
'''

tag_remove = re.compile('<.+?>')
def ignore_tag(tag):
    return tag_remove.sub('', str(tag)).strip()

seed_url = 'https://www.op.gg/summoners/kr/%EB%AF%B8%EC%93%B0%EB%A6%AC'
model_kwargs = {
}
with requests.Session() as session:
    resp = session.get(url=seed_url, headers=http_header)
    data = BeautifulSoup(resp.text, 'html.parser')

    for item in data.find_all(class_="css-utzuox e19epo2o2"):
        main_data = item.find(class_='info')
        model_kwargs['type'] = main_data.find(class_='type').text
        model_kwargs['result'] = main_data.find(class_='game-result').text
        model_kwargs['game_length'] = main_data.find(class_='game-length').text
        model_kwargs['kill'] = item.find(class_='k-d-a').text.split('/')[0].strip()
        model_kwargs['death'] = item.find(class_='k-d-a').text.split('/')[1].strip()
        model_kwargs['assist'] = item.find(class_='k-d-a').text.split('/')[2].strip()
        model_kwargs['mmr'] = item.find(class_='mmr').text
