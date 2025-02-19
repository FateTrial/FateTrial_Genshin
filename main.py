import json
import requests
import os
import aiohttp
import asyncio
import logging

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.all import *
from astrbot.api.message_components import *

@register("Genshin", "FateTrial", "原神攻略查询插件", "1.0.0")
class StrategyQuery(Star):
    @filter.command("原神查询")
    async def query_strategy(self, event: AstrMessageEvent, *, message: str):
        # 发送消息，提示用户正在查询攻略
        yield event.plain_result("正在查询攻略，请稍候...")

        # 构造请求url
        url = f'https://api.yaohud.cn/api/v5/mihoyou/yuan?key=SqGWZxWJxEWagRFxkqB&msg={message}'
 
        # 发送post请求
        response = requests.post(url, data={'key1': 'value1', 'key2': 'value2'})
 
        # 获取响应内容
        result = response.json()

        # 打印结果
        json_str = json.dumps(result, ensure_ascii=False, indent=4)
        # 发送结果给用户
        yield event.plain_result(json_str)
