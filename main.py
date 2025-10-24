# -*- coding: utf-8 -*-
"""
健康追踪应用 - 主程序
使用Kivy框架开发跨平台移动应用
核心功能：跑步追踪 + 饮食记录
"""

import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from chinese_config import setup_chinese_display
from ui_helpers import patch_kivy_defaults
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
import threading

# 导入自定义模块
from screens.run_screen import RunScreen
from screens.food_screen import FoodScreen
from screens.today_screen import TodayScreen
from screens.history_screen import HistoryScreen
from screens.profile_screen import ProfileScreen
from services.gps_service import GPSService
from services.food_api_service import FoodAPIService
from services.firebase_service import FirebaseService
from services.pedometer_service import PedometerService
from services.camera_service import CameraService
from utils.storage_manager import StorageManager
from utils.error_handler import ErrorHandler, NetworkErrorHandler, GPSErrorHandler
from utils.performance_monitor import PerformanceMonitor

class BottomNavigation(BoxLayout):
    """底部导航栏"""
    
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1
        self.screen_manager = screen_manager
        
        # 导航按钮
        nav_buttons = [
            ('跑步', 'run_screen'),
            ('饮食', 'food_screen'), 
            ('今日', 'today_screen'),
            ('历史', 'history_screen'),
            ('资料', 'profile_screen')
        ]
        
        for text, screen_name in nav_buttons:
            btn = Button(
                text=text,
                size_hint_x=0.2,
                background_color=[0.2, 0.6, 1, 1]
            ,
            font_name='Chinese'
        )
            btn.bind(on_press=lambda x, name=screen_name: self.switch_screen(name))
            self.add_widget(btn)
    
    def switch_screen(self, screen_name):
        """切换屏幕"""
        self.screen_manager.current = screen_name

