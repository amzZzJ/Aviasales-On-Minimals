from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# import pandas as pd
import time
# from dateutil.relativedelta import relativedelta
from datetime import datetime
import re


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
data = []

try:
    driver.get('https://www.aeroflot.ru/ru-ru')
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(((By.NAME, 'ticket-city-arrival-0-booking')))
    )
    city_from = driver.find_element(By.NAME, "ticket-city-departure-0-booking")
    city_from.send_keys(Keys.CONTROL + "a")
    city_from.send_keys(Keys.DELETE)
    time.sleep(1)
    city_from.clear()
    city_from.send_keys("Москва")
    time.sleep(1)
    city_from.send_keys(Keys.DOWN)
    city_from.send_keys(Keys.ENTER)
    city_to = driver.find_element(By.NAME, 'ticket-city-arrival-0-booking')
    city_to.send_keys("Стамбул")
    time.sleep(1)
    city_to.send_keys(Keys.DOWN)
    city_to.send_keys(Keys.ENTER)
    time.sleep(1)
    date_to = driver.find_element(By.NAME, 'ticket-date-from-booking')
    date_to.send_keys(Keys.CONTROL + "a")
    date_to.send_keys(Keys.DELETE)
    time.sleep(1)
    date_to.send_keys("25.11.2024")
    time.sleep(1)
    date_to.send_keys(Keys.ENTER)
    date_from = driver.find_element(By.NAME, "ticket-date-to-booking")
    date_from.send_keys("30.11.2024")
    date_from.send_keys(Keys.ENTER)
    time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR, "#adaptive-sub_0 > div > div > fieldset > div.main-module__row."
                                                  "main-module__search-form__footer.main-module__h-display--flex."
                                                  "main-module__simple > div.main-module__search-form__search-btn."
                                                  "main-module__col--4.main-module__col-tablet--5."
                                                  "main-module__col--stack-below-tablet-vertical > button")
    button.click()
    time.sleep(15)
    to = driver.find_elements(By.CLASS_NAME, 'flight-search')
    # i = 1
    # link_flights = driver.find_element(By.CSS_SELECTOR, f'#frame-0\.8446740044746548 > div:nth-child(2) > div:nth-child({i}) > div.flight-search__inner > div.col--4.col--stack-below-tablet.flight-search__btn')
    # link_flights.click()
    # print(link_flights)
    # time.sleep(15)
finally:
    driver.quit()