import re
from lxml import etree
from urllib import request
import time
import csv

class LianjiaSpider():
    def __init__(self):
        self.start_url = "https://{}.lianjia.com/ershoufang/"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
        }
        self.f = open("lianjia.csv", "a")
        self.writter = csv.writer(self.f)
        self.writter.writerow(["title"])

    def parse(self,url):#发送请求
        print("正在请求的页面：",url)
        re = request.Request(url=url,headers=self.headers)
        res = request.urlopen(re)
        return res.read().decode()

    def get_house_detail(self,html_str):#获取除北京外的数据
        html_etree = etree.HTML(html_str)
        house_list = html_etree.xpath("//ul[@class='sellListContent']/li")
        for house in house_list:
            item = {}
            item["title"] = house.xpath(".//div[@class='title']/a/text()")[0] if len(house.xpath(".//div[@class='title']/a/text()"))>0 else None
            yield item

    def get_bjhouse_detail(self,html_str):#获取北京的数据
        html_etree = etree.HTML(html_str)
        house_list = html_etree.xpath("//ul[@class='sellListContent']/li")
        for house in house_list:
            title_list = house.xpath(".//div[@class='title']/a/text()")
            for title in title_list:
                item ={}
                item["title"] = title
                yield item

    def save_house(self,house_list):#存储数据
        for house in house_list:
            self.writter.writerow([house["title"]])

    def run(self):#实现主要逻辑
        #构造url
        url_list =['gz','bj']
        for url in url_list:
            url1 = self.start_url.format(url)
            html_str = self.parse(url1)
            if url == 'bj':
                house_list = self.get_bjhouse_detail(html_str)
            else:
                house_list = self.get_house_detail(html_str)

            self.save_house(house_list)
        self.f.close()

if __name__ == '__main__':

    lianjia = LianjiaSpider()
    lianjia.run()






