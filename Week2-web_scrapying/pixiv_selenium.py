from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import time,random,requests,os,dotenv

#loading .env
dotenv.load_dotenv()
ACCOUNT = os.getenv("ACCOUNT")
PASSWORD = os.getenv("PASSWORD")

#the class names on pixiv
classname = {
    "account":"sc-bn9ph6-6.degQSE",
    "password":"sc-bn9ph6-6.hfoSmp",
    "login":"sc-bdnxRM.jvCTkj.sc-dlnjwi.pKCsX.sc-2o1uwj-7.fguACh.sc-2o1uwj-7.fguACh",
    "recommend_pic":"sc-d98f2c-0.sc-rp5asc-16.iUsZyY.gtm-toppage-thumbnail-illustration-recommend-works.sc-iJCRrE.hizmCn",
    "picture_div":"sc-1qpw8k9-1.jOmqKq",
    "one_picture":"sc-1qpw8k9-3.eFhoug.gtm-expand-full-size-illust",
    "pictures":"sc-1qpw8k9-3.eAvtpu"
}

#open the website with headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)
url = 'https://www.pixiv.net/login.php?ref=wwwtop_accounts_index'
driver.get(url)

#login
element = driver.find_element(By.CLASS_NAME, classname["account"])
element.send_keys(ACCOUNT)
element = driver.find_element(By.CLASS_NAME, classname["password"])
element.send_keys(PASSWORD)
button = driver.find_element(By.CLASS_NAME, classname["login"])
button.click()

#wait until page loaded
WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME,classname["recommend_pic"])))

#find the picture
pictures = driver.find_elements(By.CLASS_NAME, classname["recommend_pic"])
target = pictures[0]
for i in pictures:
    if i.get_attribute("data-gtm-recommend-score") > target.get_attribute("data-gtm-recommend-score"):
        if random.randint(1,100) > 30:
            target = i
picture_url = target.get_attribute("href")

#go to target picture
driver.get(picture_url)
WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, classname["picture_div"])))

#find the picture url
url = ''
try:
    img = driver.find_element(By.CLASS_NAME, classname["one_picture"])
    url = img.get_attribute("href")
except:
    img = driver.find_element(By.CLASS_NAME, classname["pictures"])
    url = img.get_attribute("href")

#setup the header and request the picture
headers = {
    'User-Agent' : "user_agent",
    'referer':url
}
image = requests.get(url,headers=headers)

#generate the picture
timestr = time.strftime("%Y%m%d-%H%M%S")
with open(f"{timestr}.png", "wb") as file:
    file.write(image.content)

#close the website
driver.quit()