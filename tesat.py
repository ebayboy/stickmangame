import calendar
import datetime

oneday = datetime.timedelta(days=1)
today = datetime.date.today()
m1 = calendar.MONDAY
days = 0
while days < 180:
    if today.weekday() == m1:
        nextMonday = today.strftime('%Y-%m-%d')
        print(nextMonday)
    today += oneday
    days += 1

weight = 82

while weight >= 70:
    print(weight)
    weight -= 1

