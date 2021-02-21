 #-*-coding:utf-8-*-

from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

import importlib,sys
importlib.reload(sys)

class Textnow:  

  def __init__(self, TN_USER, TN_PASS, PHONE_NUMBER, MESSAGE):
    self.TN_USER = TN_USER
    self.TN_PASS = TN_PASS
    self.PHONE_NUMBER = PHONE_NUMBER
    self.MESSAGE = MESSAGE
    self.url = "https://www.textnow.com/login"

  def send_text(self):

    #profile = webdriver.FirefoxProfile()
    #proxy = '127.0.0.1:10808'
    #ip, port = proxy.split(":")
    #port = int(port)
    ## 不使用代理的协议，注释掉对应的选项即可
    #settings = {
    #  'network.proxy.type': 1,
    #  'network.proxy.http': ip,
    #  'network.proxy.http_port': port,
    #  'network.proxy.ssl': ip,  # https的网站,
    #  'network.proxy.ssl_port': port,
    #}
    #
    ## 更新配置文件
    #for key, value in settings.items():
    #    profile.set_preference(key, value)
    #profile.update_preferences()
    
    #https://github.com/mozilla/geckodriver/releases
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')  # 无头参数
    #options.add_argument('-private')  # 隐身模式
    driver = webdriver.Firefox(options=options)
    #
    #driver = webdriver.Firefox(executable_path='geckodriver', options=options)
    #driver = webdriver.Firefox(firefox_profile=profile, options=options)
    #driver = webdriver.Firefox(proxy = proxy)

    #https://sites.google.com/a/chromium.org/chromedriver/home
    #options = webdriver.ChromeOptions()
    #options.add_argument('--headless')# 无头参数
    #options.add_argument('--disable-web-security')# 禁用web安全参数
    #options.add_argument('--incognito')# 无痕参数
    #options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"')# user-agent参数
    
    #chrome_driver = '/opt/hostedtoolcache/Python/3.7.9/x64/lib/python3.7/site-packages/seleniumbase-1.42.4-py3.7.egg/seleniumbase/drivers/chromedriver'  #chromedriver的文件位置
    #driver = webdriver.Chrome(executable_path = chrome_driver, chrome_options=options)   
    
    #这两种设置都进行才有效
    #driver.set_page_load_timeout(5)
    #driver.set_script_timeout(5)
    
    
    try:
        driver.get(self.url)
    except:
        pass
    
    # 分辨率 1920*1080
    driver.set_window_size(1920,1080)
    time.sleep(10)

    #presence_of_element_located： 当我们不关心元素是否可见，只关心元素是否存在在页面中。
    #visibility_of_element_located： 当我们需要找到元素，并且该元素也可见。
    
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='username']")))
    uname_box = driver.find_element_by_xpath("//input[@name='username']")
    pass_box = driver.find_element_by_xpath("//input[@name='password']")
    uname_box.send_keys(self.TN_USER)
    pass_box.send_keys(self.TN_PASS)

    login_btn = driver.find_element_by_xpath("//button[@type='submit']")
    login_btn.click()

    #显性等待，每隔3s检查一下条件是否成立
    try:
      WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='notification-priming-modal']")))
    except:
      pass

    print(u'登录成功')
    # 隐性等待,最长等待30秒
    driver.implicitly_wait(30)

    # remove通知提示框
    driver.execute_script("document.querySelectorAll('#recent-header .toast-container').forEach(function(e,i){console.log(e.href)})")
    time.sleep(1)
   
    driver.execute_script("document.querySelectorAll('.notification-priming-modal').forEach(function(e,i){console.log(e.href)})")
    time.sleep(1)
    
    #检测jQuery是否存在，如果不存在，则手动加载一次
    driver.execute_script("if(!window.jQuery){var scriptEle=document.createElement('script');scriptEle.src='https://cdn.jsdelivr.net/gh/jquery/jquery@3.2.1/dist/jquery.min.js';document.body.append(scriptEle)}")
    time.sleep(3)
    
    driver.execute_script("$('#recent-header .toast-container').remove();")
    driver.execute_script("$('.notification-priming-modal').remove();")
    driver.execute_script("$('.modal').remove();")
    time.sleep(2)
    
    cookie = {}
    uid = driver.get_cookie('__cfduid')['value']
    sid = driver.get_cookie('connect.sid')['value']
    cookie['__cfduid'] = uid
    cookie['connect.sid'] = sid
    print(cookie)
    
    cookies = {
        '__cfduid': uid,
        'connect.sid': sid,
    }
    headers = {
        'authority': 'www.textnow.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-csrf-token': 'yraqsLnx-qfRfOVFEuMwbc0D-pPXO-9K0tLU',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.textnow.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.textnow.com/messaging',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    data = {
        "contact_value":self.PHONE_NUMBER,
        "message":self.MESSAGE
    }
    url = 'https://www.textnow.com/api/users/brf2053/messages'
    response = requests.post(url=url,headers=headers,cookies=cookies,data=data)
    print(response.text)
    

    
    
    driver.quit()
    
