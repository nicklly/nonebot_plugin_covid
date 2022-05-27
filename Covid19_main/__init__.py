import re
import time

import requests

from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, escape
from typing import Union

from nonebot.matcher import Matcher
from nonebot import on_command
from nonebot.params import Arg, CommandArg, ArgPlainText
from ..util.covid_config import config
from ..util.city_list import city_list, province_list, country_list
from ..util.common import get_covid_china_info, get_covid_global_info

covid = on_command('covid', aliases={'新冠', '疫情', 'covid'}, priority=18)
r = requests.session()


@covid.handle()
async def _handle(event: Union[GroupMessageEvent, MessageEvent], matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg('city', args)


@covid.got('city', prompt="您想查询哪座城市的疫情数据呢？")
async def _(event: Union[GroupMessageEvent, MessageEvent], city: str = ArgPlainText('city')):
    message = ''
    if re.match(r'.*CQ:.*', city):
        return
    else:
        if city in city_list or city in province_list or city in country_list:
            try:
                res = await get_covid_china_info(city)
                if res['codeid'] != 10000:
                    await covid.finish(res['message'])
                result = res['retdata']
            except TypeError as e:
                await covid.finish(f'程序出错:{e}')
            """
            各省数据查询   
            """
            if city in province_list:
                updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(result['updateTime'])))

                subList = result['dangerousAreas']['subList']
                message += config.City_template.format(result['xArea'], updateTime, result['confirm'], result['died'], result['heal'])

                if len(subList) > 0:
                    message += "当前{0}共有{1}个中高风险地区\n".format(result['xArea'], len(subList))
                    tmp = subList[0: 5]
                    for i in range(len(tmp)):
                        message += "\n{0}地区: {1}".format(tmp[i]['level'], tmp[i]['xArea'])
                    message += '\n\n'
                else:
                    message += '当前省份没有中高风险地区\n'
                if result['dangerousAreas']['moreUrl']:
                    message += "如要查阅详细的风险地区, 请到: {0} 查询".format(result['dangerousAreas']['moreUrl'])
                """
                直辖市、特殊区域、港澳台  
                """
            elif city in ['北京', '上海', '重庆', '天津', '香港', '澳门', '台湾', '新疆', '西藏']:
                updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(result['updateTime'])))

                subList = result['subList']
                message += config.City_template.format(result['xArea'], updateTime, result['confirm'], result['died'], result['heal'])

                for i in range(len(subList)):
                    subList2 = subList[i]['dangerousAreas']['subList']
                    if len(subList2) > 10 or len(subList2) < 10:
                        tmp = subList2[0: 5]
                    for n in range(len(tmp)):
                        message += "{0}地区: {1}\n".format(tmp[n]['level'], tmp[n]['xArea'])
                if result['dangerousAreas']['moreUrl']:
                    message += "\n"
                    message += "如要查阅详细的风险地区, 请到: {0} 查询".format(result['dangerousAreas']['moreUrl'])
            elif city in city_list:
                """
                    其他地级市，不支持县级市及下属行政区
                    """
                updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(result['updateTime'])))
                subList = result['dangerousAreas']['subList']
                message += config.City_template.format(result['city'], updateTime, result['confirm'], result['died'], result['heal'])

                tmp = subList[0: 5]
                for i in range(len(tmp)):
                    message += "{0}地区: {1}\n".format(tmp[i]['level'], tmp[i]['xArea'])
                if result['dangerousAreas']['moreUrl']:
                    message += "\n"
                    message += "如要查阅详细的风险地区, 请到: {0} 查询".format(result['dangerousAreas']['moreUrl'])

                """
                查询海外疫情数据 仅部分国家支持显示下属城市
                """
            elif city in country_list:
                try:
                    res = await get_covid_global_info()
                    if res['codeid'] != 10000:
                        await covid.finish(res['message'])
                    result = res['retdata']
                except TypeError as e:
                    await covid.finish(f'程序出错:{e}')

                for i in range(len(result)):
                    """
                    匹配海外国家
                    """
                    rematch = re.match(city, result[i]['xArea'])
                    subList = result[i]['subList']

                    if rematch:
                        if rematch.group() == result[i]['xArea']:

                            updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(result[i]['relativeTime'])))
                            message += config.Country_template.format(result[i]['xArea'], result[i]['confirm'], result[i]['heal'], result[i]['died'], result[i]['curConfirm'], updateTime)

                            if config.enable_country_covid19_data:
                                if len(subList) > 0:
                                    message += '\n\n{0}的主要城市疫情数据:\n'.format(result[i]['xArea'])
                                    for n in range(len(subList)):
                                        message += '{0}: 确诊: {1}例, 死亡: {2}例, 治愈: {3}例, 治愈率: {4}, 死亡率: {5}\n'.format(
                                            subList[n]['city'], subList[n]['confirm'], subList[n]['died'],
                                            subList[n]['heal'], subList[n]['curedPercent'], subList[n]['diedPercent'])

            await covid.finish(message)
        else:
            await covid.finish(f"您所输入的 {city} 暂不支持查询, 请重新输入")
