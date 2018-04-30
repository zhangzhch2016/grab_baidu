import scrapy
import re
import json
from baidu.items import BaiduItem
from urllib.parse import urlparse
from urllib import request
from bs4 import BeautifulSoup as bs


class Baidu(scrapy.Spider):
    name = 'baidu'

    def __init__(self, starurl=None, p=5, *args, **kwargs):
        super(Baidu, self).__init__(*args, **kwargs)
        self.total_page = int(p)
        self.page_num = 1
        self.garGetUrl = starurl.replace('#', '&')

    def start_requests(self):
        if re.search('ms\=1', self.garGetUrl):
            yield scrapy.Request(url=self.garGetUrl, callback=self.parse_phone)
        else:
            yield scrapy.Request(url=self.garGetUrl, callback=self.parse_pc)

    def parse_pc(self, response):
        """提取相关数据"""
        sort = 0
        item = BaiduItem()
        soup = bs(response.body, 'lxml')
        urlarr = self.get_url_query(response.url)
        search = urlarr['wd'] if urlarr['wd'] else urlarr['word']
        connects = soup.find_all(attrs={"class": "c-container"})
        if soup.find('span', 'hint_toprq_tips_items') is not None:
            rec = self.parse_rec(soup.find('span', 'hint_toprq_tips_items'))
        else:
            rec = None
        if soup.find('div', id='rs') is not None and sort == 0:
            rel = self.parse_rel(soup.find('div', id='rs'))
        else:
            rel = None
        for index, connect in enumerate(connects):
            if(self.page_num == 1) :
                url = 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=%s&cb=&json=1' % search
                recommendList = self.get_recommend(url)
                recLen = len(recommendList)
                if recLen-1 >= index:
                    item['recom_search'] = recommendList[index]
                else:
                    item['recom_search'] = ''
            else:
                item['recom_search'] = ''
            sort += 1
            if connect.find('h3', 't') is None:
                item['title'] = connect.find('a').get_text()
                item['url'] = connect.find('a')['href']
            else:
                item['title'] = connect.find('h3').get_text().strip()
                item['url'] = self.parse_url(connect.find('h3').a['href'])
            item['page'] = '第%s页' % self.page_num
            item['sort'] = sort
            if connect.find('span', ' newTimeFactor_before_abs m') is not None:
                item['time'] = connect.find('span', ' newTimeFactor_before_abs m').get_text().replace(u'\xa0-\xa0', '')
            else:
                item['time'] = ''

            if rec is not None:
                try:
                    data = next(rec)
                    item['rec_url'] = self.parse_url(response.url + data['url'])
                    item['rec_tit'] = data['title']
                except StopIteration:
                    item['rec_url'] = ''
                    item['rec_tit'] = ''
            else:
                item['rec_url'] = ''
                item['rec_tit'] = ''

            if rel is not None:
                try:
                    data = next(rel)
                    item['rel_url'] = response.url + data['url']
                    item['rel_tit'] = data['title']
                except StopIteration:
                    item['rel_url'] = ''
                    item['rel_tit'] = ''
            else:
                item['rel_url'] = ''
                item['rel_tit'] = ''
            yield item

        if self.page_num < self.total_page:
            self.page_num += 1
            next_url = response.urljoin(soup.find('div', id='page').find('strong').next_sibling['href'])
            yield scrapy.Request(next_url, callback=self.parse_pc)

    def parse_phone(self, response):
        item = BaiduItem()
        sort = 0
        soup = bs(response.body, 'lxml')
        urlarr = self.get_url_query(response.url)
        search = urlarr['wd'] if 'wd' in urlarr.keys() else urlarr['word']
        if soup.find('div', class_='rw-list') is not None:
            rel = self.parse_rel(soup.find('div', class_='rw-list'))
        else:
            rel = None

        if soup.find('div', class_='hint-toprq-tips') is not None:
            rec = self.parse_rel(soup.find('div', class_='hint-toprq-tips'))
        else:
            rec = None

        if soup.find('div', id='page-controller').find('a', class_='new-nextpage') is not None:
            next_page_url = soup.find('div', id='page-controller').find('a', class_='new-nextpage')['href']
        else:
            next_page_url = soup.find('div', id='page-controller').find('a', class_='new-nextpage-only')['href']
        if not re.search('ms\=1', next_page_url):
            next_page_url = next_page_url + '&ms=1'
        connects = soup.find('div', id='results').find_all('div', class_='c-result')
        for index,connect in enumerate(connects):
            if (self.page_num == 1):
                url = 'https://m.baidu.com/su?pre=1&p=3&json=1&wd=%s&sugmode=2&_=1493098255100' % search
                recommendList = self.get_recommend(url)
                recLen = len(recommendList)
                if recLen - 1 >= index:
                    item['recom_search'] = recommendList[index]
                else:
                    item['recom_search'] = ''
            else:
                item['recom_search'] = ''
            sort += 1
            tag_a = connect.find('div', class_='c-container').find('a')
            item['title'] = tag_a.get_text()
            if rel is not None:
                try:
                    data = next(rel)
                    item['rel_url'] = response.url + data['url']
                    item['rel_tit'] = data['title']
                except StopIteration:
                    item['rel_url'] = ''
                    item['rel_tit'] = ''
            else:
                item['rel_url'] = ''
                item['rel_tit'] = ''
            if rec is not None:
                try:
                    data = next(rec)
                    item['rec_url'] = self.parse_url(response.url + data['url'])
                    item['rec_tit'] = data['title']
                except StopIteration:
                    item['rec_url'] = ''
                    item['rec_tit'] = ''
            else:
                item['rec_url'] = ''
                item['rec_tit'] = ''
            if connect['data-log'] is not None:
                data_log = json.loads(connect['data-log'].replace("'", '"'))
                item['sort'] = data_log['order']
                if data_log['mu'] != '':
                    item['url'] = data_log['mu']
                else:
                    item['url'] = self.parse_url(tag_a['href'])
            else:
                item['url'] = self.parse_url(tag_a['href'])
            if connect.find('span', class_='c-gray') is not None:
                item['time'] = connect.find('span', class_='c-gray').get_text()
            else:
                item['time'] = ''
            item['page'] = '第%s页' % self.page_num


            # self.write_log(tag_a.get_text())
            yield item
        if next_page_url != '' and self.page_num < self.total_page:
            self.page_num += 1
            yield scrapy.Request(url=next_page_url, callback=self.parse_phone)

    def parse_rec(self, html):
        """解析推荐"""
        item = BaiduItem()
        for row in html.find_all('a'):
            item['url'] = row['href']
            item['title'] = row.get_text().strip()
            yield item

    def parse_rel(self, html):
        """解析相关搜索"""
        item = BaiduItem()
        for row in html.find_all('a'):
            item['url'] = row['href']
            item['title'] = row.get_text().strip()
            yield item

    def parse_url(self, url):
        if re.search('www\.baidu\.com\/link\?url\=', url):
            try:
                return request.urlopen(url).url
            except:
                return url
        else:
            return url

    def get_recommend(self,url):
        with request.urlopen(url) as body:
            response = body.read().decode('gbk')
            start = response.find('{')
            end = response.rfind('}') + 1
            data = response[start:end]
            data = json.loads(data)
            return data['s']

    def get_url_query(self, url):
        parent = {}
        query = urlparse(url).query
        for q in query.split('&'):
            l = q.split('=')
            parent[l[0]] = l[1]
        return parent

    def write_log(self, log):
        with open('baidu.log', 'a') as f:
            f.write(str(log))