#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 21:28:38 2019

@author: Harshit Jain and Mohit Khemchandani

CHROMEDRIVER VERSION USED : 80
"""

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as ec
#from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from time import sleep
import os
import time

CURR_DIR=os.getcwd()
cm_ex=os.popen("nmcli dev show | grep 'IP4\.ADDRESS'|awk '{print $2}'|sed '1q'")
ip_addr=cm_ex.readline().strip()


a=ip_addr.split('.')
b=a[3].split('/')
del(a[3])
b[0]='0'
ip_addr='.'.join(a)+'.'+'/'.join(b)

command="nmap -sP "+ip_addr+" -oG - | awk '/Up$/{print $2}' > {}".format(CURR_DIR)+"/hosts.txt"
os.system(command)  #Change the path to your home directory 
uname='username'  #username here
pass1='password'  #password here
driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get("https://localhost:8834/") #nessus url here
wait = ui.WebDriverWait(driver,30)
user=wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div/form/div[1]/input")))
user.send_keys(uname)
pass2=driver.find_element_by_xpath('/html/body/div/form/div[2]/input')
pass2.send_keys(pass1)

log_in=driver.find_element_by_xpath('/html/body/div/form/button')
log_in.click()

sleep(3)

new_scan=driver.find_element_by_xpath('//*[@id="titlebar"]/a[1]')
new_scan.click()
sleep(2)
advan_scan=driver.find_element_by_xpath('//*[@id="content"]/section/div[1]/a[2]')
advan_scan.click()
sleep(3)
tim=time.asctime(time.localtime(time.time())).split()
scan_name=tim[2]+'_'+tim[1]+'_'+tim[4]+'_'+tim[3]
name=wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="editor-tab-view"]/div/div[1]/section/div[1]/div[1]/div[1]/div[1]/div/input')))
name.send_keys(scan_name)

file_path='/hosts.txt'
sleep(3)
upload_ele=driver.find_element_by_xpath('//*[@id="editor-tab-view"]/div/div[1]/section/div[1]/div[1]/div[1]/div[6]/div/input')
upload_ele.send_keys(os.getcwd()+file_path)
sleep(5)
drop=driver.find_element_by_xpath('//*[@id="content"]/section/form/div[2]/i')
drop.click()
launch_scan=driver.find_element_by_xpath('//*[@id="content"]/section/form/div[2]/ul/li')
launch_scan.click()

scan_open=wait.until(ec.element_to_be_clickable((By.XPATH,'/html/body/section[3]/section[3]/section/div[2]/table/tbody/tr/td[4]')))
scan_open.click()
while True:
    try:
        wait.until(ec.visibility_of_element_located((By.XPATH,'/html/body/section[3]/section[3]/section/div[1]/div[2]/span[11]')))
        wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="export"]')))
        exp=driver.find_element_by_xpath('//*[@id="export"]')
        exp.click()
    except Exception as e:
        pass
    else:
        break
pdf_d=driver.find_element_by_xpath('/html/body/section[3]/section[1]/span[1]/ul/li[2]')
pdf_d.click()
pop_p=wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="export-save"]')))
pop_p.click()
