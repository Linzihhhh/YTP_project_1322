from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import requests

account = '' #your account
password = '' #your password

#open the website with headless
chrome_options = Options()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)
url = 'https://www.pixiv.net/login.php?ref=wwwtop_accounts_index'
driver.get(url) 

#login
element = driver.find_element(By.CLASS_NAME, "sc-bn9ph6-6.degQSE")
element.send_keys(account)
element = driver.find_element(By.CLASS_NAME, "sc-bn9ph6-6.hfoSmp")
element.send_keys(password)
button = driver.find_element(By.CLASS_NAME, "sc-bdnxRM.jvCTkj.sc-dlnjwi.pKCsX.sc-2o1uwj-7.fguACh.sc-2o1uwj-7.fguACh")
button.click()

#wait until page loaded
WebDriverWait(driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,"sc-9y4be5-1.jtUPOE")))

#find the picture
items = driver.find_elements(By.CLASS_NAME, "sc-d98f2c-0.sc-rp5asc-16.iUsZyY.gtm-toppage-thumbnail-illustration-recommend-works.sc-iJCRrE.hizmCn")
tar = items[0]
for i in items:
    if i.get_attribute("data-gtm-recommend-score") > tar.get_attribute("data-gtm-recommend-score"):
        tar = i
goodpicture_url = tar.get_attribute("href")

#go to target picture
driver.get(goodpicture_url)
WebDriverWait(driver, 30).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "sc-1qpw8k9-1.jOmqKq")))

#find the picture url
url = ''
try:
    img = driver.find_element(By.CLASS_NAME, "sc-1qpw8k9-3.eFhoug.gtm-expand-full-size-illust")
    url = img.get_attribute("href")
except:
    img = driver.find_element(By.CLASS_NAME, "sc-1qpw8k9-3.eAvtpu")
    url = img.get_attribute("href")

#setup the header and request the picture
headers = {
    'User-Agent' : "user_agent",
    'referer':url
}
pic = requests.get(url,headers=headers)

#generate the picture
timestr = time.strftime("%Y%m%d-%H%M%S")
file = open(f"{timestr}.png", "wb")
file.write(pic.content)
file.close()

#close the website
driver.quit()