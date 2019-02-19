from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import modules

# INCOGNITO
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

#PREPARE DRIVER
chromedriver = "/users/arturkoszelow/PycharmProjects/score_predict/chromedriver"
driver = webdriver.Chrome(chromedriver, chrome_options=option)
match_driver = webdriver.Chrome(chromedriver, chrome_options=option)

driver.get('https://www.wynikinazywo.pl/')

ids = []

modules.wait_for_all_elements_located_by_tag_name(driver=driver, time=5, tag_name='tr')

get_ids = driver.find_elements(By.TAG_NAME, 'tr')

for td in get_ids:
    id = td.get_attribute('id')
    if not id == '':
        ids.append(id)

for id in ids:
    match_status = driver.find_element(By.XPATH, '//*[@id="' + str(id) + '"] / td[2] / span').text

    if match_status == 'Koniec':
        ht_score = driver.find_element(By.XPATH, '//*[@id="' + str(id) + '"]/td[4]').text.split('-')
        score_host = int(ht_score[0])
        score_guest = int(ht_score[1])

        if score_host != score_guest:
            idx = id[4:]
            match_driver.get('https://www.wynikinazywo.pl/mecz/' + str(idx) + '/#szczegoly-meczu')

            try:
                button = WebDriverWait(match_driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="detcon"]/table/thead/tr/th/div/div/span[2]')))

                # COUNTRY & LEAGUE
                country_league = match_driver.find_element(By.XPATH, '//*[@id="detcon"]/table/thead/tr/th/div/div/span[2]').text
                # country_league_text = country_league.text
                host = match_driver.find_element(By.XPATH, '//*[@id="flashscore_column"]/table/tbody/tr[1]/td[1]/span/a').text
                guest = match_driver.find_element(By.XPATH, '//*[@id="flashscore_column"]/table/tbody/tr[1]/td[3]/span/a').text
                print(match_status)
                print(country_league)
                print(host, score_host, '-', score_guest, guest)


                # HOST RED CARDS
                host_red_cards = match_driver.find_elements(By.CLASS_NAME, 'fl')
                red_cards = {'Host reds': 0, 'Guest reds': 0}
                for reds in host_red_cards:
                    redsl = reds.find_elements(By.CLASS_NAME, 'r-card')
                    if not len(redsl) == 0:
                        red_cards['Host reds'] = int((len(redsl) / 2))
                    yredsl = reds.find_elements(By.CLASS_NAME, 'yr-card')
                    if not len(yredsl) == 0:
                        red_cards['Host reds'] += int((len(yredsl) / 2))


                # GUEST RED CARDS
                guest_red_cards = match_driver.find_elements(By.CLASS_NAME, 'fr')
                for reds in guest_red_cards:
                    redsr = reds.find_elements(By.CLASS_NAME, 'r-card')
                    if not len(redsr) == 0:
                        red_cards['Guest reds'] = int((len(redsr) / 2))
                    yredsr = reds.find_elements(By.CLASS_NAME, 'yr-card')
                    if not len(yredsr) == 0:
                        red_cards['Guest reds'] += int((len(yredsr) / 2))

                # SUMMARY OF RED CARDS
                if score_host > score_guest:
                    red_summary = red_cards['Host reds'] - red_cards['Guest reds']
                else:
                    red_summary = red_cards['Guest reds'] - red_cards['Host reds']

                print(red_cards, '(', red_summary, ')')

                # ODDS
                button = match_driver.find_element(By.XPATH, '//*[@id="odds-tab-prematch"]/span/a').click()
                pre_odds_1 = match_driver.find_element(By.XPATH, '//*[@id="default-odds"]/tbody/tr/td[2]/span/span[2]/span').text
                pre_odds_x = match_driver.find_element(By.XPATH, '//*[@id="default-odds"]/tbody/tr/td[3]/span/span[2]/span').text
                pre_odds_2 = match_driver.find_element(By.XPATH, '//*[@id="default-odds"]/tbody/tr/td[4]/span/span[2]/span').text

                print(float(pre_odds_1), float(pre_odds_x), float(pre_odds_2))

                try:
                    live_odds_1 = match_driver.find_element(By.XPATH, '//*[@id="default-live-odds"]/tbody/tr/td[2]/span/span[2]/span').text
                    live_odds_x = match_driver.find_element(By.XPATH, '//*[@id="default-live-odds"]/tbody/tr/td[3]/span/span[2]/span').text
                    live_odds_2 = match_driver.find_element(By.XPATH, '//*[@id="default-live-odds"]/tbody/tr/td[4]/span/span[2]/span').text

                    print(float(live_odds_1), float(live_odds_x), float(live_odds_2))
                    print((float(live_odds_1) - float(pre_odds_1),
                           (float(live_odds_x) - float(pre_odds_x)),
                           (float(live_odds_2) - float(pre_odds_2))))

                except:
                    print('Match without live bet')

                # PLAYED TOGETHER
                # H2H = match_driver.find_element(By.XPATH, '//*[@id="a-match-head-2-head"]').click()
                # together = match_driver.find_element(By.XPATH, '//*[@id="tab-h2h-overall"]/div[3]/table')
                # together.find_elements(By.TAG_NAME, 'tr')


                print('\n')

            except TimeoutException:
                print('Button load too long or match cancelled')
                pass

driver.close()
match_driver.close()



