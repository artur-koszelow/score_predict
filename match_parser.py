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
pre_links = {'4AKMDdCj', 'SjbfGrft', 'fJmhNh17', '67CTSQzJ', 'QeqfZUHt'}
while len(pre_links) > 1:

    for link_x in pre_links:
        driver.get("https://www.wynikinazywo.pl/mecz/" + str(link_x) + "/#h2h;overall")
        try:
            button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'show_more')))

            rows = driver.find_elements(By.TAG_NAME, 'tr')
            for tr in rows:
                row = tr.get_attribute('onclick')
                if row == None:
                    pass
                else:
                    year = row[43:47]
                    if int(year) >= 2012:
                        link_id = row[17:25]
                        # print(link_id, year)
                        new_links.update([link_id])
                    else:
                        pass
        except TimeoutException:
            print('Button load too long')
            break

        count += 1
        now = time.time()
        print('new links', str(len(new_links)), now-then, 'sec', count)
        links_dome.update([link_x])

    pre_links.update(new_links)
    print('pre links', str(len(pre_links)))

driver.close()