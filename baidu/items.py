# -*- coding: utf-8 -*-

# D
#
# See documentation for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    page = scrapy.Field()
    sort = scrapy.Field()
    type = scrapy.Field()
    title= scrapy.Field()
    time = scrapy.Field()
    home = scrapy.Field()
    url= scrapy.Field()
    attribute= scrapy.Field()
    rel_url= scrapy.Field()
    rel_tit= scrapy.Field()
    rec_url= scrapy.Field()
    rec_tit= scrapy.Field()
    recom_search= scrapy.Field()
