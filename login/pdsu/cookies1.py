import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pytesseract

class PdsuCookies():
    def __init__(self, stunum, password, browser):
        self.url = 'http://jiaowu.pdsu.edu.cn/'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.stunum = stunum
        self.password = password

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        self.browser.switch_to.frame(self.browser.find_element_by_tag_name("iframe"))
        stunum = self.wait.until(EC.presence_of_element_located((By.ID, 'txt_asmcdefsddsd')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'txt_pewerwedsdfsdff')))
        stunum.send_keys(self.stunum)
        password.send_keys(self.password)
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btnlogin')))
        time.sleep(1)
        submit.click()

    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.ID, 'divLogNote'), '帐号或密码不正确！请重新输入。'))
        except TimeoutException:
            return False

    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            now_url = self.browser.current_url
            if now_url == "http://jiaowu.pdsu.edu.cn/MAINFRM.aspx":
                return True
            else:
                return False
        except TimeoutException:
            return False

    def get_position(self):
        """
        获取验证码位置
        :return: 识别后的验证码
        """
        try:
            img = self.wait.until(EC.presence_of_element_located((By.ID, 'imgCode')))
        except TimeoutException:
            print('未出现验证码')
            self.open()
        time.sleep(2)
        img = img.convert('L')
        threshold = 127
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        img = img.point(table,'1')
        result = pytesseract.image_to_string(img)
        return result


    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()

    def main(self):
        """
        破解入口
        :return:
        """
        self.open()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        # 获取验证码图片
        imgcode = self.wait.until(EC.presence_of_element_located((By.ID, 'txt_sdertfgsadscxcadsads')))
        imgcode.send_keys(self.get_position())
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        else:
            return {
                'status': 3,
                'content': '登录失败'
            }


if __name__ == '__main__':
    result = PdsuCookies('161360132','qwertyuiop').main()
    print(result)
