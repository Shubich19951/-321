import argparse
from datetime import datetime

ISO_8601_DATEFORMAT = "%Y-%m-%dT%H:%M:%S"
DEFAULT_DATEFORMAT = "%d-%m-%Y"


def generate_filename(currency, start_date, end_date):
    return f"{currency}_{start_date}_{end_date}.csv"


def convert_datetime(datetime_str, from_format: str, to_format: str):
    return datetime.strptime(datetime_str, from_format).strftime(to_format)


def valid_date(date: str):
    try:
        return datetime.strptime(date, DEFAULT_DATEFORMAT)
    except ValueError:
        msg = f"Введена неккоректная дата: '{date}'."
        raise argparse.ArgumentTypeError(msg)


def validate_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "-c", "--currency", type=str, required=True,
        help="Код валюты для сбора данных. (USD, EUR, RUB)"
    )
    arg_parser.add_argument(
        "--start_date", type=valid_date, required=True,
        help="Дата начала периода для аналитики, в формате дд-мм-гггг",
    )
    arg_parser.add_argument(
        "--end_date", type=valid_date, required=True,
        help="Дата конца периода для аналитики, в формате дд-мм-гггг"
    )

    args = arg_parser.parse_args()

    return args.currency, args.start_date, args.end_date


def shorten_dates(dates):
    return dates[::5] if len(dates) > 31 else dates
