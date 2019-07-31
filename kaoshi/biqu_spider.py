import requests
from lxml import etree
import os
import threading

import time



class BiquSpider():

    def __init__(self):
        self.start_url = "https://www.biquge5200.cc/xuanhuanxiaoshuo/"
        self.headers = {
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

        # self.proxy = {"http":"27.40.94.3:17541"}

    def parse(self,url):#发送请求，那大主页内容
        resp = requests.get(url = url,headers = self.headers)
        return resp.text

    def get_book_url(self,resp):

        html_tree = etree.HTML(resp)
        book_list = html_tree.xpath("//div[@id='newscontent']//ul/li")
        item_list =[]
        for book in book_list:
            item ={}
            item["book_name"] = book.xpath("./span[@class='s2']/a/text()")[0]
            item["book_url"] = book.xpath("./span[@class='s2']/a/@href")[0]
            if not os.path.exists("./" + item["book_name"]):
                os.mkdir("./" + item["book_name"])
            item_list.append(item)

        return item_list

    def run(self):  # 实现主要逻辑
        # 发送请求
        resp = self.parse(self.start_url)
        item_list = self.get_book_url(resp)
        return item_list


class GetDetail(threading.Thread):

    def __init__(self,book):
        super().__init__()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"

        }
        self.book = book

    def get_book_mulu(self):
        resp = requests.get(url=self.book["book_url"],headers = self.headers)
        mulu_tree = etree.HTML(resp.text)
        mulu_list = mulu_tree.xpath("//div[@id='list']/dl/dd")

        mulus = []
        for mulu in mulu_list:
            item = {}
            item["book_mulu"]= mulu.xpath("./a/text()")[0]
            item["book_mulu_url"] = mulu.xpath("./a/@href")[0]
            mulus.append(item)
        return mulus

    def get_book_mulu_content(self,mulu_list,lock):

        for mulu in mulu_list:
            with lock:
                resp = requests.get(url=mulu["book_mulu_url"], headers=self.headers)
                print("正在爬取的目录", mulu["book_mulu_url"])
                mulu_tree = etree.HTML(resp.text)
                mulu_content = "".join(mulu_tree.xpath("//div[@id='content']//text()")).replace("\u3000", '')
                print(mulu_content)
                with open("./" + self.book["book_name"] +"/"+mulu["book_mulu"]+".txt","w") as f:
                    f.write(mulu_content)
                time.sleep(6)

    def run(self):
        mulu_list = self.get_book_mulu()
        lock = threading.Lock()
        self.get_book_mulu_content(mulu_list,lock)

if __name__ == '__main__':

    biqu=  BiquSpider()
    book_list = biqu.run()

    t_list = []
    for book in book_list:
        t = GetDetail(book)
        t.start()
        t_list.append(t)
    for t in t_list:
        t.join()