
import requests
import urllib3
import json
from bs4 import BeautifulSoup
import csv

# 에러 표시 제거
urllib3.disable_warnings()

# 다팔자에 로그인, 인증토큰 얻기
url = "https://auth.ownerclan.xyz/auth"

payload = {
    "username" : "ID",
    "password" : "PW",
    "service" : "ownerclan",
    "userType" : "seller"
}

header = {
    "X-Powered-By" : "Express",
    "Access-Control-Allow-Origin" : "*",
    "Content-Type" : "application/json;charset=UTF-8",
    "Content-Length" : "352",
    "ETag" : 'W/"160-9rbi2S6YhQymjlAnNixWo9vYGZY"',
    "Via" : "1.1 google",
    "Alt-Svc" : "clear",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
}

response = requests.post(url, json=payload, headers=header, verify=False)

token = response.text

# 메모장에 인증 토큰 저장
f = open("token.txt", "w")
f.write(token)

# csv파일에서 상품코드 모으기
product = []

with open('file.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\n')

    for row in readCSV:
        product.append(row[0])

# product에 대한 정보 가져오기
product_url = "https://dafalzadumbapi.ownerclan.com/items"

product_payload = {"keys" : ['W65DE87']}

product_header = {
    "Authorization": "Bearer " + open("test.txt", "r").read(),
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) dafalza/2.5.1-beta Chrome/73.0.3683.121 Electron/5.0.1 Safari/537.36"
}

product_response = requests.post(product_url, json=product_payload, headers=product_header, verify=False)

for j in product_response.json():
    print(j['id'], j['name'], j['price'], j['shippingFee'])
