from time import ctime, sleep
from selenium import webdriver
from multiprocessing import Process
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import os
 
 # chrome user profile mac os chrome://version 可以查看
CHROME_USER_DATA = r'C:/Users/pm/AppData/Local/Google/Chrome/User Data/Default'
# chrome_driver path mac os
CHROME_DRIVER_PATH = os.path.join(os.path.abspath('.'), 'webdriver/chromedriver')

drs = []

def get_browser():
    try:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument(r'--user-data-dir={}'.format(CHROME_USER_DATA))
        driver = webdriver.Chrome(service=ChromeService(executable_path=CHROME_DRIVER_PATH), options=chrome_options)
        return driver
    except Exception as msg:
        print("启动浏览器出现异常：%s" % str(msg))

def test_baidu():
    driver = get_browser()
    global drs
    drs.append(driver)
    driver.get("https://www.baidu.com")
    sleep(2)
    print(driver.title)



def thread_browser(*args):
  process_list = []                     # 创建线程列表
  print(os.cpu_count())
  for i in range(os.cpu_count()):
      t = Process(target=test_baidu)    # 创建线程
      process_list.append(t)
  for t in process_list:
      t.start()                    # 启动线程
  for t in process_list:
      t.join()                     # 守护线程
  print("end all time %s"% ctime())
 
 
if __name__ == "__main__":
    thread_browser()
