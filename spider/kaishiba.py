#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

import time
import pandas as pd
from selenium import webdriver

# 其他浏览器把Chrome换名就行
option = webdriver.ChromeOptions()
option.headless = True


driver = webdriver.Chrome('./chromedriver', options=option)  # 创建driver实例

def is_element_exist(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except BaseException:
        return False
    return True


login_xpaht = '//*[@id="userLogout"]/a[1]'
user_name_xpath = '/html/body/div[2]/div[2]/form/div[1]/label/input'
pass_wd_xpath = '/html/body/div[2]/div[2]/form/div[2]/label/input'
hotel_xpath = '//*[@id="app"]/div/div[3]/ul/li[{}]/div/a'
item_xpath = '//*[@id="app"]/div/div[3]/ul/li[1]'
login_button_xpaht = '/html/body/div[2]/div[2]/form/div[5]/input'
founder_xpath = '//*[@id="app"]/div/div[3]/ul/li[{}]/div/div/div/div[1]/div/span'
about_xpath = '//*[@id="about"]'
my_project_xpath = '//*[@id="myProject"]'
why_xpath = '//*[@id="why"]'
url = 'https://www.kaishiba.com/project/more'

driver.get(url)

driver.find_element_by_xpath(login_xpaht).click()
username = driver.find_element_by_xpath(user_name_xpath)
passwd = driver.find_element_by_xpath(pass_wd_xpath)
username.send_keys("test")
passwd.send_keys("test")
driver.find_element_by_xpath(login_button_xpaht).click()
time.sleep(1)
content = []
for i in range(600, 3000):
    print("now i is {}".format(i))
    while not is_element_exist(hotel_xpath.format(i)):
        driver.execute_script('window.scrollBy(0,10000)')  # 相对当前坐标移动
    item = dict()
    if driver.find_element_by_xpath(founder_xpath.format(i)).text == '开始吧':
        print('start self!!!')
        continue
    driver.find_element_by_xpath(hotel_xpath.format(i)).click()

    handles = driver.window_handles
    for handle in handles:
        if handle != driver.current_window_handle:
            driver.switch_to.window(handle)
            break
    time.sleep(2)

    item['编号'] = i
    if not is_element_exist(about_xpath):
        print("error in about, continue")
        driver.close()
        for handle in handles:
            driver.switch_to.window(handle)
            break
        continue

    if not is_element_exist(my_project_xpath):
        print("error in my_project_xpath, continue")
        driver.close()
        for handle in handles:
            driver.switch_to.window(handle)
            break
        continue
    if not is_element_exist(why_xpath):
        print("error in why_xpath, continue")
        driver.close()
        for handle in handles:
            driver.switch_to.window(handle)
            break
        continue
    item['我的自述'] = driver.find_element_by_xpath(about_xpath).text
    item['我的项目'] = driver.find_element_by_xpath(my_project_xpath).text
    item['为何发起'] = driver.find_element_by_xpath(why_xpath).text
    driver.close()
    for handle in handles:
        driver.switch_to.window(handle)
        break
    content.append(item)
    if i % 50 == 0:
        pd.DataFrame(content).to_csv("test{}.csv".format(i), encoding='gb18030', index=False)
        content = []

