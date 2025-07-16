import re
import requests
import json
import config

class TextProcessor:
    def __init__(self):
        self.api_key = config.DEEPSEEK_API_KEY
        self.api_base = config.DEEPSEEK_API_BASE
        
    def optimize_text(self, raw_text):
        """使用DeepSeek API优化文本内容"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt = f"""
            请对以下培训视频的文字内容进行优化，使其更加规范、清晰和专业：
            
            原文：
            {raw_text}
            
            要求：
            1. 保持原意不变
            2. 修正语法错误和表达不清的地方
            3. 使用更专业的培训术语
            4. 保持逻辑清晰，结构合理
            5. 确保内容适合作为培训脚本使用
            
            请直接返回优化后的文本，不要添加其他说明。
            """
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 4000
            }
            
            response = requests.post(
                f"{self.api_base}/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                optimized_text = result['choices'][0]['message']['content']
                return optimized_text
            else:
                # 如果API调用失败，返回原文
                print(f"文本优化API调用失败: {response.status_code}")
                return raw_text
                
        except Exception as e:
            print(f"文本优化失败: {str(e)}")
            return raw_text
    
    def segment_text(self, text):
        """将文本分段处理"""
        # 按句号、问号、感叹号分割
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # 按段落长度和语义进行分组
        segments = []
        current_segment = ""
        
        for sentence in sentences:
            if len(current_segment) + len(sentence) < config.MAX_TEXT_LENGTH:
                current_segment += sentence + "。"
            else:
                if current_segment:
                    segments.append(current_segment.strip())
                current_segment = sentence + "。"
        
        if current_segment:
            segments.append(current_segment.strip())
        
        return segments
    
    def analyze_structure(self, text):
        """分析文本结构，识别章节"""
        # 常见的章节关键词
        chapter_keywords = [
            '第一部分', '第二部分', '第三部分',
            '第一步', '第二步', '第三步',
            '首先', '其次', '然后', '最后',
            '培训目标', '操作步骤', '注意事项', '总结',
            '设备介绍', '安全要求', '操作流程', '维护保养'
        ]
        
        segments = self.segment_text(text)
        structured_content = {
            'title': '技能操作培训脚本',
            'sections': []
        }
        
        current_section = {
            'title': '主要内容',
            'content': []
        }
        
        for segment in segments:
            # 检查是否包含章节关键词
            is_new_section = False
            section_title = None
            
            for keyword in chapter_keywords:
                if keyword in segment[:50]:  # 只检查前50个字符
                    is_new_section = True
                    section_title = keyword
                    break
            
            if is_new_section and current_section['content']:
                structured_content['sections'].append(current_section)
                current_section = {
                    'title': section_title,
                    'content': [segment]
                }
            else:
                current_section['content'].append(segment)
        
        if current_section['content']:
            structured_content['sections'].append(current_section)
        
        return structured_content
    
    def process_text(self, raw_text):
        """完整的文本处理流程"""
        print("正在进行文本优化...")
        optimized_text = self.optimize_text(raw_text)
        
        print("正在分析文本结构...")
        structured_content = self.analyze_structure(optimized_text)
        
        return structured_content

class MockTextProcessor:
    """模拟文本处理器，用于测试"""
    def __init__(self):
        pass
    
    def process_text(self, raw_text):
        """模拟文本处理"""
        # 模拟优化后的结构化内容
        return {
            'title': '技能操作培训脚本',
            'sections': [
                {
                    'title': '培训目标',
                    'content': [
                        '通过本次培训，学员将掌握设备的基本操作方法和安全注意事项。',
                        '了解设备的主要组成部分和功能特点。'
                    ]
                },
                {
                    'title': '设备介绍',
                    'content': [
                        '设备主要由三个部分组成：控制面板、操作区域和安全装置。',
                        '控制面板位于设备正面，包含各种操作按钮和状态指示灯。',
                        '操作区域是进行实际工作的区域，需要特别注意安全。'
                    ]
                },
                {
                    'title': '安全要求',
                    'content': [
                        '操作前必须穿戴安全帽、防护眼镜和防护手套。',
                        '确保工作区域清洁，无杂物阻碍操作。',
                        '严格按照操作规程执行，不得违规操作。'
                    ]
                },
                {
                    'title': '操作步骤',
                    'content': [
                        '第一步：打开电源开关，检查设备状态指示灯。',
                        '第二步：根据工作需求设置操作参数。',
                        '第三步：按照标准流程进行操作。',
                        '第四步：操作完成后，按正确顺序关闭设备。'
                    ]
                },
                {
                    'title': '注意事项',
                    'content': [
                        '操作过程中如发现异常，立即停止操作并报告。',
                        '定期检查设备状态，确保设备正常运行。',
                        '保持工作区域整洁，及时清理杂物。'
                    ]
                },
                {
                    'title': '总结',
                    'content': [
                        '本次培训介绍了设备的基本操作方法和安全要求。',
                        '请学员在实际工作中严格按照培训内容执行。',
                        '如有疑问，请及时咨询相关技术人员。'
                    ]
                }
            ]
        } 