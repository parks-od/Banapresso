import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

sosoks = ['0', '1']
item_code_list = []

# 코스피, 코스닥 두 장의 종목코드를 읽어온다.
for sosok in sosoks:
    url_tmpl = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=%s'
    url = url_tmpl % sosok

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    # 하단의 페이지를 표시하는 부분 중 가장 마지막 페이지의 정보는
    # 'pgRR' 이라는 class 명을 가진 td 태그 안에 있다.
    item_info = soup.find_all('td', {'class': 'pgRR'})

    # href 파라미터가 가지고 있는 주소에서 숫자로 되어 있는 값을
    # 찾아서 저장하면 sosok 값이 [0]에, 페이지 값은 [1]에 들어간다.
    # '[\d]'+ 는 정규식 표현이며, 숫자 값을 계속해서 찾으라는 의미이다.
    for item in item_info:
        href_addr = item.a.get('href')
        page_info = re.findall('[\d]+', href_addr)
        page = page_info[1]
        page = int(page) + 1

    # 페이지만큼 반복해서 종목코드를 읽어온다.
    for i in range(1, page, 1):
        sub_url = '{}&page={}'.format(url, i)

        page_text = requests.get(sub_url).text
        page_soup = BeautifulSoup(page_text, 'lxml')

        items = page_soup.find_all('a', {'class': 'tltle'})
        for item in items:
            item_data = re.search('[\d]+', str(item))
            if item_data:
                item_code = item_data.group()
                item_name = item.text
                result = item_code, item_name
                item_code_list.append(result)

df = pd.DataFrame(item_code_list)
df.columns = ['item_code', 'item_name']

print(df)
df2 = pd.DataFrame(item_code_list)
df3 = None

for i in range(1):
    try:
        URL = "https://finance.naver.com/item/main.naver?code="+df['item_code'][i]
        company = requests.get(URL)
        html = company.text
        df3 = pd.read_html(company.text)[3]
        df3 = pd.DataFrame(df3).xs('최근 연간 실적', axis=1)
        df3.columns = df3.columns.droplevel(1)
        df3 = df3.transpose()
        df3.columns = ['매출액(억원)', '영업이익(억원)', '당기순이익(억원)', '영업이익률(%)', '순이익률(%)', 'ROE(%)', '부채비율(%)', '당좌비율(%)', '유보율(%)',
                       'EPS(원)', 'PER(배)', 'BPS(원)', 'PBR(배)', '주당배당금(원)', '시가배당율(%)', '배당성향(%)']
        df3['회사명'] = [df['item_name'][i], df['item_name'][i], df['item_name'][i], df['item_name'][i]]
        print(df3)
    except:
        print('재무재표가 존재하지 않는 종목')

for i in range(1, len(df['item_code'])):
# for i in range(1, 3): test
    try:
        URL = "https://finance.naver.com/item/main.naver?code="+df['item_code'][i]
        company = requests.get(URL)
        html = company.text
        df2 = pd.read_html(company.text)[3]
        df2 = pd.DataFrame(df2).xs('최근 연간 실적', axis=1)
        df2.columns = df2.columns.droplevel(1)
        df2 = df2.transpose()
        df2.columns = ['매출액(억원)', '영업이익(억원)', '당기순이익(억원)', '영업이익률(%)', '순이익률(%)', 'ROE(%)', '부채비율(%)', '당좌비율(%)', '유보율(%)',
                       'EPS(원)', 'PER(배)', 'BPS(원)', 'PBR(배)', '주당배당금(원)', '시가배당율(%)', '배당성향(%)']
        df2['회사명'] = [df['item_name'][i], df['item_name'][i], df['item_name'][i], df['item_name'][i]]
        df3 = df3.append(df2)
        print(df3)
    except:
        print('재무재표가 존재하지 않는 종목')
annual_finance = pd.DataFrame(df3)
annual_finance.to_csv('annuals_finance.csv')