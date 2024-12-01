from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from setup import utils

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://newblog.gameappszone.com/")

sleep(3)

driver.find_element(
    By.CSS_SELECTOR, ".d-flex .cusBtnOption:nth-of-type(1)").click()

sleep(3)
