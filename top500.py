from bs4 import BeautifulSoup
import json
import requests
from datetime import datetime, timedelta
import urllib.request
from selenium import webdriver
import re

driver = webdriver.Chrome('/Users/docke/Desktop/bs/chromedriver')

driver.maximize_window()

driver.implicitly_wait(3) 

driver.get('https://datalab.naver.com/shoppingInsight/sCategory.naver?cid=50001490')

driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")

top500 = []

for i in range(25):
    for j in range(20):
        a = driver.find_element_by_css_selector('#content > div.section_instie_area.space_top > div > div:nth-child(2) > div.section_insite_sub > div > div > div.rank_top1000_scroll > ul > li:nth-child({0}) > a'.format(j + 1)).text
        top500.append(a.split("\n", 1))

    driver.find_element_by_css_selector("#content > div.section_instie_area.space_top > div > div:nth-child(2) > div.section_insite_sub > div > div > div.top1000_btn_area > div > a.btn_page_next").click()

print(top500)