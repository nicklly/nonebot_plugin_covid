import nonebot
from pydantic import BaseModel
from nonebot import get_driver
from typing import List
"""
根据.env的配置
自动从.env.dev或.env.prod里分别读取WAPI_ID和WAPI_KEY
"""
wapi_config = nonebot.get_driver().config.dict()


class PluginConfig(BaseModel):
    enable_group: List[int] = []
    """
    是否列出部分国家的下属城市疫情数据
    """
    enable_country_covid19_data = False
    """
    apiid和apikey需自行到https://www.wapi.cn/注册账号后申请
    不建议频繁调用API查询数据，每天有100次的免费限制
    """
    api_id = wapi_config['wapi_id']
    api_key = wapi_config['wapi_key']


driver = get_driver()
global_cfg = driver.config
config: PluginConfig = PluginConfig.parse_obj(global_cfg.dict())
