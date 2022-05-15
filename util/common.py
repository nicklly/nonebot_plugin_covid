import datetime
import logging

import requests
from ..covid_config import config

r = requests.session()


async def get_covid_china_info(city: str):
    time = datetime.datetime.now().timestamp()
    header = {}
    param = {
        'format': 'json',
        'appid': config.api_id,
        'sign': config.api_key,
        'time': time,
        'city_name': city
    }
    try:
        req = r.get("https://giea.api.storeapi.net/api/94/221", headers=header, params=param)
        res = req.json()
        if res['codeid'] == 10000:
            return res
        return res
    except requests.exceptions.RequestException as e:
        logging.error(e)


async def get_covid_global_info():
    time = datetime.datetime.now().timestamp()
    header = {}
    param = {
        'format': 'json',
        'appid': config.api_id,
        'sign': config.api_key,
        'time': time,
    }
    try:
        req = r.get("https://giea.api.storeapi.net/api/94/220", headers=header, params=param)
        res = req.json()
        if res['codeid'] == 10000:
            return res
        return res
    except requests.exceptions.RequestException as e:
        logging.error(e)
