# AI Image Generator

基于阿里云灵积模型的批量图片生成工具

[English](README_EN.md) | 简体中文

## 功能特点

- 支持批量生成AI图片
- 自定义存储路径和文件夹结构
- 自动保存生成提示词
- 断点续传功能
- 智能请求限制处理
- 详细的错误日志记录

## 环境要求

- Python 3.7+
- aiohttp
- Pillow
- 阿里云灵积API密钥（注册即送500万tokens免费额度）

## 贡献者

这个项目由以下人员共同创建：

- [qinzihan666](https://github.com/qinzihan666) 
- [Caoyan-qzh](https://github.com/Caoyan-qzh) 

## 安装

1. 克隆项目到本地：

```bash
git clone https://github.com/yourusername/ai-image-generator.git
cd ai-image-generator
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 配置

1. 复制配置文件模板：

```bash
cp config.example.py config.py
```

2. 在config.py中设置你的API密钥和其他配置：

```python
API_KEY = "your-api-key-here"  # 在阿里云百炼平台获取API密钥：https://bailian.console.aliyun.com
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"

# 输出配置
OUTPUT_DIR = "output"  # 输出目录
IMAGE_FORMAT = "jpg"   # 图片格式
```

## 使用方法

1. 准备提示词文件

在`prompts.txt`中每行写入一个图片生成提示词：

```text
一个苹果被切开后，果肉内部长出一朵鲜花
一个风扇旋转时，风向扇叶内部吹去
...
```

2. 运行程序

```bash
python generate_images.py
```

程序会自动：
- 创建输出目录
- 读取提示词文件
- 批量生成图片
- 保存图片和提示词
- 记录错误日志

## 输出结构

```
output/
  ├── 1/
  │   ├── image.jpg
  │   └── info.txt
  ├── 2/
  │   ├── image.jpg
  │   └── info.txt
  └── ...
```

## 高级配置

在`config.py`中可以自定义更多参数：

```python
# 批处理配置
BATCH_SIZE = 10        # 每批处理数量
BATCH_DELAY = 60       # 批次间延迟(秒)
REQUEST_DELAY = 15     # 请求间延迟(秒)

# 重试配置
MAX_RETRIES = 3        # 最大重试次数
RETRY_DELAY = 5        # 重试延迟(秒)

# 图片配置
IMAGE_SIZE = "1024*1024"  # 图片尺寸
IMAGE_COUNT = 1           # 每个提示词生成图片数
```

## 错误处理

- 程序会自动处理API限流
- 失败的生成会记录到error.log
- 支持断点续传，可以从上次中断处继续

## 开发计划

- [ ] 支持更多图片格式
- [ ] 添加Web界面
- [ ] 支持更多AI模型
- [ ] 优化并发处理

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 致谢

- [阿里云灵积平台](https://bailian.console.aliyun.com) - 注册即送500万tokens免费额度
- [Python aiohttp](https://docs.aiohttp.org)
- [Pillow](https://python-pillow.org)
