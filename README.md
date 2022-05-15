# nonebot2_plugin_covid
查询国内新冠疫情

<div align="center">

# 新冠肺炎疫情数据查询
（支持国内各省市及地级市、海外国家）

</div>


## 版本

v0.0.1

⚠ 适配nonebot2-2.0.0beta2版本；

## 安装

1. 通过`pip`或`nb`安装；

命令

`pip install nonebot_plugin_covid`

`nb plugin install nonebot_plugin_covid`

###配置
根据.env里的ENVIRONMENT配置项自行选择.env.dev或.env.prod<br>
然后添加 WAPI_ID和WAPI_KEY两项配置<br>
如:<br>
`WAPI_ID='''`<br>
`WAPI_KEY=''`

注: key加密默认方式为<font color='red'>Hash</font>，具体请自行查阅API文档

## 功能

查询 国内/海外 疫情数据

注：因部分海外国家列出了下属城市的疫情数据，由于篇幅过长可能导致查阅困难<br>
默认covid_config.py里的`enable_country_covid19_data=False`<br>
如需打开请自行设置`enable_country_covid19_data=True`

## 命令

`疫情` `新冠` `covid`


### 需要参数：
<city> 国家、城市、省份请自行参考city_list.py


### 使用注意
使用第三方提供API 需要自行到<a href="https://www.wapi.cn/">点击这里</a>申请appid和key 


### 功能演示
海外国家查询：
<img src='https://github.com/nicklly/nonebot2_plugin_covid/blob/main/img/QQ%E6%88%AA%E5%9B%BE20220515152720.png?raw=true'>

国内城市查询：
<img src='https://github.com/nicklly/nonebot2_plugin_covid/blob/main/img/QQ%E6%88%AA%E5%9B%BE20220515152751.png?raw=true'>

国内省份查询：
<img src='https://github.com/nicklly/nonebot2_plugin_covid/blob/main/img/QQ%E6%88%AA%E5%9B%BE20220515152737.png?raw=true'>