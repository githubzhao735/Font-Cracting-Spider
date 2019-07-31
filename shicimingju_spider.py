import os
import time

import requests
from lxml import etree

class ShiciSpider():

    def __init__(self):
        self.start_url = "http://www.shicimingju.com/book/"
        self.headers = {

                "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36"
        }

    def get_book_url(self,url):#获取诗词url
        resp = requests.get(url=url,headers=self.headers)
        book_html_tree = etree.HTML(resp.text)
        book_list = book_html_tree.xpath("//div[@class='bookmark-list']/ul/li")
        for book in book_list:
            item = {}
            item['book_title'] = book.xpath(".//a/text()")[0]
            item['book_url'] = "http://www.shicimingju.com" + book.xpath(".//a/@href")[0]

            yield item

    def get_book_title(self,book_list):#提取每本书的章节url
        for book in book_list:
            resp = requests.get(url=book.get('book_url'), headers=self.headers)
            book_mulu_tree = etree.HTML(resp.text)
            book_mulu_list = book_mulu_tree.xpath("//div[@class='book-mulu']/ul/li")
            for book_mulu in book_mulu_list:
                item = {}
                item["book_title"] = book.get("book_title")
                item["book_mulu"] = book_mulu.xpath("./a/text()")[0] if len(book_mulu.xpath("./a/text()"))>0 else None
                item["book_mulu_url"] = "http://www.shicimingju.com" + book_mulu.xpath("./a/@href")[0] if len(book_mulu.xpath("./a/@href"))>0 else None
                time.sleep(1)
                yield item

    def save_book_content(self,book_mulu_list):#保存内容
        dirname_list =self.get_book_url(self.start_url)
        dirlist = [dir.get("book_title")for dir in dirname_list]
        for dir in dirlist:
            dir1 = os.mkdir(dir)
        for dirname in dirlist:
            for book_mulu in book_mulu_list:
                if dirname == book_mulu.get("book_title"):
                    try:
                        with open(dirname+"/"+book_mulu.get("book_mulu")+".txt","a") as f:
                            resp = requests.get(url=book_mulu.get("book_mulu_url"), headers=self.headers)
                            book_content_tree = etree.HTML(resp.text)
                            book_content = "".join(book_content_tree.xpath("//div[@class='chapter_content']//text()"))
                            f.write(book_content)
                    except Exception as e:
                        pass

    def run(self):#实现主要逻辑
        #发送请求，获取所有诗词url
        book_list = self.get_book_url(self.start_url)

        #提取每本书的章节url
        book_mulu_list = self.get_book_title(book_list)

        #提取每一张的内容,并保存
        self.save_book_content(book_mulu_list)

if __name__ == '__main__':

    shici = ShiciSpider()
    shici.run()
