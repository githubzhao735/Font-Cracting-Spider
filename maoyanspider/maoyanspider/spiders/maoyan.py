# -*- coding: utf-8 -*-
import scrapy
import re
import requests
from lxml import etree
from fontTools.ttLib import TTFont

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/1']


    def parse(self, response):
        #正则匹配拿到字体编码的url
        woff_url = "http:" + re.findall(r"url\('(.*?)'\) format\('woff'\);",response.text)[0]

        resp = requests.get(url=woff_url)

        with open("./online.woff","wb") as f: #把字体编码文件下载到本地
            f.write(resp.content)

        font = TTFont("./online.woff")
        font.saveXML('online.xml')

        font_local = TTFont("./base.woff")
        font_local.saveXML('base.xml')

        onlinecode_list = font.getGlyphNames()[1:-1]
        basecode_list = font_local.getGlyphNames()[1:-1]

        base_local_dict = {
            "uniF412":8,
            "uniF28F":4,
            "uniE3DD":7,
            "uniE990":3,
            "uniF16F":0,
            "uniF70E":6,
            'uniF829':1,
            'uniF30D':2,
            'uniF01D':9,
            'uniF3F5':5,
        }
        dict_relation = {}
        for k in basecode_list: #与基模板进行比较，形成一个对比字典
            obj_local = font_local['glyf'][k]
            # xMin = "0"
            # yMin = "0"
            # xMax = "511"
            # yMax = "707"
            # print(obj_local.xMin,obj_local.yMin,obj_local.xMax,obj_local.yMax)
            for v in onlinecode_list:
                obj_online = font['glyf'][v]
                # if obj_local.xMax == obj_online.xMax and obj_local.yMax == obj_online.yMax and obj_local.xMin == obj_online.xMin and obj_local.yMin == obj_online.yMin:
                if obj_local == obj_online:
                    #得到关系字典
                    dict_relation[v.strip('uni')] = base_local_dict[k]
        # print(dict_relation)

        #用正则匹配票房字符编码
        code_str_list = re.findall(r'<p class="total-boxoffice">总票房:.*<span><span class="stonefont">(.*?);</span>',response.text)

        total_boxoffice = []
        for code in code_str_list:#循环拿出所有电影的票房总数
            data = ''
            code = code.replace("&#x",'').upper()
            code_list = code.split(';')
            for percode in code_list:
                if len(percode) == 5:
                    data += '.'
                    percode = percode.strip('.')
                fanpa_data = str(dict_relation[percode])
                data += fanpa_data
            total_boxoffice.append(data)

        html_tree = etree.HTML(response.text)
        movie_list = html_tree.xpath("//dl[@class='board-wrapper']/dd")

        for movie in movie_list:
              item = {}
              item["movie"] = movie.xpath(".//p[@class='name']/a/text()")[0]
              item["star"] = movie.xpath(".//p[@class='star']/text()")[0]
              item["releasetime"] = movie.xpath(".//p[@class='releasetime']/text()")[0]
              item["total-boxoffice"] ="".join(re.findall(r'\S',(movie.xpath(".//p[@class='total-boxoffice']//text()")[0]+total_boxoffice[movie_list.index(movie)]+movie.xpath(".//p[@class='total-boxoffice']//text()")[2]).strip()))
              print(item)









