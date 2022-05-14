from pydantic import BaseModel
from nonebot import get_driver
from typing import List


class PluginConfig(BaseModel):

    enable_group: List[int] = []
    api_key = '9cb50f042fbfa22fb2387a3466266d7b'
    api_id = '17312'


driver = get_driver()
global_cfg = driver.config

config: PluginConfig = PluginConfig.parse_obj(global_cfg.dict())
