import requests
import urllib3
import json
from bs4 import BeautifulSoup

# 에러 표시 제거
urllib3.disable_warnings()

info = input("오너클랜 상품과 관련된 스크립트 입니다.\n\n1. 오너클랜 인증토큰 받아오기\n2. 아이템위너 가능여부 체크하기\n3. 종료\n\n메뉴를 선택하세요 : ")

while info != '3':
    if info == '1':
        # 다팔자에 로그인, 인증토큰 얻기
        url = "https://auth.ownerclan.xyz/auth"

        payload = {
            "username" : "qorgh0902",
            "password" : "dear0902!!",
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

        print("오너클랜 인증토큰을 성공적으로 받았습니다.")

    elif info == '2':
        # product에 대한 정보 가져오기
        product = input("\n판매자 상품코드를 입력하세요(예) W68562D) : ")
        price = input("\n상품의 현재 쿠팡판매가를 입력하세요 : ")
        menu = input("\n가격정보를 받아올 방법을 선택하세요.\n1. 오너클랜에서 크롤링\n2. 다팔자 서버와 통신\n\n메뉴를 선택하세요 : ")
        winner = 0
        sell = 0

        # 1. 오너클랜 홈페이지에서 크롤링
        if menu == '1':
            response = requests.get('https://ownerclan.com/V2/product/view.php?selfcode={0}'.format(product))

            soup = BeautifulSoup(response.text, 'lxml')

            main = soup.find("span", class_="price3")

            soldout = soup.find("div", class_="detail_box4").find("span").text

            winner = int(re.sub(r'\D', '', main.text))

            if soldout:
                sell = 0
                print(soldout)
            else:
                sell = 1
                print("오너클랜 홈페이지에서의 판매가격은 ", winner, "원 입니다.")
        
        else:
        # 2. 다팔자서버와 통신
            product_url = "http://dafalzadumbapi-sandbox.ownerclan.xyz/items"
            
            product_payload = {"keys" : [product], "statusOnly" : "true"}

            product_header = {
                "Authorization": "Bearer " + open("token.txt", "r").read(),
                "version": "2.6.3-beta",
                "Content-Type": "application/json;charset=UTF-8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) dafalza/2.5.1-beta Chrome/73.0.3683.121 Electron/5.0.1 Safari/537.36"
            }

            product_response = requests.post(product_url, json=product_payload, headers=product_header, verify=False)

            if product_response.json()[0]['status'] == "available":
                sell = 1
                winner = product_response.json()[0]['price']
                print("다팔자 서버에서의 판매가격은 ", winner, "원 입니다.") 
            else:
                sell = 0
                print("해당 상품은 품절되었습니다.")

        if sell == 1:
            if int((winner * 0.846) / 0.64448) > int(price):
                print("마진율이 10%이하입니다. 아이템위너 경쟁이 불가합니다.")
            else:
                print("마진율이 10%이상입니다.", int((winner * 0.846) / 0.64448), "원까지 아이템위너 경쟁이 가능합니다.")

    info = input("\n\n\n오너클랜 상품과 관련된 스크립트 입니다.\n\n1. 오너클랜 인증토큰 받아오기\n2. 아이템위너 가능여부 체크하기\n3. 종료\n\n메뉴를 선택하세요 : ")
