from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PATH = "\\Users\\User\\Documents\\Junior\\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://search.rice.edu")

search = driver.find_element_by_id("q")
driver.execute_script("window.open('http://google.com', 'new_window')")

search.send_keys("Colin") # type in name
search.send_keys(Keys.RETURN) # hit the enter button and search
time.sleep(3)