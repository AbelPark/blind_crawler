from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 웹 페이지 열기
driver.get('https://www.teamblind.com/kr/')  # 로그인 페이지 URL

# 로그인 시도
signin_button = driver.find_element(By.CLASS_NAME, 'btn_signin')
signin_button.click()
# 로그인 완료 대기 (시간 조정 가능)
time.sleep(10)

# 로그인 후 크롤링할 페이지로 이동
driver.get('https://www.teamblind.com/kr/company/%EB%8C%80%ED%95%9C%EB%AC%B4%EC%97%AD%ED%88%AC%EC%9E%90%EC%A7%84%ED%9D%A5%EA%B3%B5%EC%82%AC/reviews')  # 로그인 후 크롤링할 페이지 URL

# 데이터 크롤링
soup = BeautifulSoup(driver.page_source, 'html.parser')

review_items = soup.find_all('div', class_='review_item_inr')

for review in review_items:
    # 별점
    rating_tag = review.find('div', class_="rating")
    rating_score = rating_tag.find('strong', class_="num")
    # 제목
    title_tag = review.find('h3', class_="rvtit")
    # 장점
    adv_tag = review.find('strong', string="장점")
    adv_html = adv_tag.find_next('span')
    adv_with_breaks = ''.join(str(tag) for tag in adv_html.contents)
    adv_text = adv_with_breaks.replace('<br/>', '\n').replace('<br />', '\n').strip()
    # 단점
    dis_tag = review.find('strong', string="단점")
    dis_html = dis_tag.find_next('span')
    dis_with_breaks = ''.join(str(tag) for tag in dis_html.contents)
    dis_text = dis_with_breaks.replace('<br/>', '\n').replace('<br />', '\n').strip()
    # 이직사유
    switch_tag = review.find('strong', string="이직 사유")
    if switch_tag:
        switch_html = switch_tag.find_next('span')
        switch_with_breaks = ''.join(str(tag) for tag in switch_html.contents)
        switch_text = switch_with_breaks.replace('<br/>', '\n').replace('<br />', '\n').strip()
    else:
        switch_text = "N/A"

    print(title_tag.text, rating_score.text.replace('Rating Score', ''))
    print('장점',  adv_text)
    print('단점',  dis_text)
    # print('단점',  switch_text)

# data = soup.find_all('div', class_='review_item_inr')  # 크롤링할 데이터의 태그와 클래스 값

# for item in data:
#     print(item.text)

# # 브라우저 닫기
# driver.quit()