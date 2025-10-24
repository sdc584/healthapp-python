# -*- coding: utf-8 -*-
"""
GPS定位服务
提供实时位置追踪功能
"""

import threading
import time
from datetime import datetime

class GPSService:
    """GPS定位服务类"""
    
    def __init__(self):
        self.is_tracking = False
        self.location_callback = None
        self.tracking_thread = None
        self.current_location = None
        
        # GPS状态监控
        self.gps_status = 'unknown'
        self.location_accuracy = 0
        self.last_location_time = None
        self.weak_signal_threshold = 20  # GPS精度阈值（米）
        
        # Android GPS支持
        self.gps_provider = None
        self.init_android_gps()
    
    def init_android_gps(self):
        """初始化Android GPS"""
        try:
            # 尝试导入Android GPS模块
            from android.permissions import request_permissions, Permission
            from plyer import gps
            
            # 请求位置权限
            request_permissions([
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION
            ])
            
            self.gps_provider = gps
            
        except ImportError:
            # 非Android环境，使用模拟GPS
            print("非Android环境，使用模拟GPS数据")
            self.gps_provider = None
    
    def start_tracking(self, callback):
        """开始GPS追踪"""
        if self.is_tracking:
            return
            
        self.location_callback = callback
        self.is_tracking = True
        
        if self.gps_provider:
            try:
                # 配置GPS参数
                self.gps_provider.configure(
                    on_location=self.on_location_update,
                    on_status=self.on_gps_status
                )
                
                # 启动GPS
                self.gps_provider.start(
                    minTime=1000,  # 最小更新时间（毫秒）
                    minDistance=1  # 最小更新距离（米）
                )
                
                print("GPS追踪已启动")
                
            except Exception as e:
                print(f"GPS启动失败: {e}")
                self.start_mock_gps()
        else:
            # 使用模拟GPS
            self.start_mock_gps()
    
    def start_mock_gps(self):
        """启动模拟GPS（用于测试）"""
        def mock_gps_thread():
            # 北京坐标附近
            base_lat = 39.9042
            base_lon = 116.4074
            
            step = 0
            
            while self.is_tracking:
                # 模拟移动轨迹（圆形路径）
                import math
                angle = step * 0.1
                lat = base_lat + 0.001 * math.sin(angle)
                lon = base_lon + 0.001 * math.cos(angle)
                
                self.current_location = {
                    'latitude': lat,
                    'longitude': lon,
                    'altitude': 50.0,
                    'accuracy': 5.0,
                    'timestamp': datetime.now()
                }
                
                if self.location_callback:
                    self.location_callback(lat, lon, 50.0)
                
                step += 1
                time.sleep(2)  # 2秒更新一次
        
        self.tracking_thread = threading.Thread(target=mock_gps_thread, daemon=True)
        self.tracking_thread.start()
        print("模拟GPS追踪已启动")
    
    def stop_tracking(self):
        """停止GPS追踪"""
        self.is_tracking = False
        
        if self.gps_provider:
            try:
                self.gps_provider.stop()
                print("GPS追踪已停止")
            except Exception as e:
                print(f"GPS停止失败: {e}")
        
        self.location_callback = None
        self.current_location = None
    
    def on_location_update(self, **kwargs):
        """GPS位置更新回调"""
        try:
            lat = kwargs.get('lat', 0)
            lon = kwargs.get('lon', 0)
            altitude = kwargs.get('altitude', 0)
            accuracy = kwargs.get('accuracy', 999)
            
            # 更新GPS状态
            self.location_accuracy = accuracy
            self.last_location_time = datetime.now()
            
            # 检查GPS信号强度
            if accuracy > self.weak_signal_threshold:
                self.gps_status = 'weak'
                print(f"⚠️ GPS信号弱，精度: {accuracy}米")
            else:
                self.gps_status = 'good'
            
            self.current_location = {
                'latitude': lat,
                'longitude': lon,
                'altitude': altitude,
                'accuracy': accuracy,
                'timestamp': self.last_location_time,
                'signal_status': self.gps_status
            }
            
            if self.location_callback:
                self.location_callback(lat, lon, altitude, accuracy, self.gps_status)
                
        except Exception as e:
            print(f"GPS位置更新失败: {e}")
    
    def on_gps_status(self, stype, status):
        """GPS状态回调"""
        print(f"GPS状态: {stype} = {status}")
        
        # 更新GPS状态
        if stype == 'provider-enabled':
            if status:
                self.gps_status = 'enabled'
            else:
                self.gps_status = 'disabled'
        elif stype == 'provider-status':
            if status == 'available':
                self.gps_status = 'available'
            elif status == 'out-of-service':
                self.gps_status = 'unavailable'
    
    def get_current_location(self):
        """获取当前位置"""
        return self.current_location
    
    def is_gps_enabled(self):
        """检查GPS是否可用"""
        if self.gps_provider:
            try:
                # 检查GPS状态
                return True  # 简化实现
            except:
                return False
        return False  # 模拟模式始终可用
    
    def get_gps_status(self):
        """获取GPS状态信息"""
        return {
            'status': self.gps_status,
            'accuracy': self.location_accuracy,
            'last_update': self.last_location_time,
            'is_weak_signal': self.location_accuracy > self.weak_signal_threshold
        }
    
    def is_signal_weak(self):
        """检查GPS信号是否弱"""
        return (self.location_accuracy > self.weak_signal_threshold or 
                self.gps_status in ['weak', 'unavailable', 'disabled'])
