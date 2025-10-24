# -*- coding: utf-8 -*-
"""
步数计数器服务
提供步数统计和距离估算功能（GPS信号弱时使用）
"""

import threading
import time
from datetime import datetime

class PedometerService:
    """步数计数器服务类"""
    
    def __init__(self):
        self.is_counting = False
        self.step_callback = None
        self.step_count = 0
        self.total_steps = 0
        self.last_step_time = None
        
        # Android传感器支持
        self.accelerometer = None
        self.init_android_sensors()
        
        # 步长估算参数
        self.average_step_length = 0.65  # 默认步长65cm
        self.user_height = 170  # 默认身高170cm
        
    def init_android_sensors(self):
        """初始化Android传感器"""
        try:
            from plyer import accelerometer
            self.accelerometer = accelerometer
        except ImportError:
            print("无法导入加速度计，使用模拟步数")
            self.accelerometer = None
    
    def set_user_height(self, height_cm):
        """根据用户身高设置步长"""
        self.user_height = height_cm
        # 步长通常为身高的0.37-0.45倍，这里取0.4
        self.average_step_length = height_cm * 0.004  # 转换为米
    
    def start_counting(self, callback):
        """开始计步"""
        if self.is_counting:
            return
            
        self.step_callback = callback
        self.is_counting = True
        self.step_count = 0
        self.last_step_time = datetime.now()
        
        if self.accelerometer:
            try:
                # 启用加速度计
                self.accelerometer.enable()
                
                # 启动步数检测线程
                self.detection_thread = threading.Thread(
                    target=self._step_detection_loop, 
                    daemon=True
                )
                self.detection_thread.start()
                
                print("步数计数已启动")
                
            except Exception as e:
                print(f"加速度计启动失败: {e}")
                self._start_mock_pedometer()
        else:
            # 使用模拟计步器
            self._start_mock_pedometer()
    
    def _start_mock_pedometer(self):
        """启动模拟计步器（用于测试）"""
        def mock_step_thread():
            while self.is_counting:
                # 模拟每2秒一步
                time.sleep(2)
                if self.is_counting:
                    self._on_step_detected()

        mock_thread = threading.Thread(target=mock_step_thread, daemon=True)
        mock_thread.start()
        print("模拟计步器已启动")
    
    def _step_detection_loop(self):
        """步数检测循环"""
        last_acceleration = 0
        step_threshold = 12.0  # 步数检测阈值
        step_cooldown = 0.5    # 步数冷却时间（秒）
        last_step_time = 0
        
        while self.is_counting:
            try:
                if self.accelerometer:
                    # 获取加速度数据
                    acceleration = self.accelerometer.acceleration
                    if acceleration:
                        x, y, z = acceleration
                        
                        # 计算总加速度
                        total_acceleration = (x**2 + y**2 + z**2) ** 0.5
                        
                        # 检测步数（简单的峰值检测）
                        current_time = time.time()
                        if (total_acceleration > step_threshold and 
                            total_acceleration > last_acceleration and
                            current_time - last_step_time > step_cooldown):
                            
                            self._on_step_detected()
                            last_step_time = current_time
                        
                        last_acceleration = total_acceleration
                
                time.sleep(0.1)  # 100ms采样间隔
                
            except Exception as e:
                print(f"步数检测错误: {e}")
                time.sleep(1)
    
    def _on_step_detected(self):
        """检测到步数时的回调"""
        self.step_count += 1
        self.total_steps += 1
        self.last_step_time = datetime.now()
        
        # 计算估算距离
        estimated_distance = self.step_count * self.average_step_length
        
        if self.step_callback:
            self.step_callback(self.step_count, estimated_distance)
    
    def stop_counting(self):
        """停止计步"""
        self.is_counting = False
        
        if self.accelerometer:
            try:
                self.accelerometer.disable()
                print("步数计数已停止")
            except Exception as e:
                print(f"停止计步失败: {e}")
        
        self.step_callback = None
    
    def get_current_stats(self):
        """获取当前统计数据"""
        estimated_distance = self.step_count * self.average_step_length
        
        return {
            'steps': self.step_count,
            'total_steps': self.total_steps,
            'estimated_distance': estimated_distance,
            'step_length': self.average_step_length,
            'last_step_time': self.last_step_time
        }
    
    def reset_session(self):
        """重置当前会话"""
        self.step_count = 0
        self.last_step_time = None
    
    def estimate_calories(self, steps, user_weight=60):
        """根据步数估算卡路里消耗"""
        # 简单估算：每步约0.04-0.05卡路里
        calories_per_step = 0.045 * (user_weight / 60)  # 根据体重调整
        return steps * calories_per_step
    
    def get_pace_from_steps(self, steps, time_seconds):
        """根据步数和时间计算配速"""
        if time_seconds <= 0 or steps <= 0:
            return 0
        
        distance_km = (steps * self.average_step_length) / 1000
        speed_kmh = distance_km / (time_seconds / 3600)
        
        if speed_kmh > 0:
            pace_min_per_km = 60 / speed_kmh
            return pace_min_per_km
        
        return 0
    
    def calibrate_step_length(self, actual_distance_m, steps):
        """校准步长"""
        if steps > 0:
            new_step_length = actual_distance_m / steps
            
            # 合理性检查（步长应该在0.4-1.0米之间）
            if 0.4 <= new_step_length <= 1.0:
                self.average_step_length = new_step_length
                print(f"步长已校准为: {new_step_length:.3f}米")
                return True
        
        return False
