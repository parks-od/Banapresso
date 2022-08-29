import time

import folium as folium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import csv
import pandas as pd
import numpy as np
import googlemaps

'''

과제 https://banapresso.com/store

바나프레소 홈페이지에서 매장별 이름, 주소를 크롤링
지오코딩을 통해 주소를 위경도로 변환
해당 컬럼을 데이터 프레임에 저장
인덱스 매장이름 매장주소 위도 경도
folium 모듈을 이용하여 지도에 각 매장을 출력
'''

driver = webdriver.Chrome('/Users/baghaechan/Documents/workspace/python/Day2/chromedriver')
driver.get('https://banapresso.com/store')

# html = driver.page_source
# soup = BeautifulSoup(html, "html.parser")
#
# data_area = soup.findAll('span', {'class', 'store_name_map'})

total = []
x = []
y = []
fields = ['매장이름', '매장주소']
fields2 = ['매장주소', '위도', '경도']

# for i in range(len(data_area)):
#     titles.append(data_area[i].find('i').text)
#     address.append(data_area[i].find('span').text)


pagenum = 1

'''
xpath
//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/ul/li[2]/a
//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/ul/li[3]/a
//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/ul/li[4]/a
//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/ul/li[5]/a
//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/span/a

'''
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
data_area = soup.findAll('span', {'class', 'store_name_map'})
for i in range(len(data_area)):
    total.append([data_area[i].find('i').text, data_area[i].find('span').text])

while (True):
    time.sleep(0.5)
    try:
        for i in range(2, 6):
            driver.find_element('xpath', '//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/ul/li[' + str(
                i) + ']/a').click()
            time.sleep(0.5)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            data_area = soup.findAll('span', {'class', 'store_name_map'})

            for i in range(len(data_area)):
                total.append([data_area[i].find('i').text, data_area[i].find('span').text])
        if pagenum == 1:
            driver.find_element('xpath', '//*[@id="contents"]/article/div/section[1]/div/div[1]/div[3]/span/a').click()
            for i in range(len(data_area)):
                total.append([data_area[i].find('i').text, data_area[i].find('span').text])
            pagenum += 1
    except NoSuchElementException:
        break

banapresso = pd.DataFrame(total)
banapresso.columns = fields
extra = banapresso['매장주소']
banapresso.to_csv("./bana1.csv")

location = []

gmaps = googlemaps.Client(key='#')

# for i in range(len(total)):
for i in range(len(total)):
    try:
        result = gmaps.geocode(banapresso['매장주소'][i])[0].get('geometry')
        lat = result['location']['lat']
        lng = result['location']['lng']
        location.append([extra[i], lat, lng])
    except:
        location.append([extra[i], 0, 0])

banapresso2 = pd.DataFrame(location)
banapresso2.columns = fields2
banapresso2.to_csv("./bana2.csv")

banapresso2 = pd.read_csv('bana2.csv')

bana_tot = pd.merge(banapresso, banapresso2, on='매장주소', how='inner')

data = bana_tot
bana_map = folium.Map(location = [data['위도'].mean(), data['경도'].mean()], zoom_start=11)

for i in data.index:
  bana_name = data.loc[i, "매장이름"] + ' - ' + data.loc[i, '매장주소']
  popup = folium.Popup(bana_name, max_width=500)
  folium.Marker(location=[data.loc[i, '위도'], data.loc[i, '경도']], popup=popup).add_to(bana_map)
bana_map.save('./bana_map.html')
bana_map
