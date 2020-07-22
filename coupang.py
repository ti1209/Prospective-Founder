import os
import time
import hmac, hashlib
from urllib.parse import urlencode
import urllib.request
import ssl
import pandas as pd
import json
import xlsxwriter
import requests
import urllib3
from bs4 import BeautifulSoup
from lxml import html
import json
import re

urllib3.disable_warnings()

# Coupang HMAC Error https://mingtrace.tistory.com/508

os.environ['TZ'] = 'GMT+0'
one = time.strftime('%y%m%d', time.gmtime())
two = time.strftime('%H%M%S', time.gmtime())

datetime = one + 'T' + two + 'Z'
method = "GET"
path = "/v2/providers/seller_api/apis/api/v1/marketplace/seller-products"
query = urllib.parse.urlencode({"createdAtFrom": "2020-06-19", "createdAtTo": "2020-06-19", "status": "UC"})

accesskey = "accesskey"
secretkey = "secretkey"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

coupang = []

nextToken = 1

# 목록에서 상품번호 받아오기 (100개)
# for page in range(1): 100개 이상의 상품을 하고 싶은 경우 이 for문 이용
query = urllib.parse.urlencode({"vendorId": "A00269123", "nextToken": nextToken, "maxPerPage": 100, "status": "APPROVED"})

message = datetime + method + path + query

signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + ", signed-date=" + datetime + ", signature=" + signature

url = "https://api-gateway.coupang.com" + path + "?%s" % query

req = urllib.request.Request(url)

req.add_header("Content-type", "application/json;charset=UTF-8")
req.add_header("Authorization", authorization)

req.get_method = lambda: method

try:
    resp = urllib.request.urlopen(req, context = ctx)
except urllib.request.HTTPError as e:
    if e.code == 404:
        print("404")
    else:
        print(e.errno)
except urllib.request.URLError as e:
    print(e.errno)
else:
    body = json.loads(resp.read().decode(resp.headers.get_content_charset()))
    
    try:
        for i in range(100):
            print(i, body['data'][i]['sellerProductName'])
            coupang.append(body['data'][i]['sellerProductId'])
    except IndexError:
        print("finished.")
    
    nextToken =  body['nextToken']

# 메모장에 저장
with open("list.txt", "w") as output:
    output.write(str(coupang))

