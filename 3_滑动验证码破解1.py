from selenium import webdriver
from time import sleep
from PIL import Image
from selenium.webdriver import ActionChains

# 辅助函数1、截图
def shot_img(driver):
    sleep(2)
    # 截整个浏览器界面的图
    driver.save_screenshot("./page.png")
    # 加载截图
    img = Image.open("./page.png")
    # 从整张界面图中提取出验证码区域的截图
    loc = driver.find_element_by_class_name("geetest_slicebg").location # 取出验证码区域的位置
    size = driver.find_element_by_class_name("geetest_slicebg").size # 取出验证码区域的大小
    print(loc,size)
    # {'x': 388, 'y': 158} {'height': 159, 'width': 258}
    # {'x': 388, 'y': 158} {'height': 159, 'width': 258}

    # 计算验证码区域的截图范围
    top = loc["y"]
    left = loc["x"]
    right = loc["x"] + size["width"]
    bottom = loc["y"] + size["height"]
    print(left,top,right,bottom)  #388 158 646 317

    # 根据截图区域的范围来截取出图片
    code_img = img.crop((left,top,right,bottom)) # 经验告诉我乘以2好使
    # code_img.show()
    return code_img
# 辅助函数2、就是缺口的距离
def get_distance(img1,img2):
    print(img1,img2)
    # 寻找缺口图和无缺口的图之间像素的差异，只需要找到第一个存在差异的像素取出该像素的x位置就是缺口到起始点的距离
    for i in range(50,img1.size[0]):
        print(img1.size)
        print(img2.size)
        print(img1.size[0])   #拿高度作为x轴？？有问题吧？打印结果发现：这里是宽度
        print(img1.size[1])
        for j in range(img1.size[1]):
            print(img1.size[1])
            # 加载rgb值
            rgb1 = img1.load()[i,j]
            print(rgb1)
            rgb2 = img2.load()[i,j]
            # 计算两张图片rbg的差异
            r = abs(rgb1[0] - rgb2[0])
            g = abs(rgb1[1] - rgb2[1])
            b = abs(rgb1[2] - rgb2[2])
            # 判断，如果r、g、b三个的差异都大于60，则判断为缺口位置
            if r>30 and g>30 and b>30:
                print(i)
                return i-6
# 辅助函数3、生成一个滑块移动的轨迹
def get_tracks(distance):
    print('******')
    print(distance)
    # 拖动的时候多拖出去20
    # distance += 20
    v = 0
    t = 0.2
    # 定义一个列表，用于存放向前滑动的轨迹（每次向前滑动的距离）
    forwards = []
    # 当前位置
    current = 0
    # 中间位置
    mid = distance*3/5
    while current < distance:
        if current < mid:
            a = 3
        else:
            a = -3
        s = v*t + 0.5*a*(t**2)
        v = a*t + v
        current += s
        forwards.append(round(s))

    print(forwards)
    #forwards 列表的和刚好等于distance，距离不加长的话，下边的后退也就不用执行了
    return {"forwards":forwards,"backs":[-3,-3,-2,-2,-3,-2,-2,-1,-1,-1]}




# 封装一个函数，用于破解滑动验证码
def crack_code(driver):
    # 1、求滑动距离
    # 1）截取带缺口的图
    img1 = shot_img(driver)
    # 2）去掉缺口
    # 写一个js语句就可以执行然后去缺口
    js = "document.querySelector('.geetest_canvas_slice').style.display='block';document.querySelector('.geetest_canvas_slice').style.zIndex=10;document.querySelector('.geetest_canvas_fullbg').style.display='block';"
    driver.execute_script(js)

    # 3）截取不带缺口的图
    img2 = shot_img(driver)
    # 4）两张图都截取完毕了，接下来要让图片恢复原状
    js = "document.querySelector('.geetest_canvas_slice').style.display='block';document.querySelector('.geetest_canvas_slice').style.zIndex=10;document.querySelector('.geetest_canvas_fullbg').style.display='none';"
    driver.execute_script(js)
    # 5）根据带缺口和不带缺口的两张图来计算法缺口和起始点的距离
    distance = get_distance(img1,img2)
    print(distance)

    # 2、模拟人类的动作来滑动滑块
    # 用ActionChains对象来模拟人类动作

    btn = driver.find_element_by_class_name("geetest_slider_button")
    # 按住按钮
    ActionChains(driver).click_and_hold(btn).perform()
    # 按照一定的轨迹来拖动
    # 向前的轨迹
    tracks = get_tracks(distance)

    for track in tracks["forwards"]:
        ActionChains(driver).move_by_offset(yoffset=0,xoffset=track).perform()
    sleep(0.5)
    # for track in tracks["backs"]:
    #     ActionChains(driver).move_by_offset(yoffset=0,xoffset=track).perform()
    # sleep(0.5)
    # 松开手
    ActionChains(driver).release().perform()

# 封装一个函数用于登录
def login_blogs(name,password):
    # 登录页面的接口
    login_page = "https://account.cnblogs.com/signin"
    driver = webdriver.Chrome()
    try:
        driver.get(login_page)
        sleep(1)
        # 找到相关的表单将用户名和密码输入
        driver.find_element_by_id("LoginName").send_keys(name)
        driver.find_element_by_id("Password").send_keys(password)
        # 点击登录按钮
        driver.find_element_by_class_name("ladda-label").click()

        # 登录按钮按下以后会弹出滑动验证码界面，接下来破解
        crack_code(driver)

        sleep(5)

    finally:
        driver.close()






if __name__ == '__main__':
    login_blogs("qwer","qwer")
