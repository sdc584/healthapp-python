# -*- coding: utf-8 -*-
"""
错误处理和日志管理模块
提供统一的错误处理和用户反馈机制
"""

import traceback
import logging
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class ErrorHandler:
    """统一错误处理器"""
    
    def __init__(self):
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='HealthApp_Python/logs/app.log'
        )
        self.logger = logging.getLogger('HealthApp')
        
        # 错误统计
        self.error_count = 0
        self.recent_errors = []
    
    def handle_error(self, error, context="", show_user_dialog=True, critical=False):
        """处理错误"""
        error_info = {
            'timestamp': datetime.now(),
            'error': str(error),
            'context': context,
            'traceback': traceback.format_exc(),
            'critical': critical
        }
        
        # 记录错误
        self.error_count += 1
        self.recent_errors.append(error_info)
        
        # 保留最近20个错误
        if len(self.recent_errors) > 20:
            self.recent_errors.pop(0)
        
        # 日志记录
        if critical:
            self.logger.critical(
            f"严重错误 - {context}: {error}\n{traceback.format_exc()}"
        )
        else:
            self.logger.error(f"错误 - {context}: {error}")
        
        # 显示用户对话框
        if show_user_dialog:
            self.show_error_dialog(error_info)
        
        return error_info
    
    def show_error_dialog(self, error_info):
        """显示错误对话框"""
        error_type = "严重错误" if error_info['critical'] else "错误"
        
        popup = Popup(
            title=f'⚠️ {error_type}',
            size_hint=(0.8, 0.6)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # 错误描述
        if error_info['critical']:
            error_text = (f"应用遇到严重问题：\n\n{error_info['context']}\n\n"
                         "建议重启应用或联系支持。")
        else:
            friendly_msg = self.get_user_friendly_message(error_info['error'])
            error_text = (f"操作失败：\n\n{error_info['context']}\n\n"
                         f"{friendly_msg}")
        
        error_label = Label(
            text=error_text,
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        content.add_widget(error_label)
        
        # 按钮
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)
        
        if error_info['critical']:
            restart_btn = Button(text='重启应用', background_color=[1, 0.3, 0.3, 1])
            restart_btn.bind(on_press=lambda x: self.restart_app())
            btn_layout.add_widget(restart_btn)
        
        retry_btn = Button(text='重试', background_color=[0, 0.8, 1, 1])
        retry_btn.bind(on_press=popup.dismiss)
        btn_layout.add_widget(retry_btn)
        
        close_btn = Button(text='关闭')
        close_btn.bind(on_press=popup.dismiss)
        btn_layout.add_widget(close_btn)
        
        content.add_widget(btn_layout)
        popup.content = content
        popup.open()
    
    def get_user_friendly_message(self, error_str):
        """获取用户友好的错误信息"""
        error_lower = error_str.lower()
        
        if 'network' in error_lower or 'connection' in error_lower:
            return "网络连接问题，请检查网络设置。"
        elif 'permission' in error_lower:
            return "权限不足，请在设置中授予必要权限。"
        elif 'gps' in error_lower or 'location' in error_lower:
            return "定位服务问题，请检查GPS设置。"
        elif 'camera' in error_lower:
            return "相机访问问题，请检查相机权限。"
        elif 'storage' in error_lower or 'file' in error_lower:
            return "存储访问问题，请检查存储权限。"
        elif 'timeout' in error_lower:
            return "操作超时，请重试。"
        else:
            return "操作失败，请稍后重试。"
    
    def restart_app(self):
        """重启应用"""
        try:
            import os
            import sys
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            self.logger.critical(f"重启应用失败: {e}")
    
    def log_info(self, message, context=""):
        """记录信息"""
        self.logger.info(f"{context}: {message}" if context else message)
    
    def log_warning(self, message, context=""):
        """记录警告"""
        self.logger.warning(f"{context}: {message}" if context else message)
    
    def get_error_stats(self):
        """获取错误统计"""
        return {
            'total_errors': self.error_count,
            'recent_errors': len(self.recent_errors),
            'critical_errors': len([e for e in self.recent_errors if e['critical']])
        }
    
    def export_error_report(self):
        """导出错误报告"""
        try:
            report_path = 'HealthApp_Python/logs/error_report.txt'
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"健康追踪应用 - 错误报告\n")
                f.write(f"生成时间: {datetime.now()}\n")
                f.write(f"总错误数: {self.error_count}\n\n")
                
                f.write("最近错误详情:\n")
                f.write("=" * 50 + "\n")
                
                for i, error in enumerate(self.recent_errors[-10:], 1):
                    f.write(f"\n错误 #{i}:\n")
                    f.write(f"时间: {error['timestamp']}\n")
                    f.write(f"上下文: {error['context']}\n")
                    f.write(f"错误: {error['error']}\n")
                    f.write(f"严重: {'是' if error['critical'] else '否'}\n")
                    f.write(f"跟踪:\n{error['traceback']}\n")
                    f.write("-" * 30 + "\n")
            
            return report_path
            
        except Exception as e:
            self.logger.error(f"导出错误报告失败: {e}")
            return None

class NetworkErrorHandler(ErrorHandler):
    """网络错误专用处理器"""
    
    def handle_network_error(self, error, operation="网络操作"):
        """处理网络相关错误"""
        if "timeout" in str(error).lower():
            message = f"{operation}超时，请检查网络连接或稍后重试。"
        elif "connection" in str(error).lower():
            message = f"网络连接失败，请检查网络设置。"
        elif "dns" in str(error).lower():
            message = f"域名解析失败，请检查网络连接。"
        else:
            message = f"{operation}失败，请检查网络连接。"
        
        return self.handle_error(error, message, show_user_dialog=True)

class GPSErrorHandler(ErrorHandler):
    """GPS错误专用处理器"""
    
    def handle_gps_error(self, error, operation="GPS操作"):
        """处理GPS相关错误"""
        if "permission" in str(error).lower():
            message = f"需要位置权限才能使用GPS功能，请在设置中授权。"
        elif "unavailable" in str(error).lower():
            message = f"GPS服务不可用，请检查定位设置。"
        elif "timeout" in str(error).lower():
            message = f"GPS定位超时，建议移动到空旷地区。"
        else:
            message = f"GPS {operation}失败，请检查定位设置。"
        
        return self.handle_error(error, message, show_user_dialog=True)
