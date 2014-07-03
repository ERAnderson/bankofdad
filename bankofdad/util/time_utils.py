from datetime import date, timedelta

def previous_saturday(today):
    today_day_of_week = today.isoweekday()
    days_since_saturday = 6 - today_day_of_week
    if days_since_saturday == 0:
        days_since_saturday = 7
    return today - timedelta(days_since_saturday)

def previous_sunday(today):
    today_day_of_week = today.isoweekday()
    days_since_sunday = 7 - today_day_of_week
    if days_since_sunday == 0:
        days_since_sunday = 7
    return today - timedelta(days_since_sunday)
