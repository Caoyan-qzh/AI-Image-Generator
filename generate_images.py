import os
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO
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
OUTPUT_DIR = config.OUTPUT_DIR
IMAGE_FORMAT = config.IMAGE_FORMAT
IMAGE_SIZE = config.IMAGE_SIZE
IMAGE_COUNT = config.IMAGE_COUNT
BATCH_SIZE = config.BATCH_SIZE
BATCH_DELAY = config.BATCH_DELAY
REQUEST_DELAY = config.REQUEST_DELAY
MAX_RETRIES = config.MAX_RETRIES
RETRY_DELAY = config.RETRY_DELAY
ERROR_LOG = config.ERROR_LOG
PROMPTS_FILE = config.PROMPTS_FILE
MODEL = config.MODEL

# 从文件读取提示词 / Read prompts from file
try:
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"错误：找不到提示词文件 {PROMPTS_FILE}")
    print(f"Error: Prompt file {PROMPTS_FILE} not found")
    sys.exit(1)

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

async def generate_and_save(session, index, prompt, max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY):
    """生成并保存图片 / Generate and save image
    
    Args:
        session: aiohttp客户端会话 / aiohttp client session
        index: 当前处理的索引 / Current processing index
        prompt: 生成提示词 / Generation prompt
        max_retries: 最大重试次数 / Maximum retry attempts
        retry_delay: 重试延迟(秒) / Retry delay in seconds
        
    Returns:
        str: 处理结果信息 / Processing result message
    """
    print(f"开始生成第 {index} 个场景: {prompt}")
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"第 {attempt + 1} 次重试...")
                await asyncio.sleep(retry_delay)

            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json',
                'X-DashScope-Async': 'enable'
            }

            payload = {
                "model": MODEL,
                "input": {"prompt": prompt},
                "parameters": {"size": IMAGE_SIZE, "n": IMAGE_COUNT}
            }

            async with session.post(API_URL, json=payload, headers=headers) as response:
                response_data = await response.json()
                
                if response_data.get('code') == 'Throttling.RateQuota':
                    print(f"API请求限制，等待{retry_delay * 2}秒后重试...")
                    await asyncio.sleep(retry_delay * 2)
                    continue

                if 'output' not in response_data or 'task_id' not in response_data['output']:
                    raise Exception(f"无效的API响应: {response_data}")

                task_id = response_data['output']['task_id']
                print(f"获取到任务ID: {task_id}")

                while True:
                    status_response = await check_task_status(session, task_id)
                    task_status = status_response['output']['task_status']
                    print(f"任务状态: {task_status}")
                    
                    if task_status == 'SUCCEEDED':
                        image_url = status_response['output']['results'][0]['url']
                        async with session.get(image_url) as img_response:
                            img_data = await img_response.read()
                        
                        image = Image.open(BytesIO(img_data))
                        folder_path = os.path.join(OUTPUT_DIR, str(index))
                        os.makedirs(folder_path, exist_ok=True)
                        
                        image_path = os.path.join(folder_path, f"image.{IMAGE_FORMAT}")
                        image.save(image_path, IMAGE_FORMAT.upper())
                        
                        info_path = os.path.join(folder_path, "info.txt")
                        with open(info_path, "w", encoding="utf-8") as f:
                            f.write(prompt)
                        
                        return f"成功生成: {folder_path}"
                    
                    elif task_status == 'FAILED':
                        raise Exception(f"任务执行失败: {status_response}")
                    
                    await asyncio.sleep(2)

        except Exception as e:
            if attempt == max_retries - 1:
                with open(ERROR_LOG, "a", encoding="utf-8") as log:
                    log.write(f"生成失败: {prompt}, 错误: {str(e)}\n")
                return f"生成失败: {prompt}"
            print(f"尝试失败: {str(e)}，准备重试...")

def get_last_processed_index():
    """获取上次处理的最后索引 / Get the last processed index
    
    Returns:
        int: 最后处理的索引 / Last processed index
    """
    processed_folders = [f for f in os.listdir(OUTPUT_DIR) 
                       if os.path.isdir(os.path.join(OUTPUT_DIR, f)) and f.isdigit()]
    return max([int(f) for f in processed_folders], default=0)

async def process_all_prompts():
    """处理所有提示词 / Process all prompts"""
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        last_index = get_last_processed_index()
        print(f"从索引 {last_index + 1} 开始继续处理...")
        
        remaining_prompts = prompts[last_index:]
        total_batches = len(remaining_prompts) // BATCH_SIZE + (1 if len(remaining_prompts) % BATCH_SIZE else 0)
        
        async with aiohttp.ClientSession() as session:
            for i in range(0, len(remaining_prompts), BATCH_SIZE):
                batch = remaining_prompts[i:i + BATCH_SIZE]
                current_batch = i // BATCH_SIZE + 1
                print(f"\n开始处理第 {current_batch} 批场景 (总共 {total_batches} 批)")
                
                for j, prompt in enumerate(batch):
                    current_index = last_index + i + j + 1
                    if j > 0:
                        print(f"等待{REQUEST_DELAY}秒后处理下一个任务...")
                        await asyncio.sleep(REQUEST_DELAY)
                    result = await generate_and_save(session, current_index, prompt)
                    print(result)
                
                if i + BATCH_SIZE < len(remaining_prompts):
                    print(f"\n当前批次完成，等待{BATCH_DELAY}秒后处理下一批...")
                    await asyncio.sleep(BATCH_DELAY)
                    
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        raise

def main():
    """主程序入口 / Main program entry"""
    try:
        asyncio.run(process_all_prompts())
    except Exception as e:
        print(f"主程序执行出错: {str(e)}")

if __name__ == "__main__":
    main()