# -*- coding : utf-8 -*-
from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urlencode
import http
import requests
import json
import re
import os
from bs4 import BeautifulSoup

Host = 'http://webtoon.daum.net'
headers = {'User-Agent': 'Mozilla/5.0','Referer' : 'http://webtoon.daum.net', 'Host':"webtoon.daum.net",}

while True :
    print("검색어를 입력해 주세요")
    word = '게임'
    resultList = []
    resultURLList = []
    for x in range(1,50) :
        try :
            url ='http://webtoon.daum.net/data/webtoon/list_by_option?page_no='+str(x)+'&page_size=30'
            request = Request(url,None,headers)
            sock = urlopen(request)
            sockSoup =  BeautifulSoup(sock)
            jsonResult = json.loads(sockSoup.prettify())
            for y in jsonResult['data']['webtoonList']:
                if re.search(word,y['title']) :
                    print(y['title'])
                    resultList.append(y['title'])
                    print(y['nickname'])
                    resultURLList.append(y['nickname'])
        except TypeError as e :
            print(e)
            break
    if not resultList :
        print('찾으시는 결과가 없습니다')
        continue
    else :
        print("검색 결과입니다. 다운 받을 웹툰을 선택해 주세요")
        downNo = 1
        for x in resultList :
            print(downNo,". ",x)
            downNo += 1
        print("0. 나가기")
        downInput = input()
        if str(downInput) == '0' :
            continue
        elif downInput.isdigit() :
            #폴더 만들기
            dirname = resultList[int(downInput)-1]
            if not os.path.isdir(dirname) :
                os.mkdir(dirname)
            webtoonURL = Host +'/webtoon/view/'+resultURLList[int(downInput)-1]
            webtoonRequest = Request(webtoonURL,None,headers)
            webtoonSock = urlopen(webtoonRequest)
            webtoonSoup = BeautifulSoup(webtoonSock)
            scriptResult = webtoonSoup.find_all('script',attrs={'type':"text/javascript"})
            result = re.findall('title:".+?",\sshortTitle:".+?",\surl:".+?",',scriptResult[12].text)
            for x in result :
                partition = x.split(',')
                path = dirname + '/'+ partition[1].split('"')[1]
                articleNo = re.search('\d+',partition[2].split('"')[1]).group()
                jsURL =Host + '/webtoon/viewer_images.js?webtoon_episode_id='+articleNo
                articleURL = Host+partition[2].split('"')[1]
                print('jsURL : ',articleURL)
                print('articleURL : ', articleURL)
                param = {'webtoon_episode_id':articleNo}
                data = urlencode(param)
                articleHTTP = http.client.HTTPConnection(Host,80)
                print(articleHTTP)
                articleSoup = BeautifulSoup(urlopen(articleURL))
                print(articleSoup.prettify())
                articleRequest = articleHTTP.request('POST','/webtoon/viewer_images.js?webtoon_episode_id='+articleNo+':80', data,
                                                     headers={'Host':Host,'User-Agent':'Mozilla/5.0','Referer':webtoonSock.read()})
                #articleRequest = Request(articleURL,None,headers)
                #articleSock = urlopen(articleRequest)


                #imgResult = json.loads(articleSoup)['images']
                #print(imgResult)
                break

        else :
            print("숫자를 입력해주세요")

    break