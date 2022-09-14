import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from config import USER_CONFIG
# 登陆链接
LOGIN_URL = 'https://hwid1.vmall.com/CAS/portal/login.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Facaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'
# 购买链接
GOODS_URL = 'https://www.vmall.com/product/10086238622707.html'
# chrome_driver path mac os
CHROME_DRIVER_PATH = os.path.join(os.path.abspath('.'), 'webdriver/chromedriver')

# chrome user profile mac os chrome://version 可以查看
CHROME_USER_DATA = r'C:/Users/pm/AppData/Local/Google/Chrome/User Data/Default'

BEGIN_GO = '2022-09-14 10:07:50'
END = '2022-09-14 10:09:50'

def loginMall():
    print(USER_CONFIG)
    is_login = False
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(r'--user-data-dir={}'.format(CHROME_USER_DATA))
    global driver # 防止浏览器自动关闭
    driver = webdriver.Chrome(service=ChromeService(executable_path=CHROME_DRIVER_PATH), options=chrome_options)
    driver.get(LOGIN_URL)
    # 等待元素加载完全
    driver.implicitly_wait(1)
    try:
        # hwid-getAuthCode 获取验证码
        # hwid-login-btn 登陆
        el_user = driver.find_element(By.CLASS_NAME, 'userAccount')
        el_password = driver.find_element(By.CLASS_NAME, 'hwid-input-pwd')
        el_login_btn = driver.find_element(By.CLASS_NAME, 'hwid-login-btn')
        el_user.send_keys(USER_CONFIG['USE_NAME'])
        el_password.send_keys(USER_CONFIG['PASSWORD'])
        el_login_btn.click()
        # 等待加载出dialog
        time.sleep(5)
        if driver.current_url == 'https://www.vmall.com/index.html':
            is_login = True
        else:
            el_get_auth_code = driver.find_element(By.CLASS_NAME, 'hwid-getAuthCode')
            el_get_auth_code.click()
            time.sleep(10)
            is_login = True
    except Exception as err:
        print('找不到元素，请尝试增加等待时常', err)
        # driver.quit()
    if is_login:
        driver.get(GOODS_URL)
        time.sleep(3)
        mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')
        if mall_btn.text == '立即登录':
            mall_btn.click()
        time.sleep(5)
        mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')    
        print(mall_btn.text)
        print(mall_btn.get_attribute('class'))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '准备开抢')
        timestamp = time.mktime(time.strptime(BEGIN_GO, '%Y-%m-%d %H:%M:%S'))
        while True:
            if time.time() > timestamp:
                try:
                    mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')
                    if mall_btn.get_attribute('class') != 'product-button02 disabled':
                        mall_btn.click()
                        print('click')
                except Exception as err:
                    mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')
                    print(err)
        pass

if __name__ == '__main__':
    loginMall()

