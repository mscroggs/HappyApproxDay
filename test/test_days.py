import pytest
from dayfinder import days_in_month, get_approximation_day


@pytest.mark.parametrize(
    "day, month", [(d, m) for m in range(1, 13)
                   for d in range(days_in_month[m])])
def test_day(day, month):
    approx = get_approximation_day(day, month)
    assert approx is not None
    print(approx)
