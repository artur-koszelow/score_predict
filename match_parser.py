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
    day = 27

old_len = 0
until_date = datetime.date(2011, 12, 31)
today = datetime.date.today()
date = datetime.date(year, month, day)
tdelta = datetime.timedelta(days=1)


while year > 2011:

    date = date - tdelta
    year = date.year
    month = date.month
    day = date.day
    day_time = time.time()

    driver.get('https://www.betexplorer.com/results/soccer/?year='+str(year)+'&month='+str(month)+'&day='+str(day)+'')

    modules.wait4xpath(driver, '//*[@id="nr-all"]/div[2]/div/table/tbody[1]/tr[1]/th[1]/a')

    tbody_len = driver.find_elements(By.TAG_NAME, 'tbody')

    for n_tournament in range(1, (len(tbody_len) - 1)):
        xpath_tournament = '//*[@id="nr-all"]/div[2]/div/table/tbody[' \
                           + str(n_tournament) + ']/tr[1]/th[1]/a'

        try:
            tournament = driver.find_element(By.XPATH, xpath_tournament).text

        except: pass

        for n_partial in range(2, (len(tbody_len) - 1)):
            xpath_partial = '//*[@id="nr-all"]/div[2]/div/table/tbody[' \
                            + str(n_tournament) + ']/tr[' \
                            + str(n_partial) + ']/td[3]'
            xpath_competitors = '//*[@id="nr-all"]/div[2]/div/table/tbody[' \
                                + str(n_tournament) + ']/tr[' \
                                + str(n_partial) + ']/td[1]/a'
            try:
                partial = driver.find_element(By.XPATH, xpath_partial).text
                competitors = driver.find_element(By.XPATH, xpath_competitors).text
            except: break

            if not len(partial) < 10 and len(partial) < 13:
                country = tournament.split(': ')[0]
                #trnmt = tournament.split(': ')[1]
                host = competitors.split(' - ')[0]
                guest = competitors.split(' - ')[1]

                half1_score = partial.split(',')[0][1:]
                half2_score = partial.split(',')[1][:-1]

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

                # print(year, month, day, country, tournament, host, guest, half1_score, ft_score, broken)

                matches_data['year'].append(year)
                matches_data['month'].append(month)
                matches_data['day'].append(day)
                matches_data['country'].append(country)
                matches_data['tournament'].append(tournament)
                matches_data['host'].append(host)
                matches_data['guest'].append(guest)
                matches_data['ht_score'].append(half1_score)
                matches_data['ft_score'].append(ft_score)
                matches_data['broken'].append(broken)

    json_matches_data = json.dumps(matches_data, indent=4)

    with open('matches.json', 'w') as json_file:
        json_file.write(json_matches_data)
    json_file.close()



    # PRINTING INFORMATION
    end_day_time = time.time() - day_time
    end_time = time.time() - start_time
    match_add = (len(matches_data['year']) - old_len)
    days_done = today - date
    days_left = date - until_date

    print(str(days_done).split(',')[0] + '/' + str(days_left).split(',')[0] + ' done / left')
    print('Matches from ' + str(date) + ':')

    # BREAK IF ARRAYS LENGTH IS NOT EQUAL
    for i in matches_data:
        if len(matches_data[i]) == len(matches_data['year']):
            print(str(len(matches_data['year'])) + ' matches')
        else:
            year = 2011

    # BREAK IF NO MATCHES ADDED
    if match_add == 0:
        year = 2011
    else:
        print(str(match_add) + ' new matches')
    print(str(end_day_time / 60) + ' min - this day')
    print(str(end_time / 60) + ' min - whole time')
    print('\n')

    old_len = len(matches_data['year'])

driver.close()

# print(str(len(matches_data['year'])) + ' years')
# print(str(len(matches_data['month'])) + ' months')
# print(str(len(matches_data['day'])) + ' days')
# print(str(len(matches_data['country'])) + ' countries')
# print(str(len(matches_data['tournament'])) + ' tournaments')
# print(str(len(matches_data['host'])) + ' hosts')
# print(str(len(matches_data['guest'])) + ' guests')
# print(str(len(matches_data['ht_score'])) + ' half time scores')
# print(str(len(matches_data['ft_score'])) + ' full time scores')
# print(str(len(matches_data['broken'])) + ' # broken data')



