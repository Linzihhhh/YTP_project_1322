from selenium import webdriver
import os

#open the msedgedriver.exe before runing the code
edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--window-size=1920x1080")
edge_options.add_argument("--headless")
edge_driver = os.getcwd() + "\\msedgedriver.exe"
print(edge_driver)
driver = webdriver.Chrome(options=edge_options, executable_path=edge_driver)

url = 'https://www.youtube.com/'
driver.get(url)
