from constants import get_constants
from random import shuffle

days_in_month = {9: 30, 4: 30, 6: 30, 11: 30,
                 1: 31, 3: 31, 5: 31, 7: 31, 8: 31, 10: 31, 12: 31,
                 2: 29}
monthnames = {1: "January", 2: "February", 3: "March", 4: "April",
              5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}


def get_approximation_day(day, month):
    for i in range(3):
        constants = get_constants(day / month, i)
        shuffle(constants)
        for c in constants:
            if is_closest(c, day, month):
                return c


def is_closest(c, day, month):
    for m, days in days_in_month.items():
        for d in range(1, days + 1):
            if m != month or d != day:
                if c.error(d / m) < c.error(day / month):
                    return False
    return True
