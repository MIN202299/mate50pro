from ast import main
from selenium import webdriver
from multiprocessing import Process
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import os
import time

# 登陆链接
LOGIN_URL = 'https://hwid1.vmall.com/CAS/portal/login.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Facaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'
# 购买链接
GOODS_URL = 'https://www.vmall.com/product/10086238622707.html'
# chrome_driver path mac os
CHROME_DRIVER_PATH = os.path.join(os.path.abspath('.'), 'webdriver/chromedriver')

# 开启的drivers
drs = []

def buyPhone():
  global drs
  driver = webdriver.Chrome(service=ChromeService(executable_path=CHROME_DRIVER_PATH))
  drs.append(driver)
  driver.get(GOODS_URL)
  # 等待元素加载完全
  driver.implicitly_wait(10)
  # 在此期间收动登录
  mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')
  if mall_btn.text == '立即登录':
    mall_btn.click()
  # 在此期间手动登录  
  time.sleep(60)
  while True:
    try:
        mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')
        print(mall_btn.get_attribute('class'))
        if mall_btn.get_attribute('class') != 'product-button02 disabled':
            mall_btn.click()
            print('click')
    except Exception as err:
        mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')
        print(err)


if __name__=='__main__':
  process_list = []
  cup_nums = os.cpu_count()
  # 正式切换为cup_nums
  for i in range(4):
    p = Process(target=buyPhone)
    process_list.append(p)
  for p in process_list:
    p.start()
  for p in process_list:
    p.join()
