import datetime
import logging

from .covid_config import config
from ..util import aiorequest


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
        req = await aiorequest.get(url="https://giea.api.storeapi.net/api/94/221", headers=header, params=param)
        res = req.json()
        if res['codeid'] == 10000:
            return res
        return res
    except Exception as e:
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
        req = await aiorequest.get("https://giea.api.storeapi.net/api/94/220", headers=header, params=param)
        res = req.json()
        if res['codeid'] == 10000:
            return res
        return res
    except Exception as e:
        logging.error(e)
