from bs4 import BeautifulSoup
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

chromedriver = "/users/arturkoszelow/PycharmProjects/lamacz/chromedriver"
driver = webdriver.Chrome(chromedriver, chrome_options=option)
driver.get("https://www.wynikinazywo.pl/")

ids = set()
with open('links_copy.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for i in csv_reader:
        ids.update(i)

print(len(ids))

for _ in range(5):

    dzien = driver.find_element_by_xpath('//*[@id="ifmenu-calendar"]/span[1]')
    dzien.click()

    try:
        button = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'tr')))
    except TimeoutException:
        print('Page load too long')
        driver.quit()

    rows = driver.find_elements_by_tag_name('tr')

    for id in rows:
        m = id.get_attribute('id')
        if not m == '':
            m = m[4:]
            ids.add(m)

    print(ids)
    print(len(ids))

ids_list = list(ids)
with open('links.csv', 'w', newline='') as links:
    writer = csv.writer(links)
    for i in range(len(ids_list)):
        writer.writerow([ids_list[i]])
    links.close()

print('Thats all')
driver.quit()

'''
comment
'''