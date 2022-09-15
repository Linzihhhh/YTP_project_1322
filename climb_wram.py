import requests
from bs4 import BeautifulSoup

res = requests.get("https://hackmd.io/gaROpPThTyC2vGDfJlEUOA")
soup = BeautifulSoup(res.text,"html.parser")

print(soup.prettify())