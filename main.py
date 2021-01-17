import requests
import re
from bs4 import BeautifulSoup

def crawling_country_url(soup): #각각 나라의 url을 받아오는 함수

    country_url = []
    countries = soup.find("table",id="main_table_countries_today").find_all("a",class_="mt_a")
    for country in countries:
        country_url.append("https://www.worldometers.info/coronavirus/"+country["href"]) # 제대로 된 url로 변경
        
    return country_url
    
    
def crawling_world(soup): # 세계의 데이터 크롤링 하는 함수

    data = ["World"] # "World"를 처음에 리스트에 넣어준다
    numbers = soup.find_all("div", class_="maincounter-number") # 확진자 사망자 완치 데이터를 찾는다
    for number in numbers:
        data.append(number.text.replace("\t","").replace(",","").replace("\n","").replace(" ","")) # 정제하여 data에 추가
    print("World {'확진자':", data[1], ", '사망자':", data[2], ", '완치':", data[3], "}") #여기서 출력예시 처럼 출력
    
    return data # data 값 반환
        
        
def crawling(soup): # 각각 나라의 url 크롤링 하는 함수
    
    data = [] #모든 데이터 담기위한 리스트
    name = soup.find("h1").text.replace("\t","").replace(" \xa0","").replace("\n","").replace(" ","") #나라의 이름 찾기
    data.append(name) #나라 이름 추가
    numbers = soup.find_all("div", class_="maincounter-number") #확진자 사망자 완치 데이터를 찾는다
    
    for number in numbers:
        data.append(number.text.replace("\t","").replace(",","").replace("\n","").replace(" ","")) # 정제하여 data에 추가
    
    print(name, "{'확진자':", data[1], ", '사망자':", data[2], ", '완치':", data[3], "}") #출력예시처럼 원하는 대로 출력
    return data


def main() :
    custom_header = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    html = requests.get("https://www.worldometers.info/coronavirus/", headers=custom_header)
    soup = BeautifulSoup(html.text, "html.parser")
    
    result = [] # 모든 값을 저장할 리스트
    result.append(crawling_world(soup)) # 세계의 데이터 크롤링 하는 함수
    country_list = crawling_country_url(soup) # 각각 나라의 url을 받아온다.
    
    for country in country_list: #각각 나라의 url을 받아온 값을
        coun_req = requests.get(country, headers=custom_header) #각각 접속하여서
        coun_soup = BeautifulSoup(coun_req.text, "html.parser") 
        result.append(crawling(coun_soup)) #크롤링을 각각 한여 그 값을 result에 저장
    
    dic = {} # 받아온 모든 데이터를 딕셔너리로 바꾸려고 만든 딕셔너리
    
    for i in result: # result는 2차원으로 각각 나라에 대한 이름 및 데이터가 리스트로 해서 들어가있다.
        dic[i[0]] = (i[1], i[2], i[3]) # 각각 리스트의 0번째 index에는 국가이름이 1번째에는 확진자, 2번째에는 사망자, 3번째에는 완치 결과가 들어있다. 국가이름을 dic의 key로 만들고 나머지 3개의 데이터를 튜플로 묶어 value로 넣어주었다.

if __name__ == "__main__" :
    main()
