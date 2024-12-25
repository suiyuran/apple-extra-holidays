from calendar import monthcalendar
from datetime import datetime
from uuid import UUID
from uuid import uuid3

from icalendar import Calendar
from icalendar import Event


NAMESPACE_HOLIDAY = UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

HOLIDAYS = {
    "情人节": [2, 14],
    "植树节": [3, 12],
    "愚人节": [4, 1],
    "母亲节": [5, (2, 7)],
    "父亲节": [6, (3, 7)],
    "教师节": [9, 10],
    "万圣节": [10, 31],
    "感恩节": [11, (4, 4)],
    "平安夜": [12, 24],
    "圣诞节": [12, 25],
}


def create_calendar():
    calender = Calendar()
    calender.add("VERSION", "2.0")
    calender.add("PRODID", "icalendar-python")
    calender.add("CALSCALE", "GREGORIAN")
    calender.add("X-WR-CALNAME", "中国大陆节假日补充")
    calender.add("X-APPLE-LANGUAGE", "zh")
    calender.add("X-APPLE-REGION", "CN")
    return calender


def create_event(summary: str, dtstart: str):
    event = Event()
    event.add("DTSTAMP;VALUE=DATE", "19760401")
    event.add("UID", uuid3(NAMESPACE_HOLIDAY, dtstart))
    event.add("DTSTART;VALUE=DATE", dtstart)
    event.add("CLASS", "PUBLIC")
    event.add("SUMMARY;LANGUAGE=zh-CN", summary)
    event.add("TRANSP", "TRANSPARENT")
    event.add("CATEGORIES", "節慶")
    event.add("X-APPLE-UNIVERSAL-ID", uuid3(NAMESPACE_HOLIDAY, summary))
    return event


def create_date(year: int, month: int, day: int | tuple[int, int]):
    if isinstance(day, tuple):
        month_cal = monthcalendar(year, month)
        first_day = month_cal[0][day[1] - 1]
        day = first_day + 7 * (day[0] - 1 if first_day else day[0])
    return datetime(year, month, day).strftime("%Y%m%d")


def create_holidays(year: int):
    holidays = []
    for key in HOLIDAYS.keys():
        month, day = HOLIDAYS[key]
        holidays.append(create_event(key, create_date(year, month, day)))
    return holidays


def main():
    year = datetime.now().year
    calender = create_calendar()
    holidays = sum(map(create_holidays, [year, year + 1]), [])

    for holiday in holidays:
        calender.add_component(holiday)

    with open("cn_zh.ics", "w", encoding="utf-8") as file:
        file.write(calender.to_ical(sorted=False).decode("utf-8"))


if __name__ == "__main__":
    main()
