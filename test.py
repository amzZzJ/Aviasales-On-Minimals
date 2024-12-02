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


data = """06:50SVOC
IST12:25
Аэрофлот
SU 2140
Boeing 737-800
5 ч. 35 мин.
от 15 564 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
08:35SVOC
IST14:10
Аэрофлот
SU 2130
Airbus A320
5 ч. 35 мин.
от 15 564 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
10:05SVOC
IST15:30
Аэрофлот
SU 2136
Airbus A321
5 ч. 25 мин.
от 15 564 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
11:55SVOC
IST17:05
Аэрофлот
SU 2132
Airbus A321
5 ч. 10 мин.
от 15 564 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
18:15SVOC
IST23:30
Аэрофлот
SU 2138
Boeing 737-800
5 ч. 15 мин.
от 15 564 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
00:10SVOC
IST05:30
Аэрофлот
SU 2134
Boeing 737-800
5 ч. 20 мин.
от 17 694 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
09:15SVOB
AER13:10
Аэрофлот
SU 1134
Airbus A321
Пересадка 20 ч. 20 мин.
09:30AER
IST11:45
Россия
SU 6729
Sukhoi SuperJet 100
26 ч. 30 мин.
от 30 416 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
11:05SVOB
AER15:05
Аэрофлот
SU 1150
Boeing 737-800
Пересадка 2 ч. 55 мин.
18:00AER
IST20:15
Россия
SU 6771
Sukhoi SuperJet 100
9 ч. 10 мин.
от 35 236 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
12:10SVOB
AER16:05
Аэрофлот
SU 1124
Airbus A321
Пересадка 1 ч. 55 мин.
18:00AER
IST20:15
Россия
SU 6771
Sukhoi SuperJet 100
8 ч. 5 мин.
от 35 236 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
ВЫЛЕТ
ПРИЛЕТ
ПЕРЕВОЗЧИК
РЕЙС
В ПУТИ
ЛУЧШАЯ ЦЕНА
02:00IST
SVOC06:40
Аэрофлот
SU 2139
Boeing 737-800
4 ч. 40 мин.
от 18 014 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
08:45IST
SVOC13:10
Аэрофлот
SU 2135
Boeing 737-800
4 ч. 25 мин.
от 18 014 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
14:00IST
SVOC18:45
Аэрофлот
SU 2141
Boeing 737-800
4 ч. 45 мин.
от 18 014 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
17:30IST
SVOC22:15
Аэрофлот
SU 2137
Airbus A321
4 ч. 45 мин.
от 18 014 a
Доступно мест по текущей цене: 1
ВЫБРАТЬ РЕЙС
16:30IST
SVOC21:25
Аэрофлот
SU 2131
Airbus A321
4 ч. 55 мин.
от 20 144 a
Доступно мест по текущей цене: 6
ВЫБРАТЬ РЕЙС
19:00IST
SVOC23:45
Аэрофлот
SU 2133
Airbus A321
4 ч. 45 мин.
от 20 144 a
Доступно мест по текущей цене: 6
ВЫБРАТЬ РЕЙС
12:35IST
AER14:30
Россия
SU 6730
Sukhoi SuperJet 100
Пересадка 15 ч. 35 мин.
06:05AER
SVOB09:45
Аэрофлот
SU 1129
Airbus A320
01 декабря 2024 г. 
21 ч. 10 мин.
от 43 361 a
Доступно мест по текущей цене: 2
ВЫБРАТЬ РЕЙС
21:25IST
AER23:00
Россия
SU 6772
Sukhoi SuperJet 100
Пересадка 2 ч. 30 мин.
01:30AER
SVOB05:05
Аэрофлот
SU 1133
Airbus A320
01 декабря 2024 г. 
7 ч. 40 мин.
от 49 881 a
ВЫБРАТЬ РЕЙС
12:35IST
AER14:30
Россия
SU 6730
Sukhoi SuperJet 100
Пересадка 27 ч. 50 мин.
18:20AER
SVOB22:20
Россия
SU 6718
Boeing 747-400
01 декабря 2024 г. 
33 ч. 45 мин.
от 59 131 a
Доступно мест по текущей цене: 4
ВЫБРАТЬ РЕЙС
12:35IST
AER14:30
Россия
SU 6730
Sukhoi SuperJet 100
Пересадка 2 ч. 35 мин.
17:05AER
SVOB20:45
Аэрофлот
SU 1125
Airbus A321
8 ч. 10 мин.
от 66 371 a
Доступно мест по текущей цене: 2
ВЫБРАТЬ РЕЙС
12:35IST
AER14:30
Россия
SU 6730
Sukhoi SuperJet 100
Пересадка 3 ч. 25 мин.
17:55AER
SVOB21:35
Аэрофлот
SU 1611
Airbus A321
9 ч.
от 76 611 a
Доступно мест по текущей цене: 3
ВЫБРАТЬ РЕЙС
12:35IST
AER14:30
Россия
SU 6730
Sukhoi SuperJet 100
Пересадка 1 ч. 35 мин.
16:05AER
SVOB19:40
Аэрофлот
SU 1151
Boeing 737-800
7 ч. 5 мин.
Билетов класса Эконом нет в наличии
Другие классы
«Бизнес Базовый»от 101 616 a"""

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

print("Данные успешно сохранены в tickets.json")
