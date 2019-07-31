from selenium import webdriver
from selenium.webdriver import ActionChains
from PIL import Image
import time

class SliceSpider():
    '''
    破解滑动验证码模拟登录，拿到服务端设置的cookie
    '''
    def __init__(self):
        self.login_url = "https://account.cnblogs.com/signin"
        self.driver = webdriver.Firefox()

    def shot_img(self):#此函数用于截取验证码区域的图片
        #先截取整张页面的图片
        self.driver.save_screenshot('./code.png')
        img = Image.open("./code.png")
        location = self.driver.find_element_by_class_name("geetest_slicebg").location
        size = self.driver.find_element_by_class_name("geetest_slicebg").size
        top = location["y"]
        left = location["x"]
        right = left + size["width"]
        bottom = top + size["height"]
        #截出验证码区域的图片
        code_img = img.crop((left*1.25,top*1.25,right*1.25,bottom*1.25))
        # code_img.show()
        return code_img

    def get_distance(self,img1,img2):
        for i in range(10,img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = img1.load()[i, j]
                rgb2 = img2.load()[i, j]
                # 计算两张图片rbg的差异
                r = abs(rgb1[0] - rgb2[0])
                g = abs(rgb1[1] - rgb2[1])
                b = abs(rgb1[2] - rgb2[2])
                # 判断，如果r、g、b三个的差异都大于60，则判断为缺口位置
                if r > 60 and g > 60 and b > 60:
                    return i/1.5 -15

    def get_tracks(self,distance):
        # 拖动的时候多拖出去20
        # distance += 20
        v = 0
        t = 0.2
        # 定义一个列表，用于存放向前滑动的轨迹（每次向前滑动的距离）
        forwards = []
        # 当前位置
        current = 0
        # 中间位置
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            s = v * t + 0.5 * a * (t ** 2)
            v = a * t + v
            current += s
            forwards.append(round(s))

        return {"forwards": forwards}



    def crack_code(self):#此函数用于破解滑动验证码
        #截取带缺口的图片
        code_img1 = self.shot_img()
        js = "document.querySelector('.geetest_canvas_slice').style.display='block';document.querySelector('.geetest_canvas_slice').style.zIndex=10;document.querySelector('.geetest_canvas_fullbg').style.display='block';"
        self.driver.execute_script(js)
        # 3）截取不带缺口的图
        code_img2 = self.shot_img()
        # 4）两张图都截取完毕了，接下来要让图片恢复原状
        js = "document.querySelector('.geetest_canvas_slice').style.display='block';document.querySelector('.geetest_canvas_slice').style.zIndex=10;document.querySelector('.geetest_canvas_fullbg').style.display='none';"
        self.driver.execute_script(js)

        #计算两张图片差异点的距离
        distance = self.get_distance(code_img1,code_img2)

        #模拟人类进行拖动
        bnt = self.driver.find_element_by_class_name("geetest_slider_button")
        ActionChains(self.driver).click_and_hold(bnt).perform()

        tracks = self.get_tracks(distance)
        for track in tracks["forwards"]:
            ActionChains(self.driver).move_by_offset(yoffset=0, xoffset=track).perform()
        time.sleep(0.5)
        # 松开手
        ActionChains(self.driver).release().perform()





    def click_login(self):#模拟浏览器登录，返回登陆后的cookie
        self.driver.get(self.login_url)
        self.driver.find_element_by_id("LoginName").send_keys("benjinment")
        self.driver.find_element_by_id("Password").send_keys("asdfghjkl;'123")
        time.sleep(3)
        self.driver.find_element_by_id("submitBtn").click()
        time.sleep(5)
        self.crack_code()
        time.sleep(10)
        cookies = self.driver.get_cookies()
        return cookies


    def run(self):
        #发送请求，拿到登录页面并且输入用户名和密码
        cookies = self.click_login()
        print(cookies)


if __name__ == '__main__':

    slice = SliceSpider()
    slice.run()