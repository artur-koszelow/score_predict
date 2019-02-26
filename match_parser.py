from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import modules

# INCOGNITO
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

#PREPARE DRIVER
chromedriver = "/users/arturkoszelow/PycharmProjects/score_predict/chromedriver"
driver = webdriver.Chrome(chromedriver, chrome_options=option)
driver.get('https://www.betexplorer.com/results/soccer/?year=2019&month=02&day=24')

modules.wait4tag(driver, 'tbody')

try:
    tr = driver.find_elements(By.TAG_NAME, 'tr')
    for sub_tr in tr:
        tournament = sub_tr.find_element(By.CLASS_NAME, 'table-main__tournament').text
        # print(tournament)
        for competitors in tr:
            competitors = competitors.find_elements(By.CLASS_NAME, 'table-main__tt')
            for comps in competitors:
                print(tournament, comps.text[5:])
except:
    pass

driver.close()
