import requests
import re
from w3lib.html import remove_comments
import json
from lxml import etree

class TieBa():

    def __init__(self,tiebaname):

        self.tiebaname = tiebaname
        self.start_url = "https://tieba.baidu.com/f?kw="+tiebaname+"&ie=utf-8&pn={}"
        self.headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36"}

    def parse_url(self,url):#发送请求
        response = requests.get(url,headers = self.headers)
        response = response.content.decode()
        return response

    def get_content_list(self,html_str):#提取数据
        html =  etree.HTML(html_str)
        li_list = html.xpath("//li[@class ='tl_shadow tl_shadow_new ']")
        content_list = []
        for li in li_list:
            item = {}
            item["title"] = li.xpath("./a/div[@class = 'ti_title']/span/text()")[0] if len(li.xpath("./a/text()"))>0 else None
            item["href"] = li.xpath("./a/@href")[0] if len(li.xpath("./a/@href"))>0 else None
            item['image_url'] = li.xpath("./a/div[@class='medias_wrap clearfix']/div[@class = 'medias_one_pic']/img/@src") if len(li.xpath("./a/div[@class='medias_wrap clearfix']/div[@class = 'medias_one_pic']/img/@src"))>0 else None
            content_list.append(item)
        return content_list


    def run(self):#实现主要逻辑
        num = 0
        #构建url地址
        url =self.start_url.format(num)

        #发送请求，获取响应
        html_str = self.parse_url(self.start_url)
        # print(html_str)

        #提取数据
        content_list = self.get_content_list(html_str)
        print(content_list)
        #保存数据


if __name__ == '__main__':

    tieba = TieBa("lol")

    tieba.run()