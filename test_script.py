from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# INCOGNITO
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

#PREPARE DRIVER
chromedriver = "/users/arturkoszelow/PycharmProjects/score_predict/chromedriver"
# driver = webdriver.Chrome(chromedriver, chrome_options=option)
match_driver = webdriver.Chrome(chromedriver, chrome_options=option)

red_cards = {'Host reds': 0, 'Guest reds': 0}

match_driver.get('https://www.wynikinazywo.pl/mecz/lUpMaju6/#szczegoly-meczu')
host_red_cards = match_driver.find_elements(By.CLASS_NAME, 'fl')

H2H = match_driver.find_element(By.XPATH, '//*[@id="a-match-head-2-head"]').click()
try:
    button = WebDriverWait(match_driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'show_more')))

except TimeoutException:
    print('Button load too long or match cancelled')
    pass
together = match_driver.find_element(By.XPATH, '//*[@id="tab-h2h-overall"]/div[3]/table')
date = together.find_elements(By.TAG_NAME, 'tr')
for year in date:
    year1 = year.get_attribute('onclick')
    print(year1)
# for reds in host_red_cards:
#     redsl = reds.find_elements(By.CLASS_NAME, 'r-card')
#     if not len(redsl) == 0:
#         red_cards['Host reds'] = int((len(redsl)/2))
#     yredsl = reds.find_elements(By.CLASS_NAME, 'yr-card')
#     if not len(yredsl) == 0:
#         red_cards['Host reds'] = int((len(yredsl) / 2))
#
# guest_red_cards = match_driver.find_elements(By.CLASS_NAME, 'fr')
# for reds in guest_red_cards:
#     redsp = reds.find_elements(By.CLASS_NAME, 'r-card')
#     if not len(redsp) == 0:
#         red_cards['Guest reds'] = int((len(redsp)/2))
#     yredsr = reds.find_elements(By.CLASS_NAME, 'yr-card')
#     if not len(yredsr) == 0:
#         red_cards['Host reds'] = int((len(yredsr) / 2))

# print(red_cards)
match_driver.close()
