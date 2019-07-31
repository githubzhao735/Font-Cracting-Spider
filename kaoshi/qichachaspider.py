
import requests
from lxml import etree
import time
import threading
class GetallPage():

    def __init__(self):

        self.start_url = "https://www.qichacha.com/gongsi_area.shtml?prov=GD&city=440100&p=1"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

    def get_all_pages(self,url):


        resp = requests.get(url=url,headers=self.headers)
        html_tree = etree.HTML(resp.text)
        page_url = "https://www.qichacha.com"+html_tree.xpath("//ul[@class='pagination pagination-md']/li/a[@class='next']/@href")[0] if len(html_tree.xpath("//ul[@class='pagination pagination-md']/li/a[@class='next']/@href")) >0 else None
        # time.sleep(0.5)

        if page_url:
            self.get_all_pages(page_url)
        page_list =[]
        page_list.append(page_url)
        print(page_list)
        return page_list

    def run(self):
        companies = self.get_all_pages(self.start_url)
        return companies

class GetDetail(threading.Thread):
    def __init__(self,url):
        super().__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

        self.url = url
    def get_detail(self):

        resp = requests.get(url=self.url,headers=self.headers)
        html_tree = etree.HTML(resp.text)

        companies = html_tree.xpath("//section[@id='searchlist']//tr")

        for company in companies:
            item = {}
            item["title"] = "".join(company.xpath(".//a//text()"))
            item["company_detail"] = "".join(company.xpath(".//p[1]//text()")).strip()
            print(item)

    def run(self):


        self.get_detail()


if __name__ == '__main__':

    company = GetallPage()
    company_list = company.run()
    t_list = []
    for company in company_list:
        t = GetDetail(company)
        t.start()

    for t in t_list:
        t.join()



