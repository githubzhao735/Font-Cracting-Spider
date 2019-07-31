import re
import time
from lxml import etree
import requests
from selenium import webdriver
import threading



class QiongyouSpider():
    def __init__(self):
        self.start_url = "http://guide.qyer.com/"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
        }
        self.driver = webdriver.Chrome()

    def parse_url(self,url):
        resp = requests.get(url = url,headers = self.headers)
        return resp.content.decode()

    def get_author_detail(self,book_url):#由于作者信息在响应中没有，定义一个函数模拟浏览器提取
        self.driver.get(book_url)
        time.sleep(3)
        page_str = self.driver.page_source
        page_tree = etree.HTML(page_str)
        author_name = page_tree.xpath("//a[@class='author-name']/text()")
        return author_name

    def get_area_book_detail(self,html_str):#提取每本攻略的信息
        book_str = re.findall(r'{"continent":"中国","country":\[(.*)\]}\],', html_str)[0]
        area_book_list = re.findall(r'{"name":"(.*?)"."poi":\[(.*?)\]}',book_str)
        for area_book in area_book_list:
            item = {}
            item["area"] = area_book[0]
            book_content = re.findall(r'{"name":"(.*?)"."url":"(.*?)"}',area_book[1])
            for book in book_content:
                item["area_book_name"] = book[0]
                item["area_book_url"] = "http://guide.qyer.com/" + re.findall(r'.*u002F(.*?)\\u002F',book[1])[0] + "/"
                book_html_str = self.parse_url(item["area_book_url"])
                book_tree = etree.HTML(book_html_str)
                item["book_download"] = book_tree.xpath("//div[@class='info-table']/h5[6]/em/text()")[0]
                item["book_discript"] = book_tree.xpath("//p[@class='intro-text']/text()")[0]
                item["book_author"] = self.get_author_detail(item["area_book_url"])
                print(item)

        self.driver.close()

    def save_book_detail(self,area_book_detail_list):
        pass

    def run(self):
        #发送请求
        html_str = self.parse_url(self.start_url)
        #获取数据，得到每个地区的每一本书
        area_book_detail_list = self.get_area_book_detail(html_str)
        #保存数据
        self.save_book_detail(area_book_detail_list)

if __name__ == '__main__':

    qiongyou = QiongyouSpider()
    qiongyou.run()




