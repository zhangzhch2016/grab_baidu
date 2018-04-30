# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
import time
import os


class BaiduPipeline(object):
    def __init__(self):
        filedir = '/home/wwwroot/index/web/baidu/data/' + time.strftime("%Y%m%d", time.localtime()) + '/'
        if os.path.exists(filedir) == False:
            os.mkdir(filedir)
        filename = str(int(time.time())) + '.xlsx'
        self.filepath = filedir + filename
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['页数', '序号', '类型', '标题', '时间', '网站', '属性', '链接', '搜索推荐', '相关搜索', '相关搜索链接', '相关推荐标题', '相关推荐链接'])
        with open('filename','w') as f:
            f.write(filename)
    def process_item(self, item, spider):
        line = [item['page'], item['sort'], '', item['title'], item['time'],'', '', item['url'], item['recom_search'],item['rel_tit'],
                item['rel_url'], item['rec_tit'], item['rec_url']]
        self.ws.append(line)
        print("#"*100)
        print(self.filepath)
        self.wb.save(self.filepath)
        return item
