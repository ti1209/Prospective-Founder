from bs4 import BeautifulSoup
import json
import requests
from datetime import datetime, timedelta
from urllib.request import Request

# 기준 데이터 - 어제일자
yesterday = datetime.today() - timedelta(days=1)
setDate = yesterday.strftime("%Y-%m-%d")

first_list = [['패션의류', '50000000', 'wear'], ['패션잡화', '50000001', 'sundries'], ['화장품/미용', '50000002', 'beauty'], ['디지털/가전', '50000003', 'digital'],\
    ['가구/인테리어', '50000004', 'interior'], ['출산/육아', '50000005', 'birth'], ['식품', '50000006', 'food'], ['스포츠/레저', '50000007', 'sports'], ['생활/건강', '50000008', 'life'],\
        ['여가/생활편의', '50000009', 'culture'], ['면세점', '50000010', 'duty']]

keyword = input("1. 패션의류\n2. 패션잡화\n3. 화장품/미용\n4. 디지털/가전\n5. 가구/인테리어\n6.출산/육아\n7. 식품\n8. 스포츠/레저\n9. 생활/건강\n10. 여가/생활편의\n11. 면세점\n\nChoose Category: ")

response = requests.get('https://search.shopping.naver.com/category/category.nhn?cat_id={0}'.format(first_list[int(keyword) - 1][1]))

soup = BeautifulSoup(response.text, 'lxml')

one = soup.find("h2", class_="category_tit")
two = soup.find("div", class_="category " + first_list[int(keyword) - 1][2])
temp = two.find_all("div", class_="category_cell")

second_list = []
third_list = []
fourth_list = [] 

for i in two.find_all("a"):
    try:
        if i.strong:
            # 2분류
            second_list.append([i.strong.text, i['href'][30:]])
        else:
            if int(i['href'][34:]) > int(3000):
                # 4분류
                fourth_list.append([i.text, i['href'][30:]])
            else:
                # 3분류
                third_list.append([i.text, i['href'][30:]])
                
    except ValueError:
        continue

url = "https://openapi.naver.com/v1/datalab/shopping/categories"

best_category = []
current_list = []

best_title = "패션의류"
best_category = ['50000000']

last = 0

current_list = first_list

sort = input("1. 1분류\n2. 2분류\n3. 3분류\n4. 4분류\n5. Quit\n\nChoose sort method: ")

while sort != '5':
    if sort == '1':
        current_list = first_list

        print("========================= 1분류 =========================\n")

    elif sort == '2':
        current_list = second_list
        
        print("========================= 2분류 =========================\n")

    elif sort == '3':
        current_list = third_list
        
        print("========================= 3분류 =========================\n")

    elif sort == '4':
        current_list = fourth_list
        
        print("========================= 4분류 =========================\n")

    if int(len(current_list)) % 2 != 0:
        current_list.append(['패션의류', '50000001'])

    for i in range(0, int(len(current_list)), 2):
        slist = []
        tlist = []

        slist.append(current_list[i][1])
        tlist.append(current_list[i+1][1])

        try:
            payload = {
            "startDate": setDate,
            "endDate": setDate,
            "timeUnit": "date",
            "category": [
                {"name": best_title, "param": best_category},
                {"name": current_list[i][0], "param": slist},
                {"name": current_list[i+1][0], "param": tlist}
            ],
            "device": "",
            "gender": "",
            "ages": []
            }

            compare = requests.post(url, json=payload,
                                headers={"X-Naver-Client-Id" : "06WJKuCdH5hQMbXHSo42",
                                "X-Naver-Client-Secret" : "KRnjxh_A8o",
                                "Content-Type" : "application/json"}).json()

            for row in compare['results']:
                if row['data']:
                    if str(row['data'][0]['ratio']) == '100':
                        if row['title'] == best_title:
                            continue
                        else:
                            best_title = row['title']
                            best_category = row['category']

                            print("오늘의 ratio 100 카테고리 :", row['title'])

                    else:
                        # 값이 1이상인 것만 뽑고 싶을 때 적용
                        # if float(row['data'][0]['ratio']) > float(1.00000):
                            print(row['title'], row['data'][0]['ratio'])
                else:
                    # 데이터가 없는 경우
                    print(row['title'], "X")

        except IndexError:
            print("Error")
            break

    print("\n\n\n")

    sort = input("1. 1분류\n2. 2분류\n3. 3분류\n4. 4분류\n5. Quit\n\nChoose sort method: ")
