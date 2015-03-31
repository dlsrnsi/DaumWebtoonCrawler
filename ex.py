# -*- coding : utf-8 -*-
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import re
import os

HOST = "http://comic.naver.com"
headers = {'User-Agent': 'Mozilla/5.0'}
result = []
url = 'http://comic.naver.com/webtoon/list.nhn?titleId=626904&page=1'
request = Request(url,None,headers)
sock = urlopen(request)
soup = BeautifulSoup(sock)
result = soup.find_all('a',attrs={'class':'next'})
print(soup.prettify())
print(result)
if not soup.find_all('a',attrs={'class':'next'}) :
    print("no next page")