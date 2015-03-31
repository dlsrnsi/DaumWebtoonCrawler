# -*- coding : utf-8 -*-
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import os
import re
 
HOST = "http://comic.naver.com"
headers = {'User-Agent': 'Mozilla/5.0'}
def webtoondownload(url,path) :
    page = 1
    while True:
        print(HOST)
        print(url)
        page_url = HOST + url +"&page="+str(page)
        print(page_url)
        html = urlopen(page_url)
        pagesoup = BeautifulSoup(html)
        for tag_a in pagesoup.select("table.viewList tr > td:nth-of-type(1) a"):
            tag_img = tag_a.find('img')
            if tag_img:
                print (tag_img['title'])
                print (HOST + tag_a['href'])
                print (tag_img['src'])
                dirname = path + '/'+re.sub('[\\\/\*\?\"\<\>\|\r\n\,\.\:]','',tag_img['title'])
                if not os.path.isdir(dirname) :
                    os.mkdir(dirname)
                articleurl = HOST + tag_a['href']
                request = Request(articleurl,None,headers)
                sock = urlopen(request)
                soup = BeautifulSoup(sock.read())
                imgList = soup.find_all('img',attrs={'id':re.compile('content')})
                fileNo = 1
                for img in imgList :
                    print(img['src'])
                    if not os.path.isfile(dirname+'/'+str(fileNo)+'.jpg'):
                        try :
                            imgURL = img['src']
                            imgRequest = Request(imgURL,None,{'User-Agent': 'Mozilla/5.0','referer':articleurl},unverifiable=True)
                            imgSock = urlopen(imgRequest)
                            open(dirname+'/'+str(fileNo)+'.jpg','wb').write(imgSock.read())
                            imgSock.close()
                        except ValueError as e :
                            print(e)
                    fileNo +=1
                sock.close()
        print("page search end")
        page += 1
        if  pagesoup.find_all(pagesoup.find_all('a', attrs={'class':'next'}, text='다음페이지')) :
            print("no next page")
            break
        print("start searching ", page,"page")
