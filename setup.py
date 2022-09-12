import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

abs_path = os.path.abspath('.')

webdriver_path = os.path.join(abs_path, 'webdriver/chromedriver')

# 休眠
# secTime = int(time.mktime(time.strptime('2022-09-12 10:06:00', '%Y-%m-%d %H:%M:%S'))) * 1000
#
# deadTime = int(time.mktime(time.strptime('2022-09-12 10:10:00', '%Y-%m-%d %H:%M:%S'))) * 1000
#
# now = int(time.time() * 1000)
#
# while now < secTime:
#     now = int(time.time() * 1000)
#     print('休眠10秒钟')
#     time.sleep(10)


driver = webdriver.Chrome(service=ChromeService(executable_path=webdriver_path))

driver.get('https://www.vmall.com/product/10086238622707.html')

# 倒计时结束开抢

ToCountDown = 30

for i in range(ToCountDown):
    time.sleep(1)
    print('剩余{0}秒开始秒杀！'.format(ToCountDown - i))


btn1 = driver.find_element(By.ID, 'pro-operation')

miao_sha_btn = btn1.find_element(By.CLASS_NAME, 'product-button02')

print('获取到秒杀按钮', miao_sha_btn)
count = 0
# 默认抢 2 分钟
while True:
    now = int(time.time() * 1000)
    try:
        count += 1
        dt = datetime.datetime.now()
        print('时间[{1}]:点击按钮{0}'.format(count, dt.strftime('%Y-%m-%d %H:%M:%S %f')))
        miao_sha_btn.click()
    except Exception as err:
        print(err, '失败')
        break
