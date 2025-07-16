import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import config
from speech_to_text import MockSpeechToText
from text_processor import MockTextProcessor
from document_processor import MockDocumentProcessor

class Video2ScriptGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(config.APP_TITLE)
        self.root.geometry("1000x700")
        
        # 初始化处理器
        self.speech_to_text = MockSpeechToText()
        self.text_processor = MockTextProcessor()
        self.document_processor = MockDocumentProcessor()
        
        # 文件路径
        self.video_path = None
        self.template_path = None
        self.structured_content = None
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text=config.APP_TITLE, 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 文件选择区域
        self.create_file_selection_area(main_frame)
        
        # 处理按钮区域
        self.create_processing_area(main_frame)
        
        # 内容显示区域
        self.create_content_area(main_frame)
        
        # 导出按钮区域
        self.create_export_area(main_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
    
    def create_file_selection_area(self, parent):
        """创建文件选择区域"""
        file_frame = ttk.LabelFrame(parent, text="文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 视频文件选择
        video_frame = ttk.Frame(file_frame)
        video_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(video_frame, text="视频文件:").pack(side=tk.LEFT)
        
        self.video_path_var = tk.StringVar()
        self.video_entry = ttk.Entry(video_frame, textvariable=self.video_path_var, state="readonly")
        self.video_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5))
        
        self.video_button = ttk.Button(video_frame, text="选择视频", command=self.select_video)
        self.video_button.pack(side=tk.RIGHT)
        
        # 模板文件选择
        template_frame = ttk.Frame(file_frame)
        template_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(template_frame, text="文档模板:").pack(side=tk.LEFT)
        
        self.template_path_var = tk.StringVar()
        self.template_entry = ttk.Entry(template_frame, textvariable=self.template_path_var, state="readonly")
        self.template_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5))
        
        self.template_button = ttk.Button(template_frame, text="选择模板", command=self.select_template)
        self.template_button.pack(side=tk.RIGHT)
    
    def create_processing_area(self, parent):
        """创建处理按钮区域"""
        processing_frame = ttk.LabelFrame(parent, text="处理操作", padding="10")
        processing_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.process_button = ttk.Button(processing_frame, text="开始处理", 
                                        command=self.start_processing)
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        self.progress = ttk.Progressbar(processing_frame, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def create_content_area(self, parent):
        """创建内容显示区域"""
        content_frame = ttk.LabelFrame(parent, text="脚本内容", padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 创建Notebook用于标签页
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 原始文本标签页
        self.raw_text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.raw_text_frame, text="原始文本")
        
        self.raw_text = scrolledtext.ScrolledText(self.raw_text_frame, wrap=tk.WORD)
        self.raw_text.pack(fill=tk.BOTH, expand=True)
        
        # 优化文本标签页
        self.optimized_text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.optimized_text_frame, text="优化文本")
        
        self.optimized_text = scrolledtext.ScrolledText(self.optimized_text_frame, wrap=tk.WORD)
        self.optimized_text.pack(fill=tk.BOTH, expand=True)
        
        # 结构化内容标签页
        self.structured_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.structured_frame, text="结构化内容")
        
        self.structured_text = scrolledtext.ScrolledText(self.structured_frame, wrap=tk.WORD)
        self.structured_text.pack(fill=tk.BOTH, expand=True)
    
    def create_export_area(self, parent):
        """创建导出按钮区域"""
        export_frame = ttk.LabelFrame(parent, text="导出操作", padding="10")
        export_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.export_button = ttk.Button(export_frame, text="导出脚本", 
                                       command=self.export_script, state="disabled")
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        self.save_content_button = ttk.Button(export_frame, text="保存内容", 
                                             command=self.save_content, state="disabled")
        self.save_content_button.pack(side=tk.LEFT, padx=5)
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X)
    
    def select_video(self):
        """选择视频文件"""
        filetypes = [
            ("视频文件", "*.mp4 *.mov *.avi *.mkv"),
            ("MP4文件", "*.mp4"),
            ("MOV文件", "*.mov"),
            ("所有文件", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=filetypes
        )
        
        if filename:
            self.video_path = filename
            self.video_path_var.set(filename)
            self.status_var.set(f"已选择视频文件: {os.path.basename(filename)}")
    
    def select_template(self):
        """选择文档模板"""
        filetypes = [
            ("Word文档", "*.docx *.doc"),
            ("DOCX文件", "*.docx"),
            ("DOC文件", "*.doc"),
            ("所有文件", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="选择文档模板",
            filetypes=filetypes
        )
        
        if filename:
            self.template_path = filename
            self.template_path_var.set(filename)
            self.status_var.set(f"已选择模板文件: {os.path.basename(filename)}")
    
    def start_processing(self):
        """开始处理视频"""
        if not self.video_path:
            messagebox.showerror("错误", "请先选择视频文件")
            return
        
        # 禁用按钮
        self.process_button.config(state="disabled")
        self.progress.start()
        self.status_var.set("正在处理视频...")
        
        # 在新线程中处理
        thread = threading.Thread(target=self.process_video_thread)
        thread.daemon = True
        thread.start()
    
    def process_video_thread(self):
        """在新线程中处理视频"""
        try:
            # 语音转文字
            self.status_var.set("正在提取音频...")
            raw_text = self.speech_to_text.process_video(self.video_path)
            
            # 更新原始文本
            self.root.after(0, lambda: self.raw_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.raw_text.insert(1.0, raw_text))
            
            # 文本处理
            self.status_var.set("正在优化文本...")
            self.structured_content = self.text_processor.process_text(raw_text)
            
            # 更新优化文本
            optimized_text = self.format_structured_content(self.structured_content)
            self.root.after(0, lambda: self.optimized_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.optimized_text.insert(1.0, optimized_text))
            
            # 更新结构化文本
            structured_text = self.format_structured_content_detailed(self.structured_content)
            self.root.after(0, lambda: self.structured_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.structured_text.insert(1.0, structured_text))
            
            # 启用导出按钮
            self.root.after(0, lambda: self.export_button.config(state="normal"))
            self.root.after(0, lambda: self.save_content_button.config(state="normal"))
            
            self.root.after(0, lambda: self.status_var.set("处理完成"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("处理失败"))
        
        finally:
            # 恢复按钮状态
            self.root.after(0, lambda: self.process_button.config(state="normal"))
            self.root.after(0, lambda: self.progress.stop())
    
    def format_structured_content(self, content):
        """格式化结构化内容为文本"""
        if not content:
            return ""
        
        text = f"{content['title']}\n\n"
        
        for section in content['sections']:
            text += f"{section['title']}\n"
            for item in section['content']:
                text += f"  {item}\n"
            text += "\n"
        
        return text
    
    def format_structured_content_detailed(self, content):
        """格式化结构化内容为详细文本"""
        if not content:
            return ""
        
        text = f"文档标题: {content['title']}\n"
        text += "=" * 50 + "\n\n"
        
        for i, section in enumerate(content['sections'], 1):
            text += f"第{i}章: {section['title']}\n"
            text += "-" * 30 + "\n"
            for j, item in enumerate(section['content'], 1):
                text += f"{j}. {item}\n"
            text += "\n"
        
        return text
    
    def export_script(self):
        """导出脚本"""
        if not self.structured_content:
            messagebox.showerror("错误", "没有可导出的内容")
            return
        
        try:
            output_path = self.document_processor.export_to_docx(
                self.structured_content, 
                self.template_path
            )
            
            if output_path:
                messagebox.showinfo("成功", f"脚本已导出到:\n{output_path}")
                self.status_var.set("导出完成")
            else:
                messagebox.showerror("错误", "导出失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def save_content(self):
        """保存内容"""
        if not self.structured_content:
            messagebox.showerror("错误", "没有可保存的内容")
            return
        
        try:
            output_path = self.document_processor.save_structured_content(self.structured_content)
            
            if output_path:
                messagebox.showinfo("成功", f"内容已保存到:\n{output_path}")
                self.status_var.set("保存完成")
            else:
                messagebox.showerror("错误", "保存失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")

def main():
    """主函数"""
    root = tk.Tk()
    app = Video2ScriptGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 