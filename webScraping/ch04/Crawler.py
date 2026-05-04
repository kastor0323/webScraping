import requests
from bs4 import BeautifulSoup

from webScraping.ch04.Website import Website
from webScraping.ch04.Content import Content

class Crawler:

    def getPage(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            req = requests.get(url, headers=headers, timeout=10)
            if req.status_code != 200:
                print(f"접근 불가: {url} (Status Code: {req.status_code})")
                return None
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        #내용이 존재할 때
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ''

    def search(self, topic, site):
        """
        주어진 검색어로 주어진 웹사이트를 검색해 결과 페이지를 모두 기록합니다.
        """

        bs = self.getPage(site.searchUrl + topic)

        if bs is None:
            print(f"검색 페이지를 불러올 수 없습니다: {site.name}")
            return

        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs['href']
            if(site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print('Something was wrong with that page or URL. Skipping!')
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title !='' and body !='':
                content = Content(topic, url, title, body)
                content.print()

crawler = Crawler()

siteData = [
    ['Quotes to Scrape (연습용 공식 사이트)',
     'http://quotes.toscrape.com',
     'http://quotes.toscrape.com/tag/',        # 검색어(태그)를 붙일 URL
     'div.quote',                              # 1. 검색 결과 리스트 아이템
     'span > a',                               # 2. 아이템 내의 'about' (저자 상세페이지) 링크
     False,                                    # 상대 경로 사용 (예: /author/Albert-Einstein)
     'h3.author-title',                        # 3. 상세 페이지 제목 (저자 이름)
     'div.author-description']                 # 4. 상세 페이지 본문 (저자 설명)
]

sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

topics = ['humor', 'life']
for topic in topics:
    print('GETTING INFO ABOUT: ' + topic)
    for targetSite in sites:
        crawler.search(topic, targetSite)

