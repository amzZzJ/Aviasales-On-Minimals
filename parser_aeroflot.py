import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Вспомогательные функции для обработки текста
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

    if i < len(lines):
        ticket["Общее время в пути"] = lines[i]
        if i + 1 < len(lines):
            ticket["Цена"] = lines[i + 1]
        else:
            ticket["Цена"] = "Цена не указана"
        if i + 2 < len(lines):
            ticket["Доступные места"] = lines[i + 2]
        else:
            ticket["Доступные места"] = "Информация о доступных местах отсутствует"

    return ticket



# Настройка Selenium
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

    # Обработка данных
    tickets = []
    for flight in flights:
        flight_text = flight.text
        lines = list(filter(None, map(str.strip, flight_text.split('\n'))))
        if lines:
            ticket = parse_ticket(lines)
            if ticket:
                tickets.append(ticket)

    # Сохранение данных в JSON
    if tickets:
        with open('tickets_with_transfers.json', 'w', encoding='utf-8') as f:
            json.dump(tickets, f, ensure_ascii=False, indent=4)

        print("Данные успешно сохранены в tickets_with_transfers.json")
    else:
        print("Не удалось найти данные о рейсах.")
finally:
    driver.quit()
