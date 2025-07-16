#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video2Script - 视频转脚本工具
主程序入口
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui_simple import Video2ScriptGUI
    import config
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保已安装所有依赖包: pip install -r requirements.txt")
    sys.exit(1)

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'tkinter',
        'docx',
        'moviepy',
        'requests',
        'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'docx':
                from docx import Document
            elif package == 'moviepy':
                from moviepy.editor import VideoFileClip
            elif package == 'requests':
                import requests
            elif package == 'PIL':
                from PIL import Image
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_config():
    """检查配置文件"""
    if config.DEEPSEEK_API_KEY == "your_deepseek_api_key_here":
        print("警告: 请在config.py中配置您的DeepSeek API密钥")
        print("当前将使用模拟模式进行测试")
        return False
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("Video2Script - 视频转脚本工具")
    print(f"版本: {config.APP_VERSION}")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        input("按回车键退出...")
        sys.exit(1)
    
    # 检查配置
    api_configured = check_config()
    
    try:
        # 创建主窗口
        root = tk.Tk()
        
        # 设置窗口图标（如果有的话）
        try:
            root.iconbitmap("icon.ico")
        except:
            pass
        
        # 创建应用实例
        app = Video2ScriptGUI(root)
        
        # 显示配置提示
        if not api_configured:
            messagebox.showwarning(
                "配置提示", 
                "检测到未配置DeepSeek API密钥，当前使用模拟模式。\n\n"
                "如需使用真实API功能，请在config.py中配置您的API密钥。"
            )
        
        # 启动应用
        print("应用启动成功")
        root.mainloop()
        
    except Exception as e:
        print(f"应用启动失败: {e}")
        messagebox.showerror("错误", f"应用启动失败:\n{str(e)}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main() 