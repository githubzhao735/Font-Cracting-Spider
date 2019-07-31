import json

import requests



class Douban_spider():

    def __init__(self):
         self.url_temp = "https://m.douban.com/rexxar/api/v2/subject_collection/tv_american/items?start={}&count=18&loc_id=108288"
         self.headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0"}

    def pase_url(self,url):

        response = requests.get(url,headers = self.headers)
        return response.content.decode()

    def get_data(self,json_str):
        dict_data = json.loads(json_str)
        print(dict_data)
        content_list = dict_data["subject_collection_items"]
        return content_list

    def save_content_list(self,content_list):
        with open('douban.txt','a',encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content,ensure_ascii=False))
                f.write('\n')

    def run(self):
        num =0

         #构建url
        url_temp = self.url_temp.format(num)
        #发送请求
        json_str = self.pase_url(url_temp)
       #提取数据
        content_list = self.get_data(json_str)
        #保存数据
        self.save_content_list(content_list)

if __name__ == '__main__':

    douban = Douban_spider()
    douban.run()