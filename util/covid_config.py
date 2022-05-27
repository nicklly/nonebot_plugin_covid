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

    """
    消息推送模板
    """
    City_template = "当前查询: {0}\n" \
                    "数据更新时间: {1}\n" \
                    "累计确诊: {2}例, 死亡: {3}例, 治愈: {4}例\n"

    Country_template = '当前查询: {0}\n' \
                       '{0}累计确诊: {1}例, 治愈:{2}例, 死亡: {3}例\n' \
                       '截止到 {5}, {0}新增: {4}例'

    push_city_template = "========= 定时推送 =========\n" \
                         "当前已绑定: {0}\n" \
                         "截止到: {1}\n" \
                         "累计确诊: {2}例, 死亡: {3}例, 治愈: {4}例\n" \
                         "========= 推送结束 ========="

    push_country_template = "========= 定时推送 =========\n" \
                            "当前已绑定: {0}\n" \
                            "截止到: {5}\n" \
                            "{0}累计确诊: {1}例, 治愈:{2}例, 死亡: {3}例\n" \
                            "========= 推送结束 ========="


config: PluginConfig = PluginConfig.parse_obj(get_driver().config.dict())
