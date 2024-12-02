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
import json


class Ticket:
    def __init__(self, departure_time, arrival_time, departure_city, arrival_city, duration, price, seats):
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.duration = duration
        self.price = price
        self.seats = seats

    def __str__(self):
        return (f"{self.departure_time}{self.departure_city}\n"
                f"{self.arrival_time}{self.arrival_city}\n"
                f"{self.duration}\n"
                f"от {self.price}\n"
                f"Доступно мест по текущей цене: {self.seats}")


def parse_flight_segment(lines, start_index):
    """Парсит информацию об одном сегменте рейса."""
    try:
        return {
            "Вылет": lines[start_index],
            "Прилет": lines[start_index + 1],
            "Перевозчик": lines[start_index + 2],
            "Рейс": lines[start_index + 3],
            "Самолет": lines[start_index + 4]
        }
    except IndexError:
        return None


def parse_ticket(lines):
    """Парсит информацию о билете (с пересадкой или без)."""
    ticket = {}
    segments = []
    i = 0
    while i < len(lines):
        segment = parse_flight_segment(lines, i)
        if segment:
            segments.append(segment)
            i += 5
            if i < len(lines) and "Пересадка" in lines[i]:
                segments[-1]["Пересадка"] = lines[i]
                i += 1
        else:
            break

    if segments:
      ticket["segments"] = segments

    if len(lines) > i:
        ticket["Общее время в пути"] = lines[i]
        ticket["Цена"] = lines[i+1]
        ticket["Доступные места"] = lines[i+2] if len(lines) > i + 2 else None

    return ticket


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
    date_to.send_keys("03.12.2024")
    time.sleep(1)
    date_to.send_keys(Keys.ENTER)
    date_from = driver.find_element(By.NAME, "ticket-date-to-booking")
    date_from.send_keys("17.12.2024")
    date_from.send_keys(Keys.ENTER)
    time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR, "#adaptive-sub_0 > div > div > fieldset > div.main-module__row."
                                                  "main-module__search-form__footer.main-module__h-display--flex."
                                                  "main-module__simple > div.main-module__search-form__search-btn."
                                                  "main-module__col--4.main-module__col-tablet--5."
                                                  "main-module__col--stack-below-tablet-vertical > button")
    button.click()
    time.sleep(20)
    flights = driver.find_elements(By.CLASS_NAME, 'flight-search')
    # i = 1
    # link_flights = driver.find_element(By.CSS_SELECTOR, f'#frame-0\.8446740044746548 > div:nth-child(2) > div:nth-child({i}) > div.flight-search__inner > div.col--4.col--stack-below-tablet.flight-search__btn')
    # link_flights.click()
    # print(link_flights)
    # time.sleep(15)
    for i in flights:
        print(i.text)
    '''
    flights = re.split(r'ВЫБРАТЬ РЕЙС', data)
    tickets = []
    for flight in flights:
        lines = list(filter(None, map(str.strip, flight.split('\n'))))
        if lines:
            ticket = parse_ticket(lines)
            if ticket:
                tickets.append(ticket)

    # Сохранение в JSON
    with open('tickets_with_transfers.json', 'w', encoding='utf-8') as f:
        json.dump(tickets, f, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в tickets.json")'''
finally:
    driver.quit()
    