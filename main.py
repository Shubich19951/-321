import os
import sys

import pandas as pd

import nbrb_api
from plot_graphs import (
    plot_graph,
    plot_std,
    plot_changes,
    plot_histogram,
    plot_decompose,
)
from utils import (
    generate_filename,
    validate_args,
    convert_datetime,
    ISO_8601_DATEFORMAT,
    DEFAULT_DATEFORMAT,
)

CSV_DELIMITER = ","


def save_to_file(rates_data, csv_file_path):
    """Prepares data retrieved from API to csv format and save it file"""

    try:
        dataframe = pd.DataFrame(
            {
                "day": [
                    convert_datetime(day_rate["Date"], ISO_8601_DATEFORMAT, DEFAULT_DATEFORMAT)
                    for day_rate in rates_data
                ],
                "rate": [
                    day_rate["Cur_OfficialRate"]
                    for day_rate in rates_data
                ],
            }
        )
    except KeyError as e:
        print(f"Error while trying to save data to csv-file. Key {e} does not exists")
        sys.exit(1)
    else:
        with open(csv_file_path, "w") as csv_file:
            csv_file.write(dataframe.to_csv(index=False, sep=CSV_DELIMITER))


def generate_plots_from_csv(csv_file_path: str, general_label: str):
    """Reads data from csv file, constructing plots and show them"""

    dataframe = pd.read_csv(csv_file_path, sep=CSV_DELIMITER)
    dataframe.index = pd.to_datetime(dataframe["day"].values, format=DEFAULT_DATEFORMAT)
    dataframe = dataframe.drop(["day"], axis=1)

    df_month = dataframe.resample("M").mean()
    df_quarter = dataframe.resample("Q").mean()

    # plotting
    plot_graph(
        df=dataframe,
        title=f"График зависимости курса валюты от времени (Day)",
        label=general_label,
        xlabel="Время",
        ylabel="Курс валют",
    )

    plot_graph(
        df=df_month,
        title=f"График зависимости курса валюты от времени (Month)",
        label=general_label,
        xlabel="Время",
        ylabel="Курс валют",
    )

    plot_graph(
        df=df_quarter,
        title=f"График зависимости курса валюты от времени (Month)",
        label=general_label,
        xlabel="Время",
        ylabel="Курс валют",
    )

    plot_decompose(df=dataframe)

    plot_changes(
        df=dataframe,
        title=f"График зависимости изменения курса валюты от времени (Day)",
        label=general_label,
        xlabel="Время",
        ylabel="Курс валют"
    )

    plot_histogram(
        df=dataframe,
        title=f"Равноинтервальная гистограмма курса валют (Day)",
        label="Аппроксимация гистограммы",
        xlabel="Курс валют",
        ylabel="Количество вхождений в интервал"
    )

    plot_std(
        df=dataframe,
        title=f"График зависимости cреднеквадратического отклонения курса валюты с окном в 5 дней от времени (Day)",
        label=general_label,
        xlabel="Время",
        ylabel="Среднеквадратическое отклонение"
    )


def main():
    currency, start_date, end_date = validate_args()
    csv_file_path = generate_filename(currency, start_date, end_date)

    if not os.path.exists(csv_file_path):
        try:
            rates_data = nbrb_api.get_rates(currency, start_date, end_date)
        except nbrb_api.NBRBApiException as e:
            print(e, file=sys.stderr)
            sys.exit(1)

        save_to_file(rates_data=rates_data, csv_file_path=csv_file_path)

    plots_label = f"BYN/{currency} {start_date.strftime(DEFAULT_DATEFORMAT)} - {end_date.strftime(DEFAULT_DATEFORMAT)}"
    generate_plots_from_csv(csv_file_path=csv_file_path, general_label=plots_label)


if __name__ == "__main__":
    main()
