import pytest
from dayfinder import days_in_month, get_approximation_day, monthnames


@pytest.mark.parametrize("day, month, value", [
    (22, 7, u"\u03C0"),
    (19, 7, "e")
])
def test_days(day, month, value):
    approx = get_approximation_day(day, month)
    assert str(approx) == value


@pytest.mark.parametrize("month", range(1, 13))
def test_regularity(month):
    count = 0
    for day in range(1, days_in_month[month] + 1):
        approx = get_approximation_day(day, month)
        if approx is not None:
            print(day, approx)
            count += 1
            assert abs(approx.value - day / month) < 0.1
    print(count, "/", days_in_month[month], "days in",
          monthnames[month], "will have tweets")

    # Assert that at most one day a month doesn't get a tweet
    assert count == days_in_month[month] - 1
