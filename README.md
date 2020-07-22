# Prospective-Founder

### 1. top500.py  
-> 네이버 데이터랩 쇼핑인사이트 우측에 위치한 인기검색어 500개 가져오기  

**Output**
![](https://github.com/ti1209/Prospective-Founder/blob/master/image/top500.PNG)
       

### 2. ad_keyword.py  
-> 네이버광고 > 키워드도구에서 나오는 결과값 가져오기  
-> 참고 http://naver.github.io/searchad-apidoc/#/tags/RelKwdStat  

**Output**  
![](https://github.com/ti1209/Prospective-Founder/blob/master/image/ad_keyword.PNG)
       

### 3. crawl.py  
-> 네이버 쇼핑에서 검색 시 나오는 다양한 값들을 크롤링

**Output**  
![](https://github.com/ti1209/Prospective-Founder/blob/master/image/crawl_1.PNG)
![](https://github.com/ti1209/Prospective-Founder/blob/master/image/crawl_2.PNG)
![](https://github.com/ti1209/Prospective-Founder/blob/master/image/crawl_3.PNG)
![](https://github.com/ti1209/Prospective-Founder/blob/master/image/crawl_4.PNG)


### 4. category.py  
-> 네이버 데이터랩 쇼핑인사이트 하단에 위치한 트렌드 비교값 가져오기  
-> 참고 https://developers.naver.com/docs/datalab/shopping/#%EC%87%BC%ED%95%91%EC%9D%B8%EC%82%AC%EC%9D%B4%ED%8A%B8-%EB%B6%84%EC%95%BC%EB%B3%84-%ED%8A%B8%EB%A0%8C%EB%93%9C-%EC%A1%B0%ED%9A%8C

**Output**  
![](https://github.com/ti1209/Prospective-Founder/blob/master/image/category.PNG)


### 5. dafalza.py
-> 다팔자 서버에 직접 접근하여 원하는 상품들의 가격 등의 정보를 가져오기  
       
       
       
### 6. dafalza_v2.py  
- 오너클랜 상품 1개가 쿠팡에서 아이템위너 경쟁이 가능한지 판단하는 스크립트
- 자동화X, 메뉴선택형  



### 7. coupang.py  
- 쿠팡 상품목록에 있는 상품들의 아이템위너 여부를 파악 후, 아이템위너 경쟁이 가능하면 **10% 마진이 적용된 가격**으로 판매가를 변경하는 스크립트  
(가격, 배송비, 쿠폰, 판매자 평점 등 아이템 위너를 결정하는 여러 요소 중 **가격**만으로만 판단함)
- 자동화O 이나, 대량의 상품에 적용해보지 않아 신중한 사용이 필요
