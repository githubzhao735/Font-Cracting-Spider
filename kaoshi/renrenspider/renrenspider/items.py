# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RenrenspiderItem(scrapy.Item):
    #设置字段
    carbiaoshi = scrapy.Field()
    carbrand = scrapy.Field()
    cartitle = scrapy.Field()
    carprice = scrapy.Field()
    cartime = scrapy.Field()
    cardistance = scrapy.Field()
    caraddr = scrapy.Field()
    carsummary= scrapy.Field()

