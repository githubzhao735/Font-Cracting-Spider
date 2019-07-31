from selenium import webdriver
from lxml import etree
import csv
import time

class VipinSpider():
    def __init__(self):
        self.start_url = "https://category.vip.com/suggest.php?keyword=连衣裙&page={}"
        self.driver = webdriver.Chrome()
        self.f = open("goods.csv", "a")
        self.writter = csv.writer(self.f)
        self.writter.writerow(["title", "sell_price", "market_price", "count", "good_url"])

    def parse(self,url):#模拟浏览器发送请求
        self.driver.get(self.start_url)
        for i in range(50):
            distance = i*200
            js = "document.documentElement.scrollTop={}".format(distance)
            self.driver.execute_script(js)
            time.sleep(1)
        html_str = self.driver.page_source
        return html_str

    def get_good_list(self,html_str):#提取数据
        html_etree = etree.HTML(html_str)
        good_list = html_etree.xpath("//div[@class='goods-list-item  c-goods  J_pro_items']")
        for good in good_list:
            item = {}
            item["title"] = "".join(good.xpath(".//h4[@class='goods-info goods-title-info']/a/text()")).strip()
            item["sell_price"] = good.xpath(".//span[@class='price' or @class='title']/text()")[0]
            item["market_price"] = good.xpath(".//del[@class='goods-small-price goods-market-price ' or @class='c-price']/text()")[1] if len(good.xpath(".//del[@class='goods-small-price goods-market-price ' or @class='c-price']/text()"))==2 else good.xpath(".//span[@class='price']")[0]
            item["count"] = good.xpath(".//span[@class='goods-discount-wrap hidden839' or @class='goods-small-price vipshop-discount']/text()")[0]
            item["good_url"] = "https:" + good.xpath(".//a[@class='goods-image-link']/img/@data-original")[0]

            yield item

    def save_good(self,good_list):#存储数据
        for good in good_list:
            self.writter.writerow([good["title"],good["sell_price"],good["market_price"],good["count"],good["good_url"]])

    def run(self):#实现主要逻辑
        for num in range(1,2):
            #构造url地址
            url = self.start_url.format(num)
            #发送请求
            html_str = self.parse(url)
            #提取数据
            good_list = self.get_good_list(html_str)
            #存储数据
            self.save_good(good_list)
            time.sleep(2)

        self.f.close()
        self.driver.close()

if __name__ == '__main__':

    vipin = VipinSpider()
    vipin.run()

