from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def wait4tags(driver, tags_name: str):
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, tags_name)))
    except TimeoutException:
        print('tags {} load too long'.format(tags_name))
        pass


def wait4tag(driver, tag_name: str):
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, tag_name)))
    except TimeoutException:
        print('tags {} load too long'.format(tag_name))
        pass


def wait4xpath(driver, xpath: str):
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print('xpath {} load too long'.format(xpath))
        pass
