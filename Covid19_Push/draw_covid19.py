import json
import os
from encodings import unicode_escape

from PIL import ImageFont, ImageDraw, Image, ImageColor
from nonebot.adapters.onebot.v11 import escape

from ..util.pil_util import load_image, get_font, MessageBuild

res_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'res')


async def draw_covid19_1(data):
    if not data:
        return '数据缺失'

    data = json.loads(data)
    bg_img = load_image(os.path.join(res_path, 'covid19', 'bg.jpg'))
    bg_draw = ImageDraw.Draw(bg_img)
    
    bg_draw.text((20, 5), '疫情数据', fill='white', font=get_font(50, '优设标题黑.ttf'))
    bg_draw.text((20, 85), f'当前绑定: {data["xArea"]}', fill='white', font=get_font(25, '优设标题黑.ttf'))
    bg_draw.text((20, 115), f'截止到: {data["time"]}', fill='white', font=get_font(25, '优设标题黑.ttf'))
    bg_draw.text((20, 145), f'累计确诊: {data["confirm"]}例', fill='white', font=get_font(25, '优设标题黑.ttf'))
    bg_draw.text((20, 175), f'累计治愈: {data["heal"]}例', fill='white', font=get_font(25, '优设标题黑.ttf'))
    bg_draw.text((20, 205), f'累计死亡: {data["died"]}例', fill='white', font=get_font(25, '优设标题黑.ttf'))

    return MessageBuild.Image(bg_img, size=0.35, quality=70)


async def draw_covid19_2(data):
    if not data:
        return '数据缺失'

    data = json.loads(data)
    bg_img = load_image(os.path.join(res_path, 'covid19', 'bg.jpg'))
    bg_draw = ImageDraw.Draw(bg_img)

    bg_draw.text((20, 5), '疫情数据', fill='white', font=get_font(50, '优设标题黑.ttf'))
    bg_draw.text((20, 85), f'当前绑定: {data["xArea"]}', fill='white', font=get_font(25, '优设标题黑.ttf'))
    bg_draw.text((20, 145), f'累计确诊: {data["confirm"]}例', fill='white', font=get_font(25, '优设标题黑.ttf'))
    bg_draw.text((20, 175), f'累计治愈: {data["heal"]}例', fill='white', font=get_font(25, '优设标题黑.ttf'))
    bg_draw.text((20, 205), f'累计死亡: {data["died"]}例', fill='white', font=get_font(25, '优设标题黑.ttf'))
    bg_draw.text((20, 115), f'截止到: {data["time"]}, 共新增: {data["curconfirm"]}例', fill='white', font=get_font(25, '优设标题黑.ttf'))

    return MessageBuild.Image(bg_img, size=0.35, quality=70)