# 각 상품별 상세조회
workbook = xlsxwriter.Workbook('coupang.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})

worksheet.write('A1', 'sellerProductId', bold)
worksheet.write('B1', 'sellerProductName', bold)
worksheet.write('C1', 'returnCharge', bold)
worksheet.write('D1', 'originalPrice', bold)
worksheet.write('E1', 'salePrice', bold)
worksheet.write('F1', 'supplyPrice', bold)
worksheet.write('G1', 'vendorItemId', bold)
worksheet.write('H1', 'externalVendorSku', bold)

col = 0

with open("list.txt", "r") as output:
    plist = output.read()

make_json = json.loads(plist)

for i in range(100): 
    path = "/v2/providers/seller_api/apis/api/v1/marketplace/seller-products/{0}".format(make_json[i])
    
    message = datetime + method + path + query

    signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

    authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + ", signed-date=" + datetime + ", signature=" + signature

    url = "https://api-gateway.coupang.com" + path + "?%s" % query

    req = urllib.request.Request(url)

    req.add_header("Content-type", "application/json;charset=UTF-8")
    req.add_header("Authorization", authorization)

    req.get_method = lambda: method

    try:
        resp = urllib.request.urlopen(req, context = ctx)
    except urllib.request.HTTPError as e:
        if e.code == 404:
            print("404")
        else:
            print(e)
    except urllib.request.URLError as e:
        print(e.errno)
    else:
        body = json.loads(resp.read().decode(resp.headers.get_content_charset()))

        worksheet.write(i+1, col, body['data']['sellerProductId'])
        worksheet.write(i+1, col + 1, body['data']['sellerProductName'])
        worksheet.write(i+1, col + 2, body['data']['returnCharge'])
        worksheet.write(i+1, col + 3, body['data']['items'][0]['originalPrice'])
        worksheet.write(i+1, col + 4, body['data']['items'][0]['salePrice'])
        worksheet.write(i+1, col + 5, body['data']['items'][0]['supplyPrice'])
        worksheet.write(i+1, col + 6, body['data']['items'][0]['vendorItemId'])
        worksheet.write(i+1, col + 7, body['data']['items'][0]['externalVendorSku'])

workbook.close()

read = pd.read_excel(open('coupang.xlsx', 'rb'))

for i in range(100):
    # 각 상품별 수량/가격/상태 조회
    path = "/v2/providers/seller_api/apis/api/v1/marketplace/vendor-items/{0}/inventories".format(str(read['vendorItemId'][i]))

    message = datetime + method + path + query

    signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

    authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + ", signed-date=" + datetime + ", signature=" + signature

    url = "https://api-gateway.coupang.com" + path + "?%s" % query

    req = urllib.request.Request(url)

    req.add_header("Content-type", "application/json;charset=UTF-8")
    req.add_header("Authorization", authorization)

    req.get_method = lambda: method

    try:
        resp = urllib.request.urlopen(req, context = ctx)
    except urllib.request.HTTPError as e:
        if e.code == 404:
            print("404")
        else:
            print(e.errno)
    except urllib.request.URLError as e:
        print(e.errno)
    else:
        body = json.loads(resp.read().decode(resp.headers.get_content_charset()))
        
        if not body['data']['amountInStock'] == '0' and not body['data']['onSale'] == 'False':
            # 원가확인(다팔자)
            winner = 0
            soldout = ""

            response = requests.get('https://ownerclan.com/V2/product/view.php?selfcode={0}'.format(str(read['externalVendorSku'][i])))

            soup = BeautifulSoup(response.text, 'lxml')

            main = soup.find("span", class_="price3")

            winner = int(re.sub(r'\D', '', main.text))

            try:
                soldout = soup.find("div", class_="detail_box4").find("span").text

                if soldout:
                    print(soldout)

            except AttributeError:
                print("오너클랜 홈페이지에서의 판매가격은", winner, "원 입니다.")
        else:
            print("쿠팡 상품이 품절되었습니다.")
            continue

        # 쿠팡 로그인 쿠키 얻기
        data = {
            'username' : 'VENDOR,ID',
            'password' : 'PW'
        }

        header = {
            "X-Requested-With" : "XMLHttpRequest",
            "Accept" : "application/json, text/javascript, */*; q=0.01",
            "Accept-Language" : "ko-KR",
            "Accept-Encoding" : "gzip, deflate",
            "Cache-Control" : "no-cache",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
            "Content-Length" : "44",
            "Referer" : "https://wing.coupang.com:443/login",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
        }

        cookie = ""

        with requests.Session() as s:
            response = s.post('https://wing.coupang.com/login', data=data, headers=header, verify=False)

            for key, value in response.cookies.get_dict().items():
                cookie += key + "=" + value + ";"

        # 아이템위너 확인
        product = str(read['vendorItemId'][i])

        header = {
            "Accept" : "*/*",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection" : "keep-alive",
            "Content-Length" : "31",
            "Cookie" : cookie,
            "Host" : "wing.coupang.com",
            "Origin" : "https://wing.coupang.com",
            "Referer" : "https://wing.coupang.com/seller/notification/list?searchKeyWord={0}&productOrVendorItemIds=&page=0&countPerPage=15&notificationType=OUT_OF_BUYBOX&sortBy=CREATED_AT&sortDirection=DESC".format(product),
            "Sec-Fetch-Dest" : "empty",
            "Sec-Fetch-Mode" : "cors",
            "Sec-Fetch-Site" : "same-origin", 
            "X-Requested-With" : "XMLHttpRequest",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
        }

        url = "https://wing.coupang.com/seller/notification/getBuyboxAnalysis"

        req = requests.post(url, data = {"vendorItemIds[]" : product}, headers = header, verify=False)

        soup = BeautifulSoup(req.text, 'lxml')

        minimum = 0
        sell = 0

        try:
            if soldout == "":
                minimum = int((winner * 0.846) / 0.64448)

                if int((winner * 0.846) / 0.64448) > int(json.loads(soup.find("p").text)[product]['winner']['vendorItemPrice']):
                    print("마진율이 10%이하입니다. 아이템위너 경쟁이 불가합니다.")
                else:
                    sell = 1
                    print("마진율이 10%이상입니다.", minimum, "원까지 아이템위너 경쟁이 가능합니다.")
            else:
                print("오너클랜에서 상품이 품절되었습니다.")
                
        except TypeError as n:
            print("현재 아이템위너 상품입니다.")
        

        # 가격 변경
        if sell == 1:
            path = "/v2/providers/seller_api/apis/api/v1/marketplace/vendor-items/{0}/prices/{1}".format(product,  int(round((winner * 0.846) / 0.64448, -1)))

            query = urllib.parse.urlencode({"forceSalePriceUpdate" : "true"})

            method = "PUT"

            message = datetime + method + path + query

            signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

            authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + ", signed-date=" + datetime + ", signature=" + signature

            url = "https://api-gateway.coupang.com" + path + "?%s" % query

            req = urllib.request.Request(url, data=query.encode("utf-8"), method="PUT")
            req.add_header("Content-type", "application/json;charset=UTF-8")
            req.add_header("Authorization", authorization)

            try:
                resp = urllib.request.urlopen(req, context = ctx)
            except urllib.request.HTTPError as e:
                if e.code == 404:
                    print(e)
                else:
                    print(e)
            except urllib.request.URLError as e:
                print(e)
            else:
                body = json.loads(resp.read().decode(resp.headers.get_content_charset()))
                print(product,"에 대한 ",body['message'])
