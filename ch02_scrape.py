from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bs = BeautifulSoup(html, 'html.parser')

nameList = bs.findAll('span', {'class', 'green'})
for name in nameList:
    print(name.get_text())