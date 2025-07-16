@echo off
echo ========================================
echo Video2Script - 视频转脚本工具
echo 安装脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境
    echo 请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python环境检查通过
echo.

echo 正在安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖包安装失败
    pause
    exit /b 1
)

echo.
echo 依赖包安装完成
echo.

echo 正在创建输出目录...
if not exist "output" mkdir output
if not exist "temp" mkdir temp

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 使用说明:
echo 1. 运行 python main.py 启动应用
echo 2. 在config.py中配置您的DeepSeek API密钥
echo 3. 选择视频文件开始处理
echo.
echo 注意: 首次运行将使用模拟模式进行测试
echo.
pause 