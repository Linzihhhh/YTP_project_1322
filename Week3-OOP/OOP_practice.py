import os, dotenv

# load .env
dotenv.load_dotenv()
ACCOUNT = os.getenv("ACCOUNT")
PASSWORD = os.getenv("PASSWORD")

import random, time
import enum

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

import requests

class PixivClassName(enum.Enum):
    """A collection of classnames on Pixiv"""

    ACCOUNT = "sc-bn9ph6-6.degQSE"
    PASSWORD = "sc-bn9ph6-6.hfoSmp"
    LOGIN = "sc-bdnxRM.jvCTkj.sc-dlnjwi.pKCsX.sc-2o1uwj-7.fguACh.sc-2o1uwj-7.fguACh"
    RECOMMENDED_PICTURE = "sc-d98f2c-0.sc-rp5asc-16.iUsZyY.gtm-toppage-thumbnail-illustration-recommend-works.sc-iJCRrE.hizmCn"
    PICTURE_DIV = "sc-1qpw8k9-1.jOmqKq"
    ONE_PICTURE = "sc-1qpw8k9-3.eFhoug.gtm-expand-full-size-illust"
    PICTURES = "sc-1qpw8k9-3.eAvtpu"


class PixivWebScraper:
    """A Web Scraper inplemented by Selenium"""

    def __init__(self): # open the website with headless
        chrome_options = Options()
        chrome_options.add_argument('--headless') 
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chrome_options)

    def login(self, account: str, password: str) -> None:
        url = 'https://www.pixiv.net/login.php?ref=wwwtop_accounts_index'
        self.driver.get(url)
        element = self.driver.find_element(By.CLASS_NAME, PixivClassName.ACCOUNT)
        element.send_keys(account)
        element = self.driver.find_element(By.CLASS_NAME, PixivClassName.PASSWORD)
        element.send_keys(password)
        button = self.driver.find_element(By.CLASS_NAME, PixivClassName.LOGIN)
        button.click()

    def get_recommended_picture_raw_url(self):
        # wait until the page loaded
        WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, PixivClassName.RECOMMENDED_PICTURE)))

        # find the post url
        pictures = self.driver.find_elements(By.CLASS_NAME, PixivClassName.RECOMMENDED_PICTURE)
        target = pictures[0]
        for picture in pictures:
            if picture.get_attribute("data-gtm-recommend-score") > target.get_attribute("data-gtm-recommend-score"):
                if random.randint(1, 100) > 30:
                    target = picture
        post_url = target.get_attribute("href")
        return self.get_picture_raw_url(post_url)
        
    def get_picture_raw_url(self, url: str) -> str:
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, PixivClassName.PICTURE_DIV)))
        
        try:
            img = self.driver.find_element(By.CLASS_NAME, PixivClassName.ONE_PICTURE)
            return img.get_attribute("href")
        except:
            img = self.driver.find_element(By.CLASS_NAME, PixivClassName.PICTURES)
            return img.get_attribute("href")

    def download(self, url: str) -> None:
        # setup the header
        headers = {
            'User-Agent' : "user_agent",
            'referer': url
        }
        image = requests.get(url, headers=headers)

        # generate the picture
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(f"{timestr}.png", "wb") as file:
            file.write(image.content)

    def close(self):
        # close the broswer
        self.driver.quit()


pixiv_scraper = PixivWebScraper()
pixiv_scraper.login(ACCOUNT, PASSWORD)
raw_url = pixiv_scraper.get_recommended_picture_raw_url()
pixiv_scraper.download(raw_url)
pixiv_scraper.close()