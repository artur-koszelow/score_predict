from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import json

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

chromedriver = "/users/arturkoszelow/PycharmProjects/score_predict/chromedriver"
driver = webdriver.Chrome(chromedriver, chrome_options=option)
driver.get("https://www.wynikinazywo.pl/")

ids = set()
with open('links.json', 'r') as json_file:
    json_list = json_file.read()
    pre_links_list = json.loads(json_list)
    for i in pre_links_list:
        ids.add(i)
print(len(ids))

for _ in range(7):

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

js_list = json.dumps(ids_list)

with open('links_copy.json', 'w') as links:
    links.write(js_list)
    links.close()

print('Thats all')
driver.quit()

