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

count = 0
ids = set()
ids_new = set()
with open('links_copy.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for i in csv_reader:
        ids.update(i)

print(len(ids))
for id in ids:
    count += 1
    print(id, count)
    driver.get("https://www.wynikinazywo.pl/mecz/" + str(id) + "/#h2h;overall")


    try:
        button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'show_more')))
    except TimeoutException:
        print('Page show more, load too long')
        # driver.quit()
        pass

    try:
        while True:
            more = driver.find_element_by_css_selector('#tab-h2h-overall > div:nth-child(2) > table > tbody > tr.hid > td > a')
            more.click()
    except:
        # print('no more buttons1')
        pass

    try:
        while True:
            more = driver.find_element_by_css_selector('#tab-h2h-overall > div:nth-child(1) > table > tbody > tr.hid > td > a')
            more.click()
    except:
        # print('no more buttons2')
        pass

    try:
        while True:
            more = driver.find_element_by_css_selector('#tab-h2h-overall > div:nth-child(3) > table > tbody > tr.hid > td > a')
            more.click()
    except:
        # print('no more buttons3')
        pass

    for t in range(1,4):
        for i in range(1,1000):
            xpath = '//*[@id="tab-h2h-overall"]/div[' + str(t) + ']/table/tbody/tr[' + str(i) + ']'
            try:
                button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, str(xpath))))
                rows = driver.find_element_by_xpath(str(xpath))
                m = rows.get_attribute('onclick')
                if m == None:
                    break
                year = m[43:47]
                if int(year) >= 2012:
                    m = m[17:25]
                    ids_new.add(m)
                else:
                    pass
            except TimeoutException:
                # print(xpath)
                print('Collected ids ' + str(len(ids_new)))
                break

ids_list = list(ids_new)
with open('links_new.csv', 'w', newline='') as links_new:
    writer = csv.writer(links_new)
    for i in range(len(ids_list)):
        writer.writerow([ids_list[i]])
    links_new.close()

driver.quit()

'''
sprawdz mecz QeqfZUHt <- nie ma wspólnych meczy bo został odwołany
ogarnąć m na takie wypadki...
'''