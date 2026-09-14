import datetime


def query_from_date():
    while True:
        qDate = str(input('Please entry the date entry created(YYYY-MM-DD):'))
        try:
            d = datetime.date.fromisoformat(qDate)
            print(d)
            print(type(d))
            e = d + datetime.timedelta(days=1)
            print(e)
            break
        except ValueError:
            print('Please enter in correct date format!')


query_from_date()