import re

from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, Bot
from typing import Union

from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg

from .draw_covid19 import draw_covid19_1, draw_covid19_2
from ..util.city_list import country_list, city_list, province_list

from nonebot import on_command, require, get_bot

from ..util.util import load_data, get_id, get_covid19_province, get_covid19_country, get_covid19_city, save_data

push = on_command("push", aliases={"订阅推送", "push"}, priority=18)
scheduler = require('nonebot_plugin_apscheduler').scheduler


@push.handle()
async def _(event: Union[GroupMessageEvent, MessageEvent], matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg('param]', args)


@push.got('param', prompt='是否在指定时间推送指定 城市/国家 的疫情数据？请用|隔开, 如:开启|北京|06')
async def _handle(event: Union[GroupMessageEvent, MessageEvent], param: str = ArgPlainText('param')):
    args = param.split("|")

    if len(args) == 3 and args[0] == "开启":

        city = str(param.split("|")[1])
        time = param.split("|")[2]

        if city in city_list or city in province_list or city in country_list:
            if re.match(r'.*0[0-9].*', time):
                time = time.replace("0", '')

            push_data = load_data('push_data.json')
            push_id = str(get_id(event))
            push_data[push_id] = {
                'type': event.message_type,
                'hour': int(time),
                'city': str(city)
            }
            if event.message_type == 'guild':
                await push.finish("暂不支持频道内推送~")

            if scheduler.get_job('Covid19_' + str(get_id(event))):
                scheduler.remove_job('Covid19_' + str(get_id(event)))

            save_data(push_data, 'push_data.json')

            await push.finish('开启消息推送成功~', at_sender=True)

            scheduler.add_job(
                func=covid19_push_task,
                trigger='cron',
                hour=time,
                id="Covid19_" + str(get_id(event)),
                misfire_grace_time=10,
                args=(str(get_id(event)), push_data[str(get_id(event))]))
        else:
            await push.finish("暂不支持绑定该 国家/省份/城市")

    elif len(args) == 1 and args[0] == "关闭":
        push_data = load_data('push_data.json')
        del push_data[str(get_id(event))]
        if scheduler.get_job("Cvoid19_" + str(get_id(event))):
            scheduler.remove_job("Covid19_" + str(get_id(event)))
        save_data(push_data, "push_data.json")
        await push.finish("消息推送关闭成功~", at_sender=True)
    elif len(args) == 1 and args[0] == '测试':
        for push_id, push_data in load_data('push_data.json').items():
            if push_data['city'] in city_list:
                result = await get_covid19_city(str(push_data['city']))
            if push_data['city'] in province_list:
                result = await get_covid19_province(str(push_data['city']))
            if push_data['city'] in country_list:
                result = await get_covid19_country(str(push_data['city']))
            if push_data['type'] == 'group':
                await get_bot().send_group_msg(group_id=push_id, message=result)
            elif push_data['type'] == 'private':
                await get_bot().send_private_msg(user_id=push_id, message=result)
    else:
        await push.finish('参数错误，请重新执行此指令', at_sender=True)


async def covid19_push_task(push_id, push_data: dict):
    if push_data['city'] in city_list:
        result = await get_covid19_city(str(push_data['city']))
    if push_data['city'] in province_list:
        result = await get_covid19_province(str(push_data['city']))
    if push_data['city'] in country_list:
        result = await get_covid19_country(str(push_data['city']))

    if push_data['type'] == 'group':
        await get_bot().send_group_msg(group_id=push_id, message=result)
    elif push_data['type'] == 'private':
        await get_bot().send_private_msg(user_id=push_id, message=result)


for push_id, push_data in load_data('push_data.json').items():
    scheduler.add_job(
        func=covid19_push_task,
        trigger='cron',
        hour=push_data['hour'],
        minute=0,
        id="Covid19_" + push_id,
        args=(push_id, push_data),
        misfire_grace_time=10
    )
