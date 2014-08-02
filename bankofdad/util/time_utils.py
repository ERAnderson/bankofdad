from datetime import timedelta

SATURDAY = 6
SUNDAY = 7


def next_saturday_from_date(date):
    """ Calculate the next saturday after date.
    """
    return next_iso_weekday_from_date(date, SATURDAY)


def next_sunday_from_date(date):
    """ Calculate the next sunday after date.
    """
    return next_iso_weekday_from_date(date, SUNDAY)


def next_iso_weekday_from_date(date, iso_weekday):
    """ Calculate the next saturday after date.
    """
    today_day_of_week = date.isoweekday()
    days_until_iso_weekday = iso_weekday - today_day_of_week
    if days_until_iso_weekday <= 0:
        days_until_iso_weekday += 7
    return date + timedelta(days_until_iso_weekday)


def previous_saturday(today):
    today_day_of_week = today.isoweekday()
    days_since_saturday = SATURDAY - today_day_of_week
    if days_since_saturday == 0:
        days_since_saturday = 7
    return today - timedelta(days_since_saturday)


def previous_sunday(today):
    today_day_of_week = today.isoweekday()
    days_since_sunday = SUNDAY - today_day_of_week
    if days_since_sunday == 0:
        days_since_sunday = 7
    return today - timedelta(days_since_sunday)
