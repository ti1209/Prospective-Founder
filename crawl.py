import os
import sys
import json
import urllib.request
import time
import random
import requests
import hashlib
import hmac
import base64
from urllib import parse
from bs4 import BeautifulSoup

API_KEY = '자신의 API_KEY'
SECRET_KEY = '자신의 SECRET_KEY'
CUSTOMER_ID = '자신의 CUSTOMER_ID'

# HMAC 생성 - 네이버에서 기본적으로 제공함
class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

keyword = input("Keyword: ")

menu = input("1. Related Keyword\n2. Classification\n3. Title\n4. Counting\n5. Quit\nInput menu number: ")

url = parse.urlparse('https://search.shopping.naver.com/search/all.nhn?query={0}'.format(keyword))

query = parse.urlencode(parse.parse_qs(url.query), doseq=True)

response = requests.get('https://search.shopping.naver.com/search/all.nhn?' + query)

soup = BeautifulSoup(response.text, 'lxml')

while menu != '5':
    if menu == '1':
        # 연관검색어
        print("\n============================== 1. Related Keyword ==============================\n")

        related = soup.find("div", class_="co_relation_srh")

        if related:
            related_kw = related.find_all("li")

            print(len(related_kw),"개")

            for j in range(len(related_kw)):
                print(j + 1,":",related_kw[j].a.text.strip())

        else:
            print("There is no related keyword.")

    elif menu == '2':
        # 1페이지에 검색된 상품들
        print("\n============================== 2. Classification(1 page) ==============================\n")

        # 총 개수
        total = soup.find_all("li", class_="_itemSection")
        
        # 네이버 광고가 붙은 상품
        ad = soup.find_all("li", class_="ad _itemSection")

        # 가격사이트 비교 상품
        compare_group = soup.find_all("li", class_="_model_list _itemSection")

        # 스토어팜에 등록된 상품
        storefarm = soup.find_all("li", class_="exception _itemSection")

        print("total:", len(total), "개\nad:", len(ad), "개\ncompare group:", len(compare_group), "개\nstorefarm:", len(storefarm), "개\nstandard: ", len(total) - len(ad) - len(compare_group) - len(storefarm), "개\n")

    elif menu == '3':
        # 각 상품  크롤링 - 상품 키워드 선정 시 참고용
        print("============================== 3. Collect Title(",len(total),"개) ==============================\n")
        print("브랜드/제조사 | 시리즈 | 모델명 | 상품종류 | 색상 | 소재 | 패키지/내용물/수량 | 사이즈 | 성별/나이 | 속성(스펙, 용량, 무게, 연식, 호수)\n")

        for i in range(len(total)):
            count = soup.find_all("li", class_="_itemSection")[i]
            goin = count.find("div", class_="tit")
            title = goin.find("a", class_="link")

            print(i + 1,":", title.text)

    elif menu == '4':
        # 실질적인 공급량 구하기
        print("\n============================== 4. Counting Overall Product ==============================")

        total_product = soup.find("a", class_="_productSet_total").find("em", text="전체").next_sibling

        total_num = int(total_product.replace(',', ''))

        overseas_product = soup.find("a", class_="_productSet_overseas").find("em", text="해외직구").next_sibling

        overseas_num = int(overseas_product.replace(',', ''))

        query = {'siteId': "", 'biztpId': "", 'hintKeywords': keyword, 'event': "", 'month': 0, 'showDetail': 1}

        encode = parse.urlencode(query)

        r = requests.get('https://api.naver.com/keywordstool', params=encode, headers=get_header('GET','/keywordstool', API_KEY, SECRET_KEY, CUSTOMER_ID))

        demand = r.json()['keywordList'][0]['monthlyPcQcCnt'] + r.json()['keywordList'][0]['monthlyMobileQcCnt']
        print("Total search number:", demand,"개")

        supply = total_num - overseas_num
        print("Total product number:", supply,"개")

        # 경쟁강도 구하기 - 값이 낮을수록 좋음
        print("Competitiveness :", supply/demand)
       
    menu = input("\n\n\n1. Related Keyword\n2. Classification\n3. Title\n4. Counting\n5. Quit\nInput menu number: ")
