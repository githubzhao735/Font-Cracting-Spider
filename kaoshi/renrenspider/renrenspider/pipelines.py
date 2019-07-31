# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
class RenrenspiderPipeline(object):
    def process_item(self, item, spider):

        rds = redis.StrictRedis(host="127.0.0.1",port=6379,db=6)
        rds.lpush("zhaobuxu",str(item))

        print(item)

        return item
