import datetime


def parse_datetime(datetime_raw: int):
    print(datetime.datetime.fromtimestamp((datetime_raw + 3600) // 1000))
