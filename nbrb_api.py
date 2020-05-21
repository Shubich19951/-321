from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

NBRB_API_DATEFORMAT = "%Y-%m-%d"
NBRB_API_URL = "http://www.nbrb.by/API/ExRates/Rates/Dynamics/{}"

CURRENCIES = {
    "RUB": 190,
    "EUR": 19,
    "USD": 145,
}


class NBRBApiException(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return self.message or "Error while working with NBRB API."


def construct_session():
    session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    session.mount("http://", HTTPAdapter(max_retries=retries))
    return session


def get_rates(currency: str, start_date: datetime, end_date: datetime) -> dict:
    """ Get rates from NBRB API"""

    currency_code = CURRENCIES.get(currency.upper())
    if currency_code is None:
        raise NBRBApiException(F"Can't find currency code for currency {currency}")

    url = NBRB_API_URL.format(currency_code)
    params = {
        "startDate": start_date.strftime(NBRB_API_DATEFORMAT),
        "endDate": end_date.strftime(NBRB_API_DATEFORMAT)
    }

    session = construct_session()
    try:
        response = session.get(url=url, params=params)
    except requests.exceptions.ConnectionError:
        raise NBRBApiException("Connection errors after several retries!")
    else:
        if response.status_code != 200:
            raise NBRBApiException(f"NBRB API returned {response.status_code} http status code")
        return response.json()
    finally:
        session.close()
