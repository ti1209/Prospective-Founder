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

API_KEY = '0100000000a775d7a3987de5bc6df42708fc4916898ad7a8f5db91d8a5ca614822d46a70e9'
SECRET_KEY = 'AQAAAADexJhM1o0jqgVhMRt2GMbXN9JemPeb6a5HlTqMugXwQg=='
CUSTOMER_ID = '1904416'

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

query = {'siteId': "", 'biztpId': "", 'hintKeywords': "귀걸이", 'event': "", 'month': 0, 'showDetail': 1}

encode = parse.urlencode(query)

r = requests.get('https://api.naver.com/keywordstool', params=encode, headers=get_header('GET','/keywordstool', API_KEY, SECRET_KEY, CUSTOMER_ID))

print("수요 :",r.json()['keywordList'][0]['monthlyPcQcCnt'] + r.json()['keywordList'][0]['monthlyMobileQcCnt'])

# event
# Id	Name(KOR.)	Name(ENG.)	Parent Id	Level
# 1	생활	Living	0	1
# 3	가전	Home Appliances	1	2
# 5	장마	Rainy Season	1	2
# 6	난방/방한	Heating	1	2
# 7	방충	Insect	1	2
# 8	냉방	Cooling	1	2
# 10	유아/아동	Baby & Kids	1	2
# 12	자동차	Vehicles	1	2
# 14	취업	Jobs	1	2
# 16	수공예	Handmade	1	2
# 17	낚시	Fishing	1	2
# 18	원예	Horticulture	1	2
# 20	영화/공연	Movies & Entertainment	1	2
# 22	침구	Bedding	1	2
# 23	생활용품	Household Goods	1	2
# 24	건강	Health	0	1
# 26	건강	Health	24	2
# 27	레저/스포츠	Leisure & Sports	0	1
# 29	프로야구	Baseball	27	2
# 30	등산	Climbing	27	2
# 31	스키/보드	Skiing & Snowboarding	27	2
# 32	수상스포츠	Aquatic Sports	27	2
# 33	스포츠	Sports	27	2
# 34	자전거	Bicycles	27	2
# 35	시기	Seasons	0	1
# 37	설	Korean New Year	35	2
# 38	추석	Chuseok	35	2
# 39	스승의날	Teachers' Day	35	2
# 40	어린이날	Children's Day	35	2
# 41	화이트데이	White Day	35	2
# 42	크리스마스	Christmas	35	2
# 43	발렌타인데이	Valentine's Day	35	2
# 44	어버이날	Mother's Day & Father's Day	35	2
# 45	성년의날	Coming of Age Day	35	2
# 46	할로윈	Halloween	35	2
# 47	빼빼로데이	Pepero Day	35	2
# 49	축제/행사	Festivals & Events	35	2
# 50	벚꽃	Cherry Blossom Season	35	2
# 52	봄	Spring	35	2
# 53	가을	Fall	35	2
# 54	겨울	Winter	35	2
# 55	새해/운세	New Year & Fortune	35	2
# 56	연말	Year End	35	2
# 57	여름	Summer	35	2
# 58	교육/학교	Education & School	0	1
# 60	졸업	Graduation	58	2
# 61	학원	Private Institutes	58	2
# 62	학교행사	School Events	58	2
# 63	대입/수능	Admissions & SAT Tests	58	2
# 64	교재/교구	Teaching Materials & Aids	58	2
# 65	입학/개학	Entrance & New Semester	58	2
# 66	과제	School Assignments	58	2
# 67	농업	Farming	0	1
# 69	식물	Plants	67	2
# 70	음식/요리	Food & Cooking	0	1
# 72	건강식품	Health Supplements	70	2
# 73	농산물/수산물	Agricultural & Fishery	70	2
# 74	음식점	Restaurants	70	2
# 75	음식	Food	70	2
# 76	기호식품	Refreshment	70	2
# 77	패션/미용	Fashion & Beauty	0	1
# 79	패션	Fashion	77	2
# 80	미용	Beauty	77	2
# 81	여행	Outdoors	0	1
# 83	여행	Travel	81	2
# 84	캠핑	Camping	81	2
# 85	피크닉	Picnic	81	2
# 86	반려동물	Pet	1	2
