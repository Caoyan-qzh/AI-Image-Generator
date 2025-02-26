# AI Image Generator

A batch image generation tool based on Alibaba Cloud Tongyi Model

English | [简体中文](README.md)

## Features

- Batch AI image generation
- Customizable storage paths and folder structures
- Automatic prompt text saving
- Resume from breakpoint
- Smart request rate limiting
- Detailed error logging

## Requirements

- Python 3.7+
- aiohttp
- Pillow
- Alibaba Cloud Tongyi API Key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ai-image-generator.git
cd ai-image-generator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the configuration template:

```bash
cp config.example.py config.py
```

2. Set your API key and other configurations in config.py:

```python
API_KEY = "your-api-key-here"
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"

# Output settings
OUTPUT_DIR = "output"  # Output directory
IMAGE_FORMAT = "jpg"   # Image format
```

## Usage

1. Prepare the prompts file

Add one prompt per line in `prompts.txt`:

```text
An apple cut open with a flower growing inside
A fan spinning with wind blowing inward
...
```

2. Run the program

```bash
python generate_images.py
```

The program will automatically:
- Create output directory
- Read prompts file
- Generate images in batch
- Save images and prompts
- Log errors

## Output Structure

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

## Advanced Configuration

Customize more parameters in `config.py`:

```python
# Batch processing settings
BATCH_SIZE = 10        # Number of items per batch
BATCH_DELAY = 60       # Delay between batches (seconds)
REQUEST_DELAY = 15     # Delay between requests (seconds)

# Retry settings
MAX_RETRIES = 3        # Maximum retry attempts
RETRY_DELAY = 5        # Delay between retries (seconds)

# Image settings
IMAGE_SIZE = "1024*1024"  # Image dimensions
IMAGE_COUNT = 1           # Images per prompt
```

## Error Handling

- Automatic API rate limit handling
- Failed generations are logged to error.log
- Supports resuming from last successful generation

## Roadmap

- [ ] Support for more image formats
- [ ] Add Web interface
- [ ] Support for more AI models
- [ ] Optimize concurrent processing

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License

## Acknowledgments

- [Alibaba Cloud Tongyi Platform](https://dashscope.aliyun.com)
- [Python aiohttp](https://docs.aiohttp.org)
- [Pillow](https://python-pillow.org)