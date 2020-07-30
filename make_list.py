import json
from dayfinder import days_in_month, get_approximation_day

data = {}
for month in range(1, 13):
    data[month] = {}
    for day in range(1, days_in_month[month] + 1):
        approx = get_approximation_day(day, month)
        if approx is not None:
            print(day, month, approx)
            data[month][day] = approx.to_html()

with open("list.json", "w") as f:
    json.dump(data, f)
