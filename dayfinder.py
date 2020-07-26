from constants import get_constants

days_in_month = {9: 30, 4: 30, 6: 30, 11: 30,
                 1: 31, 3: 31, 5: 31, 7: 31, 8: 31, 10: 31, 12: 31,
                 2: 29}


def get_approximation_day(day, month):
    for c in get_constants(day // month):
        if c.error(day / month) < 0.01:
            if is_closest(c, day, month):
                return c


def is_closest(c, day, month):
    for m, days in days_in_month:
        for d in range(days):
            if m != month or d != day:
                if c.error(d / m) < c.error(day / month):
                    return False
    return True
