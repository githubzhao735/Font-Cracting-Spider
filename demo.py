from fontTools.ttLib import TTFont

font = TTFont("./ExCaATdo.ttf")

web = font.getBestCmap()



font1 = TTFont("./53cfe63b.woff")

font1.saveXML("./dazongdianping.xml")

font_list = font1.getGlyphNames()[1:-1]


print("起点中文网字体",web)
print("*"*100)
print("大众点评",font_list)






