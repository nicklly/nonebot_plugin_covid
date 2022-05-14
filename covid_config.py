from pydantic import BaseModel
from nonebot import get_driver
from typing import List


class PluginConfig(BaseModel):

    enable_group: List[int] = []
    api_key = ''
    api_id = ''


driver = get_driver()
global_cfg = driver.config

config: PluginConfig = PluginConfig.parse_obj(global_cfg.dict())
