from ast import main
from sqlite3 import Timestamp
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

BEGIN_GO = '2022-09-15 10:07:50'
END = '2022-09-15 10:10:00'

# 开启的drivers
drs = []

def buyPhone():
  global drs
  driver = webdriver.Chrome(service=ChromeService(executable_path=CHROME_DRIVER_PATH))
  drs.append(driver)
  driver.get(GOODS_URL)
  # 等待元素加载完全
  driver.implicitly_wait(10)
  # begin time
  Timestamp = time.mktime(time.strptime(BEGIN_GO, '%Y-%m-%d %H:%M:%S'))
  EndTimestamp = time.mktime(time.strptime(END, '%Y-%m-%d %H:%M:%S'))
  mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')
  if mall_btn.text == '立即登录':
    mall_btn.click()
  print('-----------请在120秒内手动扫码登录账号准备开抢---------------------')  
  # 在此期间手动登录  
  time.sleep(120)
  print('[{0}] {1}:准备开抢'.format(os.getpid(), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
  while True:
    if time.time() > Timestamp:
        try:
          mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')
          print(mall_btn.get_attribute('class'))
          if mall_btn.get_attribute('class') != 'product-button02 disabled':
              mall_btn.click()
              print('click')
        except Exception as err:
            mall_btn = driver.find_element(By.ID, 'pro-operation').find_element(By.CLASS_NAME, 'product-button02')
            print(err)
    if time.time() > EndTimestamp:
        break


if __name__=='__main__':
  process_list = []
  cup_nums = os.cpu_count()
  # 正式切换为cup_nums
  for i in range(cup_nums):
    p = Process(target=buyPhone)
    process_list.append(p)
  for p in process_list:
    p.start()
  for p in process_list:
    p.join()
