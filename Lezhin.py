# -*- coding : utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = urlopen('http://www.lezhin.com/#scheduled')
soup = BeautifulSoup(url)
print(soup.prettify())