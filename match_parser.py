from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import modules
import json
import datetime

start_time = time.time()

# INCOGNITO
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# PREPARE DRIVER
chromedriver = "/users/arturkoszelow/PycharmProjects/score_predict/chromedriver"
driver = webdriver.Chrome(chromedriver, options=option)

try:
    with open('matches.json', 'r') as pre_json_file:
        data = pre_json_file.read()
        matches_data = json.loads(data)

        year = int(matches_data['year'][-1])
        month = int(matches_data['month'][-1])
        day = int(matches_data['day'][-1])
except:

    # PREPARE DICTIONARY
    matches_data = {'year': [],
                    'month': [],
                    'day': [],
                    'country': [],
                    'tournament': [],
                    'host': [],
                    'guest': [],
                    'ht_score': [],
                    'ft_score': [],
                    'broken': []
                    }

    # today = datetime.date.today()
    # year = today.year
    # month = today.month
    # day = today.day
    year = 2019
    month = 2
    day = 10

date = datetime.date(year, month, day)
tdelta = datetime.timedelta(days=1)

while day > 9:

    date = date - tdelta
    year = date.year
    month = date.month
    day = date.day

    driver.get('https://www.betexplorer.com/results/soccer/?year='+str(year)+'&month='+str(month)+'&day='+str(day)+'')

    modules.wait4class(driver, 'table-main__partial')

    try:

        table = driver.find_elements(By.TAG_NAME, 'tbody')
        for tbody in table:

            # tr = sub_table.find_elements(By.TAG_NAME, 'tr')
            # for result in tr:
            #     try:
            #         WebDriverWait(sub_table, 5).until(
            #             EC.visibility_of_all_elements_located((By.CLASS_NAME, 'table-main__result')))
            #     except TimeoutException:
            #         print('no scores')
            #         break

            # COLLECT COUNTRY & TOURNAMENT
            td_tournament = tbody.find_elements(By.CLASS_NAME, 'js-tournament')
            for tournament in td_tournament:
                country = tournament.text.split(': ')[0]
                trnmt = tournament.text.split(': ')[1]

                # tr = tbody.find_elements(By.TAG_NAME, 'tr')
                # for result in tr:
                #     scr = result.find_element(By.CLASS_NAME, 'table-main__result').text
                #     print(len(scr))

                # COLLECT HOST & GUEST
                td_match = tbody.find_elements(By.CLASS_NAME, 'table-main__tt')
                for match in td_match:
                    host = match.text.split(' - ')[0][5:]
                    guest = match.text.split(' - ')[1]

                    matches_data['year'].append(year)
                    matches_data['month'].append(month)
                    matches_data['day'].append(day)
                    matches_data['country'].append(country)
                    matches_data['tournament'].append(trnmt)
                    matches_data['host'].append(host)
                    matches_data['guest'].append(guest)

                # COLLECT SCORES
                td_score = tbody.find_elements(By.CLASS_NAME, 'table-main__partial')
                for score in td_score:
                    if len(score.text) < 10 or len(score.text) > 12:
                        half1_score = 'none'
                        ft_score = 'none'
                        broken = 'none'
                    else:
                        half1_score = score.text.split(',')[0][1:]
                        half2_score = score.text.split(',')[1][:-1]

                        ft_host_score = int(half1_score.split(':')[0]) + int(half2_score.split(':')[0])
                        ft_guest_score = int(half1_score.split(':')[1]) + int(half2_score.split(':')[1])

                        ft_score = str(ft_host_score) + ':' + str(ft_guest_score)

                        # BROKEN OR NO
                        ht_host = int(half1_score.split(':')[0])
                        ht_guest = int(half1_score.split(':')[1])

                        if ht_host > ht_guest and ft_host_score < ft_guest_score \
                                or ht_host < ht_guest and ft_host_score > ft_guest_score:
                            broken = 1
                        else:
                            broken = 0

                    matches_data['broken'].append(broken)
                    matches_data['ht_score'].append(half1_score)
                    matches_data['ft_score'].append(ft_score)

    except:
        pass

    json_matches_data = json.dumps(matches_data)

    with open('matches.json', 'w') as json_file:
        json_file.write(json_matches_data)

    json_file.close()
    print(date)
    print(len(matches_data['year']))
    print(len(matches_data['month']))
    print(len(matches_data['day']))
    print(len(matches_data['country']))
    print(len(matches_data['tournament']))
    print(len(matches_data['host']))
    print(len(matches_data['guest']))
    print(len(matches_data['ht_score']))
    print(len(matches_data['ft_score']))
    print(len(matches_data['broken']))
    print(time.time() - start_time)

driver.close()

