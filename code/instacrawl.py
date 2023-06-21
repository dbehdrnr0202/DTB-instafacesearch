import time
import os
import argparse

from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


parser = argparse.ArgumentParser(description='arguments instagram_id instagram_pw')
parser.add_argument('id', type=str)
parser.add_argument('pw', type=str)
args = parser.parse_args()

img_folder = './crawling_img'
WAIT_SEC = 5
IMG_NUM = 1000

def login(driver, id, pw):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(WAIT_SEC)

    input = driver.find_elements(By.TAG_NAME, "input")
    input[0].send_keys(id)
    input[1].send_keys(pw)
    input[1].send_keys(Keys.RETURN)
    time.sleep(WAIT_SEC)

    btn_later1 = driver.find_element(By.CLASS_NAME, '_acan')
    btn_later1.click()
    time.sleep(WAIT_SEC)
    btn_later2 = driver.find_element(By.CLASS_NAME ,'_a9--')
    btn_later2.click()
    time.sleep(WAIT_SEC)

def img_download(driver, name, url):
    driver.get(url)

    index = 0
    if not os.path.isdir(f'{img_folder}/img'):
        os.mkdir(f'{img_folder}/img')
    if not os.path.isdir(f'{img_folder}/img/{name}'):
        os.mkdir(f'{img_folder}/img/{name}')

    #스크롤 내리기 이동 전 위치
    scroll_location = driver.execute_script("return document.body.scrollHeight")

    is_crawling_continue = True

    while is_crawling_continue:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(WAIT_SEC)
        
        imgdivs = driver.find_elements(By.CLASS_NAME ,'_aagv')
        for imgdiv in imgdivs:
            imgurl = imgdiv.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            if not os.path.exists(f'{img_folder}/img/{name}/{imgurl[60:100]}.jpg'):
                urlretrieve(imgurl, f'{img_folder}/img/{name}/{imgurl[60:100]}.jpg')
                index += 1

                if index > IMG_NUM: is_crawling_continue = False
                else: print(f"{name}/ index: {index}/{IMG_NUM}")
        
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        if scroll_location == scroll_height:
            break
        else:
            scroll_location = driver.execute_script("return document.body.scrollHeight")

driver = webdriver.Chrome(ChromeDriverManager().install())

userId = args.id
userPw = args.pw

login(driver, userId, userPw)

with open(f"{img_folder}/accounts.txt") as accounts:
    while True:
        line = accounts.readline()
        if not line: break
        name, url = line.split(",")
        img_download(driver, name, url)
        time.sleep(WAIT_SEC)

driver.close()