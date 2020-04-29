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

API_KEY = '자신의 API_KEY'
SECRET_KEY = '자신의 SECRET_KEY'
CUSTOMER_ID = '자신의 CUSTOMER_ID'

# HMAC 생성 코드 - 네이버 API 예제에서 기본적으로 제공
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

# 검색하고 싶은 단어 hintKeywords, 최대 5개 ','으로 구분하여 입력
query = {'siteId': "", 'biztpId': "", 'hintKeywords': "귀걸이", 'event': "", 'month': 0, 'showDetail': 1}

encode = parse.urlencode(query)

r = requests.get('https://api.naver.com/keywordstool', params=encode, headers=get_header('GET','/keywordstool', API_KEY, SECRET_KEY, CUSTOMER_ID))

# PC + MOBILE 검색량 합친 값
print("수요 :",r.json()['keywordList'][0]['monthlyPcQcCnt'] + r.json()['keywordList'][0]['monthlyMobileQcCnt'])
