#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video2Script 功能测试脚本
"""

import sys
import os
import tempfile
import shutil

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        import config
        print("✓ config模块导入成功")
    except ImportError as e:
        print(f"✗ config模块导入失败: {e}")
        return False
    
    try:
        from speech_to_text import MockSpeechToText
        print("✓ speech_to_text模块导入成功")
    except ImportError as e:
        print(f"✗ speech_to_text模块导入失败: {e}")
        return False
    
    try:
        from text_processor import MockTextProcessor
        print("✓ text_processor模块导入成功")
    except ImportError as e:
        print(f"✗ text_processor模块导入失败: {e}")
        return False
    
    try:
        from document_processor import MockDocumentProcessor
        print("✓ document_processor模块导入成功")
    except ImportError as e:
        print(f"✗ document_processor模块导入失败: {e}")
        return False
    
    try:
        import tkinter
        print("✓ tkinter模块导入成功")
    except ImportError as e:
        print(f"✗ tkinter模块导入失败: {e}")
        return False
    
    return True

def test_speech_to_text():
    """测试语音转文字功能"""
    print("\n测试语音转文字功能...")
    
    try:
        from speech_to_text import MockSpeechToText
        
        stt = MockSpeechToText()
        
        # 创建临时测试文件
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            test_video_path = f.name
        
        # 测试处理
        result = stt.process_video(test_video_path)
        
        if result and len(result.strip()) > 0:
            print("✓ 语音转文字功能正常")
            print(f"  生成文本长度: {len(result)} 字符")
            return True
        else:
            print("✗ 语音转文字功能异常: 返回空结果")
            return False
            
    except Exception as e:
        print(f"✗ 语音转文字功能测试失败: {e}")
        return False
    finally:
        # 清理临时文件
        if 'test_video_path' in locals() and os.path.exists(test_video_path):
            os.unlink(test_video_path)

def test_text_processor():
    """测试文本处理功能"""
    print("\n测试文本处理功能...")
    
    try:
        from text_processor import MockTextProcessor
        
        processor = MockTextProcessor()
        
        # 测试文本
        test_text = """
        欢迎来到技能操作培训课程。今天我们将学习如何正确使用这个设备。
        
        首先，让我们了解一下设备的基本组成部分。设备主要由三个部分组成：
        第一部分是控制面板，第二部分是操作区域，第三部分是安全装置。
        
        在开始操作之前，请确保您已经穿戴好必要的安全装备，包括安全帽、
        防护眼镜和防护手套。
        """
        
        # 测试处理
        result = processor.process_text(test_text)
        
        if result and 'sections' in result and len(result['sections']) > 0:
            print("✓ 文本处理功能正常")
            print(f"  生成章节数: {len(result['sections'])}")
            return True
        else:
            print("✗ 文本处理功能异常: 返回无效结果")
            return False
            
    except Exception as e:
        print(f"✗ 文本处理功能测试失败: {e}")
        return False

def test_document_processor():
    """测试文档处理功能"""
    print("\n测试文档处理功能...")
    
    try:
        from document_processor import MockDocumentProcessor
        
        processor = MockDocumentProcessor()
        
        # 测试结构化内容
        test_content = {
            'title': '测试培训脚本',
            'sections': [
                {
                    'title': '培训目标',
                    'content': ['掌握基本操作方法', '了解安全注意事项']
                },
                {
                    'title': '操作步骤',
                    'content': ['第一步：检查设备', '第二步：开始操作']
                }
            ]
        }
        
        # 测试导出
        output_path = processor.export_to_docx(test_content)
        
        if output_path and os.path.exists(output_path):
            print("✓ 文档处理功能正常")
            print(f"  导出文件: {output_path}")
            
            # 清理测试文件
            os.unlink(output_path)
            return True
        else:
            print("✗ 文档处理功能异常: 文件导出失败")
            return False
            
    except Exception as e:
        print(f"✗ 文档处理功能测试失败: {e}")
        return False

def test_gui_creation():
    """测试GUI创建"""
    print("\n测试GUI创建...")
    
    try:
        import tkinter as tk
        from gui_simple import Video2ScriptGUI
        
        # 创建临时根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 创建GUI实例
        app = Video2ScriptGUI(root)
        
        print("✓ GUI创建成功")
        
        # 清理
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ GUI创建测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("Video2Script 功能测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("语音转文字", test_speech_to_text),
        ("文本处理", test_text_processor),
        ("文档处理", test_document_processor),
        ("GUI创建", test_gui_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}测试:")
        if test_func():
            passed += 1
        else:
            print(f"  {test_name}测试失败")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有测试通过！应用可以正常运行。")
        return True
    else:
        print("✗ 部分测试失败，请检查相关模块。")
        return False

if __name__ == "__main__":
    success = main()
    input("\n按回车键退出...")
    sys.exit(0 if success else 1) 