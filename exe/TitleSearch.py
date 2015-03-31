# -*- coding : utf-8 -*-
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import re
import os

HOST = "http://comic.naver.com"
headers = {'User-Agent': 'Mozilla/5.0'}
result = []
while True :
    print("""
    본 프로그램을 사용함에 있어서 법적 책임은 일체 본인에게 있습니다.
    """)
    print("검색어를 입력하세요")
    word = input()
    for x in range(2005,2016) :
        url = HOST + '/webtoon/period.nhn?period=' + str(x)
        request = Request(url,None,headers)
        sock = urlopen(request)
        soup = BeautifulSoup(sock)
        if soup.find_all('a', title = re.compile(word)) :
            result.append(soup.find_all('a', title = re.compile(word)))
    if not result :
        print('찾으시는 결과가 없습니다')
        continue
    else :
        print("검색 결과입니다. 다운 받을 웹툰을 선택해 주세요")
        downNo = 1
        for x in result :
            print(downNo,". ",x[0]['title'])
            downNo += 1
        print("0. 나가기")
        downInput = input()
        if str(downInput) == '0' :
            continue
        elif downInput.isdigit() :
            import WebtoonDownloader
            print(int(downInput)-1)
            print(result[int(downInput)-1][0]['href'])
            if not os.path.isdir(result[int(downInput)-1][0]['title']) :
                os.mkdir(result[int(downInput)-1][0]['title'])
            WebtoonDownloader.webtoondownload(result[int(downInput)-1][0]['href'],result[int(downInput)-1][0]['title'])
        else :
            print("숫자를 입력해주세요")
