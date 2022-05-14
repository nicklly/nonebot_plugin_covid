#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="nonebot_plugin_covid",
    version="0.0.1",
    keywords=["pip", "nonebot_plugin_covid"],
    description="search covid of China",
    long_description="",
    license="GPL Licence",
    url="https://github.com/nicklly/nonebot2_covid_plugin",
    author="TonyKun",
    author_email="1134741727@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "pydantic >= 1.9.0",
        "nonebot2 >= 2.0.0b1",
        "nonebot-adapter-onebot >= 2.0.0b1",
    ],
)