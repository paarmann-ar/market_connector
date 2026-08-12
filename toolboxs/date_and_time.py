import datetime
import time
from datetime import datetime

# --
# ...
# --


class DateAndTime:
    @staticmethod
    def get_first_day_of_month(format="M/D/Y"):

        try:
            today = datetime.today()

            today_day = "01"
            today_year = str(today.year)
            today_month = str(today.month)

            format = format.replace("D", today_day)
            format = format.replace("M", today_month)
            format = format.replace("Y", today_year)

            return format

        except Exception as exp:
            print(f"get_first_day_of_month: {exp!r}")

    # --
    # ...
    # --

    @staticmethod
    def get_first_day_of_month_1(input_):

        try:
            today = datetime.today()
            return datetime(today.year, today.month, 1)

        except Exception as exp:
            print(repr(exp))

    # --
    # ...
    # --

    @staticmethod
    def get_today(format="%Y-%m-%d"):

        try:
            today = datetime.datetime.today().strftime(format)

            return today

        except Exception as exp:
            print(f"get_today: {exp!r}")

    # --
    # ...
    # --

    @staticmethod
    def get_now(format="%Y-%m-%d %H:%M:%S"):

        try:
            return time.strftime(format, time.gmtime())

        except Exception as exp:
            print(f"get_today: {exp!r}")
