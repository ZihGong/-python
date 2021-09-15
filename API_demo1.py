# -*- coding = utf-8 -*-
# Author: 
# @Time : 2021/9/12 5:37 下午
# @File : API_demo1.py
# @Software: pythonProject
import operator
import re
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

delay = 0.5
refresh_time = 2
username = "xxx"
password = "xxx"
#启动chromedriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('window-size=1920x1080')
# 创建 WebDriver 对象，指明使用chrome浏览器驱动
#driver = webdriver.Chrome(executable_path='d:\selenium\chromedriver.exe',chrome_options = options) #linux版本，无图形
driver = webdriver.Chrome('/Users/gongzihan/Downloads/chromedriver')#将路径改为自己的chromedriver路径


def selfclick(xpath, driver=driver):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        temp = driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].click();", temp)
        driver.switch_to.window(driver.window_handles[-1])
    except:
        return "出错，未定位到元素"


def selfinput(xpath,input_element,driver=driver):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.find_element_by_xpath(xpath).send_keys(input_element)
    except:
        return "出错，未定位到元素"


def relocate():
    time.sleep(delay)
    search_window = driver.current_window_handle  # 此行代码用来定位当前页面


if __name__ == "__main__":
    driver.get("http://dean.xjtu.edu.cn")
    selfclick("/html/body/div[4]/div[1]/div[3]/div[4]/table/tbody/tr[2]/td[1]/a/img")

    relocate()

    selfinput('//*[@id="form1"]/input[1]', username)
    selfinput('//*[@id="form1"]/input[2]', password)
    selfclick('//*[@id="account_login"]')

    relocate()

    selfclick('/html/body/div[4]/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[1]/div/input')
    selfclick('//*[@id="buttons"]/button[2]')
    selfclick('//*[@id="courseBtn"]')

    relocate()

    while True:
        selfclick('//*[@id="recommendBody"]/div[7]')
        html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        # print(html)
        bs = BeautifulSoup(html, 'lxml')
        course_html = bs.find('div', id="202120221INFT30030501_courseDiv")
        is_full_try = re.findall('isfull="\d{1}"', str(course_html))
        is_full = re.findall('\d{1}', str(is_full_try))
        is_choose_try = re.findall('ischoose="1"|ischoose="null"', str(course_html))
        is_choose = re.findall('1|null', str(is_choose_try))
        if operator.eq(is_full, ['0']) and operator.eq(is_choose, ['null']):
            selfclick('//*[@id="202120221COMP55180501_courseDiv"]')
            selfclick('//*[@id="202120221COMP55180501_courseDiv"]/div[2]/div[2]/button[1]')
            print("success")
            break
        time.sleep(refresh_time)
        driver.refresh()
        print('refresh')

