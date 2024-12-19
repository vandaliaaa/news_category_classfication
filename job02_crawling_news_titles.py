from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from setuptools.package_index import user_agent
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
options.add_argument('user_agent='+user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = 'https://news.naver.com/section/100'
driver.get(url)#브라우저 띄우기

#버튼 생성이 될때까지 기다리는 딜레이
time.sleep(1)

#버튼 더보기 주소
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'

for i in range(15):
    time.sleep(0.5)
    driver.find_element(By.XPATH, button_xpath).click()


time.sleep(10)

#driver.close()#브라우저 닫기
