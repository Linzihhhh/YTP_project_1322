from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
import os
import time
import requests

account = ''
password = ''

#open the msedgedriver.exe before runing the code
chrome_options = Options()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path = os.getcwd() + "\\chromedriver.exe",chrome_options=chrome_options)
url = 'https://www.pixiv.net/login.php?ref=wwwtop_accounts_index'
driver.get(url) #open the website
old_url = 'https://www.pixiv.net/login.php?ref=wwwtop_accounts_index'
element = driver.find_element(By.CLASS_NAME, "sc-bn9ph6-6.degQSE") #select the account entry
element.send_keys(account)
element = driver.find_element(By.CLASS_NAME, "sc-bn9ph6-6.hfoSmp") #select the password entry
element.send_keys(password)
button = driver.find_element(By.CLASS_NAME, "sc-bdnxRM.jvCTkj.sc-dlnjwi.pKCsX.sc-2o1uwj-7.fguACh.sc-2o1uwj-7.fguACh")
button.click() #login

WebDriverWait(driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,"sc-9y4be5-1.jtUPOE")))

items = driver.find_elements(By.CLASS_NAME, "sc-d98f2c-0.sc-rp5asc-16.iUsZyY.gtm-toppage-thumbnail-illustration-recommend-works.sc-iJCRrE.hizmCn")

tar = items[0]
for i in items:
    if i.get_attribute("data-gtm-recommend-score") > tar.get_attribute("data-gtm-recommend-score"):
        tar = i
goodpicture_url = tar.get_attribute("href")

driver.get(goodpicture_url)
WebDriverWait(driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "sc-1qpw8k9-1.jOmqKq")))

url = ''
try:
    img = driver.find_element(By.CLASS_NAME, "sc-1qpw8k9-3.eFhoug.gtm-expand-full-size-illust")
    url = img.get_attribute("href")
except:
    img = driver.find_element(By.CLASS_NAME, "sc-1qpw8k9-3.eAvtpu")
    url = img.get_attribute("href")
    
headers = {
    'User-Agent' : "user_agent",
    'referer':url
    }

pic = requests.get(url,headers=headers)
timestr = time.strftime("%Y%m%d-%H%M%S")
file = open(f"{timestr}.png", "wb")
file.write(pic.content)
file.close()

driver.quit()