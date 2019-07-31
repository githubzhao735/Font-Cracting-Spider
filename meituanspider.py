import json
import requests
from lxml import etree
import re
import threading
from gevent import monkey
import gevent

monkey.patch_all()

class GetallArea(threading.Thread):  #用于提取热门城市和城市的id的对应编号

    def __init__(self):
        super().__init__()
        self.start_url = "https://hotel.meituan.com/beijing/"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
        }

    def run(self):
        res = requests.get(url=self.start_url,headers=self.headers)
        html_tree = etree.HTML(res.content.decode())
        # print(res.content.decode())
        city_id_str = re.findall(r'{"label":"人气优先","value":"solds"}\]},"city":(.*?),"seo":',res.content.decode())[0]
        city_dict = json.loads(city_id_str)

        area_list = html_tree.xpath("//div[@class='hot-content']//div/a")
        for area in area_list:
            item = {}
            item["city_name"] = area.xpath("./text()")[0]
            item["city_url"] = area.xpath("./@href")[0]
            for city_id in city_dict['data']:
                if city_id['name'] == item["city_name"]:
                    item["city_id"] = city_id['id']

            yield item


class GetareaHotle(threading.Thread):  #提取数据详情
    def __init__(self,area):
        super().__init__()
        self.area = area
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
        }

    def run(self):    #构造协程提取数据
        url = self.area["city_url"]
        resp = requests.get(url=url,headers=self.headers)
        page_tree = etree.HTML(resp.text)

        try:
            total_page = page_tree.xpath("//ul[@class='paginator']/li/a/text()")[-2]
        except Exception as e:
            print(e)
            print(url)
        t_list = []
        for i in range(int(total_page)):
            url = "https://ihotel.meituan.com/hbsearch/HotelSearch?version_name=999.9&cateId=20&attr_28=129&cityId={}&offset={}&limit=20&startDay=20190621&endDay=20190621".format(self.area["city_id"],str(i*20))
            t = gevent.spawn(self.get_house_detail,url)
            t_list.append(t)

        gevent.joinall(t_list)

    def get_house_detail(self,url):  #提取数据函数
        resp = requests.get(url = url,headers=self.headers)
        hotel_dict = json.loads(resp.text)
        # print(hotel_dict)
        for hotel in hotel_dict["data"]["searchresult"]:
            item = {}
            item["hotel_name"] = hotel["name"]
            item["hotel_addr"] = hotel["addr"]
            item["hotel_score"] = hotel["scoreIntro"]
            item["hotel_price"] = hotel["lowestPrice"]
            print(item)

if __name__ == '__main__':

    t = GetallArea()
    area_list= t.run()
    areas = []
    for area in area_list:
       areas.append(area)
    t_list = []
    for area in areas:
        t1 = GetareaHotle(area)
        t1.start()
        t_list.append(t1)
    for t1 in t_list:
        t1.join()



