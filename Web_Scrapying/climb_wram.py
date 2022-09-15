import requests
from bs4 import BeautifulSoup
import os
import sys
import time

res = requests.get("https://www.pixiv.net/")
soup = BeautifulSoup(res.text,"html.parser")


timestr = time.strftime("%Y%m%d-%H%M%S")
with open(f"{timestr}.html", "wb") as file:
    file.write(soup.prettify("utf-8"))
