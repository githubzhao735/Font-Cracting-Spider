# -*- coding: utf-8 -*-
import scrapy
from renrenspider.items import RenrenspiderItem
import re

class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renrenche.com']
    start_urls = ['https://www.renrenche.com/sz/ershouche/']

    def parse(self, response):
        #拿到车的品牌url
        car_list = response.xpath("//ul[@id='filter_brand']/li")[1:-1]

        for car in car_list:
            item = RenrenspiderItem()
            item["carbiaoshi"] = "".join(re.findall(r'/sz/(.*?)/',car.xpath("./a/@data-href").extract_first()))
            item["carbrand"] = car.xpath("./a/text()").extract_first()
            #拿出每个品牌的url
            next_url ="https://www.renrenche.com" + car.xpath("./a/@data-href").extract_first()
            # print(next_url)
            yield scrapy.Request(url=next_url,callback=self.parse_car,meta = {"item":item})

    def parse_car(self,response):

        item = response.meta["item"]
        #拿到每个品牌的第一页的所有车的地址
        car_list = response.xpath("//ul[@class='row-fluid list-row js-car-list']/li[@class='span6 list-item car-item ']")
        for car in car_list:

            car_url = "https://www.renrenche.com" + car.xpath("./a/@href").extract_first()

            yield scrapy.Request(url=car_url,callback=self.parse_detail,meta={"item":item})

        # next_page =response.xpath("//ul[@class='pagination js-pagination']/li/a/@href")[-1].extract()
        # if next_page is not None:
        #     yield scrapy.Request(url="https://www.renrenche.com"+next_page,callback=self.parse_car,meta={"item":item})

    def parse_detail(self,response):

        base_dict = {
            "0":"0",
            "4":"1",
            "5":"2",
            "3":"3",
            "7":"4",
            "1":"5",
            "2":"6",
            "6":"7",
            "9":"8",
            "8":"9",
        }

        d_str = re.findall(r'\d+',response.xpath("//li[@class='span7']//p[2]/text()").extract_first())
        time = ""
        time1 = ""
        for str in d_str[0]:
            for i in str:
                time +=base_dict[i]
        for str1 in d_str[1]:
            for j in str1:
                time1 += base_dict[j]
        carttime = time+"-"+time1

        item = response.meta["item"]
        item["cartitle"] = "".join(response.xpath("//div[@class='title']/h1//text()").extract()).strip()
        item["carprice"] = "".join(response.xpath("//div[@class='list price-list']/p[@class='price detail-title-right-tagP']//text()").extract())
        item["cartime"] =carttime
        item["cardistance"] = response.xpath("//li[@class='kilometre']//strong/text()").extract_first()
        item["caraddr"] = response.xpath("//li[@class='span5 last car-licensed-city']//strong/text()").extract_first()
        item["carsummary"] = response.xpath("//li[@class='kilometre']//strong/text()").extract()[-1]

        yield item