class MainLayout(BoxLayout):
    """主布局"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # 创建屏幕管理器
        self.screen_manager = ScreenManager()
        
        # 添加各个屏幕
        self.screen_manager.add_widget(RunScreen(name='run_screen'))
        self.screen_manager.add_widget(FoodScreen(name='food_screen'))
        self.screen_manager.add_widget(TodayScreen(name='today_screen'))
        self.screen_manager.add_widget(HistoryScreen(name='history_screen'))
        self.screen_manager.add_widget(ProfileScreen(name='profile_screen'))
        
        # 设置默认屏幕
        self.screen_manager.current = 'run_screen'
        
        # 添加到布局
        self.add_widget(self.screen_manager)
        self.add_widget(BottomNavigation(self.screen_manager))

class HealthApp(App):
    """健康追踪应用主类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "健康追踪应用"
        
        # 配置中文显示
        setup_chinese_display()
        
        # 应用UI组件中文字体补丁
        patch_kivy_defaults()
        
        # 初始化服务
        self.storage = StorageManager()
        self.gps_service = GPSService()
        self.food_api = FoodAPIService()
        self.firebase = FirebaseService()
        self.pedometer_service = PedometerService()
        self.camera_service = CameraService()
        
        # 错误处理器
        self.error_handler = ErrorHandler()
        self.network_error_handler = NetworkErrorHandler()
        self.gps_error_handler = GPSErrorHandler()
        
        # 性能监控器
        self.performance_monitor = PerformanceMonitor()
        self.performance_monitor.add_performance_callback(self.on_performance_issue)
        
        # 应用数据
        self.user_data = {}
        self.current_run = None
        self.daily_nutrition = {
            'calories': 0,
            'protein': 0, 
            'carbs': 0,
            'fat': 0
        }
    
    def build(self):
        """构建应用界面"""
        # 请求权限
        self.request_permissions()
        
        # 初始化数据
        self.load_user_data()
        
        # 启动性能监控
        self.performance_monitor.start_monitoring()
        
        # 返回主布局
        return MainLayout()
    
    
    def request_permissions(self):
        """请求必要权限"""
        try:
            # 在Android上请求权限
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
                Permission.CAMERA,
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.ACTIVITY_RECOGNITION  # 步数计数权限
            ])
            
            self.error_handler.log_info("权限请求完成", "应用启动")
            
        except ImportError:
            # 非Android环境，跳过权限请求
            self.error_handler.log_info("非Android环境，跳过权限请求", "应用启动")
        except Exception as e:
            self.error_handler.handle_error(e, "请求应用权限时出错")
    
    def load_user_data(self):
        """加载用户数据"""
        try:
            self.user_data = self.storage.load_user_data()
            self.daily_nutrition = self.storage.load_daily_nutrition()
            self.error_handler.log_info("用户数据加载成功", "数据初始化")
            
        except Exception as e:
            self.error_handler.handle_error(e, "加载用户数据失败，使用默认设置", show_user_dialog=False)
            
            # 设置默认用户数据
            self.user_data = {
                'name': '用户',
                'height': 170,
                'weight': 60,
                'daily_calorie_goal': 2000
            }
            self.daily_nutrition = {
                'calories': 0,
                'protein': 0, 
                'carbs': 0,
                'fat': 0
            }
    
    def save_user_data(self):
        """保存用户数据"""
        try:
            self.storage.save_user_data(self.user_data)
            self.storage.save_daily_nutrition(self.daily_nutrition)
        except Exception as e:
            print(f"保存用户数据失败: {e}")
    
    def on_pause(self):
        """应用暂停时保存数据"""
        self.save_user_data()
        return True
    
    def on_stop(self):
        """应用停止时清理资源"""
        self.save_user_data()
        if self.gps_service:
            self.gps_service.stop_tracking()
    
    def on_performance_issue(self, issue_info):
        """性能问题回调处理"""
        try:
            issue_type = issue_info['type']
            value = issue_info['value']
            suggestion = issue_info['suggestion']
            
            # 记录性能问题
            self.error_handler.log_warning(f"性能问题: {issue_type} = {value}", "性能监控")
            
            # 根据问题类型采取相应措施
            if issue_type in ['cpu_critical', 'memory_critical']:
                # 严重性能问题，显示警告
                from kivy.uix.popup import Popup
                from kivy.uix.label import Label
                from kivy.uix.button import Button
                from kivy.uix.boxlayout import BoxLayout
                
                popup = Popup(
                    title='⚠️ 性能警告',
                    size_hint=(0.8, 0.5)
                )
                
                content = BoxLayout(orientation='vertical', spacing=10, padding=10)
                content.add_widget(Label(text=suggestion,
            font_name='Chinese'
        ))
                
                btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3, spacing=10)
                
                optimize_btn = Button(text='立即优化',
            font_name='Chinese'
        )
                optimize_btn.bind(on_press=lambda x: [self.optimize_performance(), popup.dismiss()])
                btn_layout.add_widget(optimize_btn)
                
                close_btn = Button(text='忽略',
            font_name='Chinese'
        )
                close_btn.bind(on_press=popup.dismiss)
                btn_layout.add_widget(close_btn)
                
                content.add_widget(btn_layout)
                popup.content = content
                popup.open()
                
        except Exception as e:
            print(f"处理性能问题回调失败: {e}")
    
    def optimize_performance(self):
        """执行性能优化"""
        try:
            # 清理缓存
            if hasattr(self, 'food_api'):
                self.food_api.cache.clear()
                
            # 清理存储管理器缓存
            if hasattr(self.storage, 'cache'):
                self.storage.cache.clear()
                
            # 停止不必要的后台任务
            if hasattr(self, 'firebase') and self.firebase.sync_queue:
                # 暂停同步队列处理
                self.firebase.pause_sync = True
                
            self.error_handler.log_info("性能优化完成", "系统优化")
            
        except Exception as e:
            self.error_handler.handle_error(e, "性能优化失败", show_user_dialog=False)
    
    def export_final_reports(self):
        """导出最终报告"""
        try:
            # 导出错误报告
            error_report_path = self.error_handler.export_error_report()
            if error_report_path:
                print(f"错误报告已导出: {error_report_path}")
                
            # 导出性能报告
            perf_report_path = self.performance_monitor.export_performance_report()
            if perf_report_path:
                print(f"性能报告已导出: {perf_report_path}")
                
        except Exception as e:
            print(f"导出报告失败: {e}")

if __name__ == '__main__':
    HealthApp().run()
