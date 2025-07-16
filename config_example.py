# Video2Script 配置文件示例
# 请复制此文件为 config.py 并修改相应的配置

# DeepSeek API配置
# 请访问 https://platform.deepseek.com/ 获取您的API密钥
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"  # 请替换为您的实际API密钥
DEEPSEEK_API_BASE = "https://api.deepseek.com"

# 应用设置
APP_TITLE = "Video2Script - 视频转脚本工具"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# 支持的文件格式
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mov', '.avi', '.mkv']
SUPPORTED_TEMPLATE_FORMATS = ['.docx', '.doc']

# 默认模板设置
DEFAULT_TEMPLATE = {
    "title": "技能操作培训脚本",
    "sections": [
        "培训目标",
        "操作步骤",
        "注意事项",
        "总结"
    ]
}

# 输出设置
OUTPUT_DIR = "output"
TEMP_DIR = "temp"

# 语音识别设置
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1

# 文本处理设置
MAX_TEXT_LENGTH = 4000  # 单次处理的文本长度限制
CHUNK_OVERLAP = 200     # 文本分块重叠长度

# 使用说明:
# 1. 将此文件复制为 config.py
# 2. 在 DeepSeek 平台注册账号并获取API密钥
# 3. 将您的API密钥替换 DEEPSEEK_API_KEY 的值
# 4. 保存文件后即可使用真实API功能 