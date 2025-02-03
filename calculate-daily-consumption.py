import argparse
import pandas as pd
import calendar
import datetime
from os.path import isfile


def calculate_percentage(csv_consumption_data_file: str | None = None,
                         time_col_name: str = "time",
                         power_col_name: str = "power",
                         seperator: str = ",",
                         decimal_sign: str = ",") -> dict:
    _consumption_percentage = {}

    if csv_consumption_data_file and isfile(csv_consumption_data_file):
        # calculate total power
        _data = pd.read_csv(csv_consumption_data_file, sep=seperator, decimal=decimal_sign)
        _power_total = _data[power_col_name].sum()

        # calculate percentage on total power for line
        _percentage_data = (_data[power_col_name] / _power_total).round(3)
        _consumption_percentage = dict(zip(_data[time_col_name], _percentage_data))

    return _consumption_percentage


def create_year(year: int = 2020) -> list:
    _days_of_year = []
    for month in range(1, 13):
        num_of_days = calendar.monthrange(year, month)[1]
        _days_of_year.append({'month': month, 'days': list(range(1, num_of_days + 1))})

    return _days_of_year


def add_consumption(year: list | None = None,
                    ref_daily_consumption: dict | None = None,
                    monthly_consumption: dict | None = None,
                    yearly_consumption: int = 6000000) -> list | None:
    if year and monthly_consumption and ref_daily_consumption:
        for month in year:
            n_month: int = month['month']
            n_days: int = len(month['days'])
            monthly_power: float = monthly_consumption[n_month]
            daily_consumption = round(monthly_power / n_days, 5)

            # create month day
            month_day: dict = {key: round(value * daily_consumption * yearly_consumption, 5) for key, value in ref_daily_consumption.items()}

            # add reference day to month
            for day in month['days']:
                month['days'][day-1] = month_day

    return year


def year_to_csv(year_data: list | None = None,
                year_number: int = 2020,
                csv_output_file: str | None = None) :
    if year_data and csv_output_file:
        with open("output/reference.csv", "w") as csv_file:
            csv_file.writelines('"Datetime";"Power"\n')

            for month in year_data:
                n_month: int = month['month']
                month_string = "{:02d}".format(n_month)

                for n_day in range(len(month['days'])):
                    day: dict = month['days'][n_day]
                    n_day += 1
                    day_string = "{:02d}".format(n_day)

                    for hour, power in day.items():
                        hour_string: str = "{:02d}".format(hour)
                        csv_file.write(f"\"{year_number}{month_string}{day_string}:{hour_string}\";{power}\n")


# ---- MAIN ----
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Calculate daily consumption",
                                     description='Calculate daily consumption')
    parser.add_argument('-dcf', '--daily_consumption_file')
    parser.add_argument('-mcf', '--monthly_consumption_file')

    args = parser.parse_args()

    if args.daily_consumption_file and args.monthly_consumption_file:
        _daily_consumption = calculate_percentage(args.daily_consumption_file)
        _monthly_consumption = calculate_percentage(args.monthly_consumption_file, time_col_name="month", seperator=";")
        _year = create_year(2024)

        # add daily consumption for the year
        _year = add_consumption(year=_year, ref_daily_consumption=_daily_consumption,
                                monthly_consumption=_monthly_consumption)

        # convert to csv with timestamps
        year_to_csv(year_data=_year,
                    year_number=2024,
                    csv_output_file="output/reference.csv")
