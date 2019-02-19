from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def wait_for_all_elements_located_by_tag_name(driver: vars(), time: int, tag_name: str):
    try:
        WebDriverWait(driver, time).until(EC.visibility_of_all_elements_located((By.TAG_NAME, tag_name)))
    except TimeoutException:
        print('wait_for_all_elements_located_by_tag_name wait too long')
        pass

