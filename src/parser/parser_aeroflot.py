import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from src.instance.flights_db_utils import get_cached_request, save_request_to_cache


def parse_flight_segment(lines, start_index):
    """Парсит информацию об одном сегменте рейса."""
    try:
        price = extract_price(lines).replace("a", "₽")
        # print(price)
        return {
            "Вылет": extract_departure(lines),
            "Прилет": extract_arrival(lines),
            "Перевозчик": "Аэрофлот",
            "Рейс": extract_flight_number(lines),
            "Самолет": lines[start_index + 4] if start_index + 4 < len(lines) else "Информация отсутствует",
            "Цена": price
        }
    except IndexError:
        return None


def extract_departure(lines):
    """Ищет вылет: строка начинается с времени в формате ЧЧ:ММ."""
    for line in lines:
        if re.match(r"^\d{2}:\d{2}", line):  # Строка начинается с ЧЧ:ММ
            return line
    return "Информация отсутствует"

def extract_arrival(lines):
    """Ищет прилет: строка заканчивается временем в формате ЧЧ:ММ."""
    for line in lines:
        if re.search(r"\d{2}:\d{2}$", line):  # Строка заканчивается на ЧЧ:ММ
            return line
    return "Информация отсутствует"


def extract_price(lines):
    """Ищет цену в массиве строк."""
    for line in lines:
        if "от" in line and "a" in line:  # Пример: "от 33 600 Р"
            return line.strip()
    return "Информация отсутствует"

import re

def extract_flight_number(lines):
    """Ищет номер рейса в массиве строк."""
    for line in lines:
        match = re.search(r"\bSU \d+\b", line)  # Пример: SU 1234
        if match:
            return match.group(0)
    return "Информация отсутствует"



def is_valid_time_and_location(line):
    """Проверяет, является ли строка валидным временем и локацией."""
    return bool(re.match(r"^\d{2}:\d{2}[A-Z]{3}", line))


def is_valid_carrier(line):
    """Проверяет, является ли строка валидным названием перевозчика."""
    return bool(line) and len(line.split()) <= 3  # Простая проверка на название перевозчика


def is_valid_flight_number(line):
    """Проверяет, является ли строка валидным номером рейса."""
    return bool(re.match(r"^[A-Z]{2}\s?\d{3,4}$", line))


def is_valid_aircraft(line):
    """Проверяет, является ли строка валидным названием самолёта."""
    return "Boeing" in line or "Airbus" in line or "Sukhoi" in line


def is_valid_price(line):
    """Проверяет, является ли строка валидной ценой."""
    return bool(re.match(r"^от\s\d{1,3}(?:\s?\d{3})*\s[РрAa]$", line))


def parse_ticket(lines):
    """Парсит информацию о билете (с пересадкой или без)."""
    ticket = {}
    segments = []
    seen_segments = set()
    i = 0

    while i < len(lines):
        segment = parse_flight_segment(lines, i)
        if segment:
            # Создаем ключ для проверки уникальности
            segment_key = (
                segment['Вылет'].strip(),
                segment['Прилет'].strip(),
                segment['Перевозчик'].strip(),
                segment['Рейс'].strip(),
                segment['Цена'].strip()
            )
            # Проверяем, что сегмент уникальный
            if segment_key not in seen_segments:
                segments.append(segment)
                seen_segments.add(segment_key)  # Добавляем в множество уникальных сегментов
            else:
                print(f"Дубликат найден: {segment_key}")

            # Переходим к следующему блоку
            i += 5
            if i < len(lines) and "Пересадка" in lines[i]:
                segments[-1]["Пересадка"] = lines[i]
                i += 1
        else:
            break

    # Убираем лишние блоки, если нужно оставить только один
    if len(segments) > 1:
        segments = segments[:1]  # Оставляем только первый блок

    if segments:
        ticket["segments"] = segments

    if i < len(lines):
        ticket["Общее время в пути"] = lines[i]
        if i + 1 < len(lines):
            price_text = lines[i + 1]
            match = re.search(r'\d+', price_text)
            ticket["Цена"] = match.group() if match else "Цена не указана"
        else:
            ticket["Цена"] = "Цена не указана"
        if i + 2 < len(lines):
            ticket["Доступные места"] = lines[i + 2]
        else:
            ticket["Доступные места"] = "Информация о доступных местах отсутствует"

    return ticket


def search_tickets(city_from, city_to, date_from, date_to):
    cached_response = get_cached_request(city_from, city_to, date_from, date_to)
    if cached_response:
        print("Using cached response")
        return json.loads(cached_response)

    """Ищет билеты по заданным параметрам."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    data = []

    try:
        driver.get('https://www.aeroflot.ru/ru-ru')
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(((By.NAME, 'ticket-city-arrival-0-booking')))
        )

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
        search_button = driver.find_element(By.CSS_SELECTOR,
                                            "#adaptive-sub_0 > div > div > fieldset > div.main-module__row."
                                            "main-module__search-form__footer.main-module__h-display--flex."
                                            "main-module__simple > div.main-module__search-form__search-btn."
                                            "main-module__col--4.main-module__col-tablet--5."
                                            "main-module__col--stack-below-tablet-vertical > button")
        search_button.click()

        time.sleep(20)

        flights = driver.find_elements(By.CLASS_NAME, 'flight-search')

        tickets = []
        return_tickets = []
        to_tickets = []
        counter = 0
        seen_flight_texts = set()
        collect_return = False
        for flight in flights:
            flight_text = flight.text
            if flight_text not in seen_flight_texts:
                seen_flight_texts.add(flight_text)
                lines = list(filter(None, map(str.strip, flight_text.split('\n'))))
                if "ЛУЧШАЯ ЦЕНА" in flight_text:
                    if counter == 1:
                        collect_return = True
                        continue
                    else:
                        counter += 1
                        continue
                if lines and collect_return:
                    ticket = parse_ticket(lines)
                    if ticket:
                        return_tickets.append(ticket)
                elif lines and collect_return is False:
                    ticket = parse_ticket(lines)
                    if ticket:
                        to_tickets.append(ticket)

                if to_tickets:
                    tickets.append(to_tickets)
                    tickets.append(return_tickets)

        if tickets:
            save_request_to_cache(city_from, city_to, date_from, date_to, json.dumps(tickets))
            print(tickets)
            return tickets
        else:
            print("Не удалось найти данные о рейсах.")
    except Exception as e:
        print(f"AAAA:")
    finally:
        driver.quit()


