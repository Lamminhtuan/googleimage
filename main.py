from selenium import webdriver
import time
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
dv = webdriver.Firefox()
dv.get('https://images.google.com/')
#Nhập từ khóa cần tìm
search_key = 'porsche'
#Số lượng hình ảnh muốn download
max_images = 20
#Thời gian chờ
delay = 2
def scroll(dv, delay):
    dv.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(delay)
    try:
        dv.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[2]/div[2]/input').click()
        time.sleep(delay)
    except:
        pass
def get_images(dv, delay, max_images, search):
    box = dv.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    box.send_keys(search)
    box.send_keys(Keys.ENTER)
    images_url = set()
    time.sleep(delay)
    i = 1
    while len(images_url) < max_images:
        if i % 25 == 0:
            i += 1
            continue
        xpath = '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[{}]/a[1]/div[1]/img'.format(i)

        dv.find_element(By.XPATH, xpath).click()
        xpath_img = '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img'
        imagexpath = dv.find_element(By.XPATH, xpath_img)
        if imagexpath.get_attribute('src') in images_url:
            i += 1
            continue
        if imagexpath.get_attribute('src') and 'http' in imagexpath.get_attribute('src'):
            images_url.add(imagexpath.get_attribute('src'))
            print(f'Found {len(images_url)}')

        i += 1
    return images_url
def download_images(url, foldername, filename):
    if not os.path.isdir(foldername):
        os.makedirs(foldername)
    try:
        resonse = requests.get(url)
        if resonse.status_code == 200:
            with open(os.path.join(foldername, filename+'.jpg'), 'wb') as f:
                f.write(resonse.content)
                print('Downloaded')
    except Exception as e:
        print('Failed to download image', e)
urls = get_images(dv, delay, max_images, search_key)
for i, url in enumerate(urls):
    download_images(url, 'Downloads', search_key+str(i))
dv.close()
