import base64
import os

from PIL import Image, ImageFont
from pathlib import Path
from typing import Union, Optional, Tuple
from io import BytesIO

from nonebot.adapters.onebot.v11 import MessageSegment

res_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'res')


class MessageBuild:

    @classmethod
    def Image(cls,
              img: Union[Image.Image, Path, str],
              *,
              size: Optional[Union[Tuple[int, int], float]] = None,
              crop: Optional[Tuple[int, int, int, int]] = None,
              quality: Optional[int] = 100,
              mode: Optional[str] = 'RGB'
              ) -> MessageSegment:
        if isinstance(img, str) or isinstance(img, Path):
            img = load_image(path=img, size=size, mode=mode, crop=crop)
        bio = BytesIO()
        img = img.convert(mode)
        img.save(bio, format='JPEG' if mode == 'RGB' else 'PNG', quality=quality)
        img_b64 = 'base64://' + base64.b64encode(bio.getvalue()).decode()
        return MessageSegment.image(img_b64)


def get_font(size, font='msyh.ttc'):
    return ImageFont.truetype(os.path.join(res_path, font), size)


def load_image(
        path: Union[Path, str],
        *,
        size: Optional[Union[Tuple[int, int], float]] = None,
        crop: Optional[Tuple[int, int, int, int]] = None,
        mode: Optional[str] = None,
):
    img = Image.open(path)
    if size:
        if isinstance(size, float):
            img = img.resize((int(img.size[0] * size), int(img.size[1] * size)), Image.ANTIALIAS)
        elif isinstance(size, tuple):
            img = img.resize(size, Image.ANTIALIAS)
    if crop:
        img = img.crop(crop)
    if mode:
        img = img.convert(mode)
    return img
