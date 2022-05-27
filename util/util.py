import json
import re
import time

from pathlib import Path
from typing import Union, Any

from nonebot import logger
from nonebot.adapters.onebot.v11 import escape, MessageSegment
from ..util.city_list import city_list
from .common import get_covid_china_info, get_covid_global_info
from ..Covid19_Push.draw_covid19 import draw_covid19_1, draw_covid19_2

dict = {}


def load_data(data_file):
    data_path = Path() / 'data' / 'Covid19' / data_file
    if not data_path.exists():
        save_data({}, data_file)
    return json.load(data_path.open('r', encoding='utf-8'))


def save_data(data, data_file):
    data_path = Path() / 'data' / 'Covid19' / data_file
    data_path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, data_path.open('w', encoding='utf-8'), ensure_ascii=False, indent=2)


def get_id(event):
    if event.message_type == 'private':
        return event.user_id
    elif event.message_type == 'group':
        return event.group_id


async def get_covid19_city(city: str) -> Union[str, Any]:
    message: str = ''

    try:
        res = await get_covid_china_info(escape(city))
        if res['codeid'] != 10000:
            return res['message']
    except TypeError as e:
        logger.error(f'程序出错:{e}')

    result = res['retdata']
    if city in ['北京', '上海', '重庆', '天津', '香港', '澳门', '台湾', '新疆', '西藏']:
        updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(result['updateTime'])))

        dict['xArea'] = escape(result['city'])
        dict['time'] = updateTime
        dict['confirm'] = result['confirm']
        dict['died'] = result['died']
        dict['heal'] = result['heal']

        return await draw_covid19_1(json.dumps(dict))

    elif city in city_list:
        updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(result['updateTime'])))

        dict['xArea'] = escape(result['city'])
        dict['time'] = updateTime
        dict['confirm'] = result['confirm']
        dict['died'] = result['died']
        dict['heal'] = result['heal']

        return await draw_covid19_1(json.dumps(dict))


async def get_covid19_province(province: str) -> Union[str, Any]:
    message: str = ''

    try:
        res = await get_covid_china_info(escape(province))
        if res['codeid'] != 10000:
            return res['message']
    except TypeError as e:
        logger.error(f'程序出错:{e}')

    result = res['retdata']

    updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(result['updateTime'])))

    dict['xArea'] = result['city']
    dict['time'] = updateTime
    dict['confirm'] = result['confirm']
    dict['died'] = result['died']
    dict['heal'] = result['heal']

    return json.dumps(dict)


async def get_covid19_country(country: str) -> Union[str, Any]:
    message: str = ''
    try:
        res = await get_covid_global_info()
        if res['codeid'] != 10000:
            return res['message']
    except TypeError as e:
        logger.error(f'程序出错:{e}')

    result = res['retdata']

    for i in range(len(result)):
        rematch = re.match(country, result[i]['xArea'])
        if rematch:
            if rematch.group() == result[i]['xArea']:
                updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(result[i]['relativeTime'])))

                dict['xArea'] = result[i]['xArea']
                dict['time'] = updateTime
                dict['confirm'] = result[i]['confirm']
                dict['died'] = result[i]['died']
                dict['heal'] = result[i]['heal']
                dict['curConfirm'] = result[i]['curConfirm']

            return await draw_covid19_2(json.dumps(dict))
