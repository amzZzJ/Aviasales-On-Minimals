import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

def search_tickets(city_from, city_to, date_from, date_to):
    """Ищет билеты по заданным параметрам."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    data = []

    try:
        driver.get('https://www.aeroflot.ru/ru-ru')
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(((By.NAME, 'ticket-city-arrival-0-booking')))
        )

        # Ввод данных
        from_field = driver.find_element(By.NAME, "ticket-city-departure-0-booking")
        from_field.send_keys(Keys.CONTROL + "a")
        from_field.send_keys(Keys.DELETE)
        time.sleep(1)
        from_field.clear()
        from_field.send_keys(city_from)
        time.sleep(1)
        from_field.send_keys(Keys.DOWN)
        from_field.send_keys(Keys.ENTER)

        to_field = driver.find_element(By.NAME, 'ticket-city-arrival-0-booking')
        to_field.send_keys(city_to)
        time.sleep(1)
        to_field.send_keys(Keys.DOWN)
        to_field.send_keys(Keys.ENTER)

        from_date_field = driver.find_element(By.NAME, 'ticket-date-from-booking')
        from_date_field.send_keys(Keys.CONTROL + "a")
        from_date_field.send_keys(Keys.DELETE)
        time.sleep(1)
        from_date_field.send_keys(date_from)
        time.sleep(1)
        from_date_field.send_keys(Keys.ENTER)

        to_date_field = driver.find_element(By.NAME, "ticket-date-to-booking")
        to_date_field.send_keys(date_to)
        to_date_field.send_keys(Keys.ENTER)

        time.sleep(3)
        search_button = driver.find_element(By.CSS_SELECTOR, "#adaptive-sub_0 > div > div > fieldset > div.main-module__row."
                                                             "main-module__search-form__footer.main-module__h-display--flex."
                                                             "main-module__simple > div.main-module__search-form__search-btn."
                                                             "main-module__col--4.main-module__col-tablet--5."
                                                             "main-module__col--stack-below-tablet-vertical > button")
        search_button.click()
        time.sleep(20)

        flights = driver.find_elements(By.CLASS_NAME, 'flight-search')

        tickets = []
        for flight in flights:
            flight_text = flight.text
            lines = list(filter(None, map(str.strip, flight_text.split('\n'))))
            if lines:
                ticket = parse_ticket(lines)
                if ticket:
                    tickets.append(ticket)

        if tickets:
            # print(tickets)
            return tickets
        else:
            print("Не удалось найти данные о рейсах.")
    finally:
        driver.quit()

