from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# INCOGNITO
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

#PREPARE DRIVER
chromedriver = "/users/arturkoszelow/PycharmProjects/score_predict/chromedriver"
driver = webdriver.Chrome(chromedriver, chrome_options=option)

then = time.time()
count = 0
links_dome = set()
new_links = set()
pre_links = {'4AKMDdCj', 'SjbfGrft', 'fJmhNh17', '67CTSQzJ', 'QeqfZUHt', '0OpJYNSe', '6uj583x2', 'YuqpDimq'}

while len(pre_links) > 1:

    for link_x in pre_links:
        links_dome.update([link_x])
        driver.get("https://www.wynikinazywo.pl/mecz/" + str(link_x) + "/#h2h;overall")

        try:
            button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'show_more')))
            score = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#event_detail_current_result > span:nth-child(2) > span.scoreboard')))

            # COLLECTING LINKS IDS
            # links_ids = driver.find_elements(By.TAG_NAME, 'tr')
            # for tr in links_ids:
            #     row = tr.get_attribute('onclick')
            #     if row == None:
            #         pass
            #     else:
            #         year = row[43:47]
            #         if int(year) >= 2012:
            #             link_id = row[17:25]
            #             # print(link_id, year)
            #             new_links.update([link_id])
            #         else:
            #             pass

            # COLLECTING TEAMS
            host = driver.find_element(By.CSS_SELECTOR, '#flashscore_column > table > tbody > tr:nth-child(1) > td.tname-home.logo-enable > span > a')
            guest = driver.find_element(By.CSS_SELECTOR, '#flashscore_column > table > tbody > tr:nth-child(1) > td.tname-away.logo-enable > span > a')
            host = host.get_attribute('onclick').split('/')[2]
            guest = guest.get_attribute('onclick').split('/')[2]

            # COLLECTING DATE
            date = driver.find_element(By.CLASS_NAME, 'mstat-date')
            date = date.text.split('.')[1]

            # COLLECTING SCORE
            score_host = driver.find_element(By.CSS_SELECTOR, '#event_detail_current_result > span.scoreboard')
            score_guest = driver.find_element(By.CSS_SELECTOR, '#event_detail_current_result > span:nth-child(2) > span.scoreboard')
            score_host = score_host.text
            score_guest = score_guest.text

            # PLAYED TOGETHER > 2012
            pt = driver.find_element(By.XPATH, '//*[@id="tab-h2h-overall"]/div[3]/table/tbody')
            pt = pt.find_elements(By.TAG_NAME, 'tr')

            print(date, host,':',guest, score_host,'-', score_guest, pt)

        except TimeoutException:
            print('Button load too long or match cancelled')
            pass

        count += 1
        now = time.time()
        # print('new links', str(len(new_links)), now-then, 'sec', count)


    pre_links = new_links.difference(links_dome)
    print('pre links', str(len(pre_links)))

driver.close()
