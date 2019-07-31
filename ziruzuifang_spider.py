import requests
import re
from aip import AipOcr
from lxml import etree
import time

def connect_baidu():#链接百度的文字识别库
    """ 你的 APPID AK SK """
    APP_ID = '16524782'
    API_KEY = 't2PQkGMO0EwpzLm44uq25meu'
    SECRET_KEY = 'KrnsMF58uCVGPK38uzUtWlDHumAmL1vA'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client

class ZiruSpider():
    def __init__(self):
        self.start_url = "http://hz.ziroom.com/z/nl/z3.html"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
        }

    def parse_url(self,url):#发送请求
        print("正在爬取的网页：",url)
        resp = requests.get(url = url,headers = self.headers)
        return resp.text

    def get_img_str(self,code_img_url):#拿到价格的图片
        img_resp = requests.get(url=code_img_url, headers=self.headers)
        with open("price_img.png", "wb") as f:
            f.write(img_resp.content)
        with open("price_img.png", "rb") as f:
            img = f.read()
        client = connect_baidu() #调用百度文字识别库
        img_str = client.basicAccurate(img)
        img_str = img_str['words_result'][0]['words']
        return img_str

    def get_house_price_list(self,html_str,img_str):#取每一页的房子的价格
        price_index_list = re.findall(r'"offset":\[(.*?)\]}', html_str)[0]
        price_index_list = re.findall(r'\[(.*?)\]', price_index_list)
        house_price_list = []
        for i in price_index_list:
            str_list = re.findall(r'\d+',i)
            str_index = ''
            for j in str_list:
                str_index = str_index + img_str[int(j)]
            house_price_list.append(str_index)
        return house_price_list

    def get_house_detail(self,html_str):#拿到房子的详细信息
        code_img_url = "https:"+re.findall(r'"image":"(.*?)"',html_str)[0]
        img_str = self.get_img_str(code_img_url)
        house_price_list = self.get_house_price_list(html_str,img_str)
        house_tree = etree.HTML(html_str)
        house_list = house_tree.xpath("//ul[@id='houseList']/li[@class='clearfix']")
        for house in house_list:
            item = {}
            item['title'] = house.xpath(".//h3/a[@class='t1']/text()")[0] if len(house.xpath(".//h3/a[@class='t1']/text()")) > 0 else None
            item['house_detail'] = "".join(re.findall(r'[^\s]',"".join(house.xpath(".//div[@class='detail']//text()")).strip()))
            item['house_price'] = house_price_list[house_list.index(house)]
            print(item)

        next_url = "http:" + house_tree.xpath("//div[@id='page']/a[contains(text(),'下一页')]/@href")[0] if len(house_tree.xpath("//div[@id='page']/a[contains(text(),'下一页')]/@href"))>0 else None
        if next_url is not None:
            html_next_str = self.parse_url(next_url)
            time.sleep(5)
            self.get_house_detail(html_next_str)

    def get_area_list(self,html_str):#获取地区的地址
        area_tree = etree.HTML(html_str)
        area_list = ["http:"+area for area in area_tree.xpath("//dl[@class='changeCityList']/dd/a/@href")]
        return area_list

    def run(self):#实现主要逻辑
        #发送请求
        html_str = self.parse_url(self.start_url)
        # 提取数据
        self.get_house_detail(html_str)
        area_list = self.get_area_list(html_str)
        for i in range(len(area_list)):
            next_area_url = area_list.pop()
            if next_area_url is not  None:
                # 发送请求
                html_str1 = self.parse_url(next_area_url)
                # 提取数据
                self.get_house_detail(html_str1)



if __name__ == '__main__':

    ziru = ZiruSpider()
    ziru.run()




