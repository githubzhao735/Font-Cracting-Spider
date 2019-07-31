import json
from lxml import etree

import requests
import re

class Neihan():

    def __init__(self):
        self.start_url = "https://www.qiushibaike.com/text/page/{}/"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }

    def parse_url(self,url):#发送请求
        response = requests.get(url,headers = self.headers)
        return response.content.decode()

    def get_first_page_content_list(self,html_str):#提取数据
        content_list = re.findall(r"<div class=\"content\">.*?<span>(.*?)</span>",html_str,re.S)
        new_content_list = []
        for content in content_list:
            ret = re.sub('\n',"",content)
            new_content_list.append(ret)
        return new_content_list

    def save_content_list(self,content_list):#保存数据
        with open("neihan.txt","a",encoding="utf-8") as f:
            for content in content_list:
                f.write(content)
                f.write("\n")
                f.write("\n")

    def run(self):

        num = 1

        while num <= 13:
            #构建url地址
            url = self.start_url.format(num)
            #发送请求
            html_str = self.parse_url(url)

            #提取数据
            content_list = self.get_first_page_content_list(html_str)
            # print(content_list)
            #保存数据
            self.save_content_list(content_list)
            #构造下一个请求的url地址
            num +=1



if __name__ == '__main__':

    neihan = Neihan()

    neihan.run()


