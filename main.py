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
        yield event.plain_result("正在查询攻略，请稍候...")

        try:
            url = f'https://api.yaohud.cn/api/v5/mihoyou/yuan?key=SqGWZxWJxEWagRFxkqB&msg={message}'
            response = requests.post(url, data={'key1': 'value1', 'key2': 'value2'})
            
            try:
                result = response.json()
            except json.JSONDecodeError as e:
                logging.error(f"JSON解析失败: {str(e)}")
                yield event.plain_result(f"数据解析失败，原始响应：\n{response.text}")
                return

            print(result)            

            if result['code'] == '200':
                # 格式化输出信息

                if result['url'] == '未找到有关信息':
                    yield event.plain_result("抱歉，未找到相关信息喵。")
                    return

                basic = ''.join([f'• {info}\n' for info in result['text']])
                formatted_msg = f"""
⭐ 角色攻略：{result['name']} ⭐

🖼️ 角色简介：
{result['icon']}

📍 基本信息：
{basic}

🎯 获取途径：{result['bbs']}

🤝 推荐配队：
队伍类型：{result['ranks']}
推荐阵容：{result['teamname']}
配队说明：{result['yaohuby']}

🗡️ 武器推荐：

前期武器：{result['recommendation']['one']['name']}
{result['recommendation']['one']['introduce']}

毕业武器：{result['recommendation']['two']['name']}
{result['recommendation']['two']['introduce']}

📊 圣遗物搭配：

前期搭配：{result['recommendation']['one']['early']}
主词条优先级：{result['recommendation']['one']['order']}
圣遗物部位：{result['recommendation']['one']['sequence']}
说明：{result['recommendation']['one']['yaoby']}

毕业搭配：{result['recommendation']['two']['early']}
主词条优先级：{result['recommendation']['two']['order']}
圣遗物部位：{result['recommendation']['two']['sequence']}
说明：{result['recommendation']['two']['yaoby']}

📝 数据来源：{result['yaohu']}
"""
                yield event.plain_result(formatted_msg)
            else:
                yield event.plain_result("抱歉，查询失败，请稍后重试。")

        except requests.RequestException as e:
            logging.error(f"请求失败: {str(e)}")
            yield event.plain_result(f"网络请求失败，请稍后重试。错误信息：{str(e)}")
