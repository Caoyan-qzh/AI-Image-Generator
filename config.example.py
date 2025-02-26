# -*- coding: utf-8 -*-

# API配置
API_KEY = "your-api-key-here"  # 在阿里云百炼平台获取API密钥：https://bailian.console.aliyun.com
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"

# 模型配置
MODEL = "wanx2.1-t2i-turbo"  # 使用的模型名称

# 输出配置
OUTPUT_DIR = "ai"  # 输出目录
IMAGE_FORMAT = "jpg"  # 图片格式
IMAGE_SIZE = "1024*1024"  # 图片尺寸
IMAGE_COUNT = 1  # 每个提示词生成的图片数量

# 批处理配置
BATCH_SIZE = 10  # 每批处理的提示词数量
BATCH_DELAY = 60  # 批次间延迟(秒)
REQUEST_DELAY = 15  # 请求间延迟(秒)

# 重试配置
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 5  # 重试延迟(秒)

# 日志配置
ERROR_LOG = "error.log"  # 错误日志文件
PROMPTS_FILE = "prompts.txt"  # 提示词文件