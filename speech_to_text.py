import os
import tempfile
import requests
import json
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import config

class SpeechToText:
    def __init__(self):
        self.api_key = config.DEEPSEEK_API_KEY
        self.api_base = config.DEEPSEEK_API_BASE
        
    def extract_audio_from_video(self, video_path):
        """从视频文件中提取音频"""
        try:
            # 创建临时文件
            temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_audio_path = temp_audio.name
            temp_audio.close()
            
            # 使用moviepy提取音频
            video = VideoFileClip(video_path)
            audio = video.audio
            
            # 保存音频文件
            audio.write_audiofile(temp_audio_path, 
                                fps=config.AUDIO_SAMPLE_RATE,
                                nbytes=2,
                                codec='pcm_s16le')
            
            video.close()
            audio.close()
            
            return temp_audio_path
            
        except Exception as e:
            raise Exception(f"音频提取失败: {str(e)}")
    
    def convert_audio_to_text(self, audio_path):
        """使用DeepSeek API将音频转换为文字"""
        try:
            # 读取音频文件
            with open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # 准备API请求
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'multipart/form-data'
            }
            
            files = {
                'file': ('audio.wav', audio_data, 'audio/wav'),
                'model': (None, 'deepseek-whisper'),
                'language': (None, 'zh'),
                'response_format': (None, 'json')
            }
            
            # 发送请求到DeepSeek API
            response = requests.post(
                f"{self.api_base}/v1/audio/transcriptions",
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('text', '')
            else:
                raise Exception(f"API请求失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            raise Exception(f"语音转文字失败: {str(e)}")
        finally:
            # 清理临时文件
            if os.path.exists(audio_path):
                os.unlink(audio_path)
    
    def process_video(self, video_path):
        """处理视频文件，返回转换的文字"""
        print("正在提取音频...")
        audio_path = self.extract_audio_from_video(video_path)
        
        print("正在进行语音识别...")
        text = self.convert_audio_to_text(audio_path)
        
        return text

class MockSpeechToText:
    """模拟语音转文字类，用于测试"""
    def __init__(self):
        pass
    
    def process_video(self, video_path):
        """模拟处理视频文件"""
        # 返回模拟的转换结果
        return """
        欢迎来到技能操作培训课程。今天我们将学习如何正确使用这个设备。
        
        首先，让我们了解一下设备的基本组成部分。设备主要由三个部分组成：
        第一部分是控制面板，第二部分是操作区域，第三部分是安全装置。
        
        在开始操作之前，请确保您已经穿戴好必要的安全装备，包括安全帽、
        防护眼镜和防护手套。
        
        接下来，我们将进行实际操作演示。请跟随我的步骤进行操作。
        
        第一步，打开电源开关。电源开关位于设备的右侧，请轻轻按下开关按钮。
        
        第二步，检查设备状态指示灯。绿色指示灯表示设备正常运行，
        红色指示灯表示需要检查设备状态。
        
        第三步，设置操作参数。根据您的工作需求，调整相应的参数设置。
        
        操作完成后，请按照正确的顺序关闭设备，并清理工作区域。
        
        以上就是本次培训的全部内容，感谢您的参与。
        """ 