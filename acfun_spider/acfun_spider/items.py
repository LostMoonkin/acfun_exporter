# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticleItem(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    info = scrapy.Field()