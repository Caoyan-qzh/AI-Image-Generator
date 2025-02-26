#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""AI Image Generator - API测试程序

用于测试阿里云灵积模型API的连接和响应
Test program for Alibaba Cloud Lingji Model API connection and response

使用方法 / Usage:
1. 复制config.example.py为config.py并设置API密钥
   Copy config.example.py to config.py and set your API key
2. 运行此脚本测试API连接
   Run this script to test API connection
"""

import aiohttp
import asyncio
import importlib.util
import sys

# 导入配置文件 / Import configuration
try:
    spec = importlib.util.spec_from_file_location("config", "config.py")
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
except FileNotFoundError:
    print("错误：请先复制config.example.py为config.py并设置你的API密钥")
    print("Error: Please copy config.example.py to config.py and set your API key first")
    sys.exit(1)

# 从配置文件读取设置 / Load settings from config
API_URL = config.API_URL
API_KEY = config.API_KEY
MODEL = config.MODEL

async def fetch(session, url, payload, headers):
    """发送API请求 / Send API request
    
    Args:
        session: aiohttp客户端会话 / aiohttp client session
        url: API端点 / API endpoint
        payload: 请求数据 / Request data
        headers: 请求头 / Request headers
        
    Returns:
        dict: API响应数据 / API response data
    """
    async with session.post(url, json=payload, headers=headers) as response:
        return await response.json()

async def check_task_status(session, task_id):
    """检查任务状态 / Check task status
    
    Args:
        session: aiohttp客户端会话 / aiohttp client session
        task_id: 任务ID / Task ID
        
    Returns:
        dict: 任务状态信息 / Task status information
    """
    headers = {'Authorization': f'Bearer {API_KEY}'}
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def main():
    """主程序 / Main program
    
    测试API连接并生成一张示例图片
    Test API connection and generate a sample image
    """
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'X-DashScope-Async': 'enable'
    }

    payload = {
        "model": MODEL,
        "input": {"prompt": "一只穿着宇航服的小狗"},
        "parameters": {"size": "1024*1024", "n": 1}
    }

    async with aiohttp.ClientSession() as session:
        # 第一步：创建任务 / Step 1: Create task
        print("\n1. 创建图片生成任务...")
        response = await fetch(session, API_URL, payload, headers)
        print("API响应:", response)

        if 'output' in response and 'task_id' in response['output']:
            task_id = response['output']['task_id']
            print(f"获取到任务ID: {task_id}")

            # 第二步：轮询检查任务状态 / Step 2: Poll task status
            print("\n2. 检查任务状态...")
            while True:
                status_response = await check_task_status(session, task_id)
                print("任务状态:", status_response['output']['task_status'])

                if status_response['output']['task_status'] in ['SUCCEEDED', 'FAILED']:
                    print("\n3. 任务完成！")
                    print("完整响应:", status_response)
                    break
                
                await asyncio.sleep(2)  # 等待2秒后再次检查 / Wait 2 seconds before next check

if __name__ == "__main__":
    print("开始测试阿里云灵积模型API连接...\n")
    asyncio.run(main())