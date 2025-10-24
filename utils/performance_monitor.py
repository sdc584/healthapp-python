# -*- coding: utf-8 -*-
"""
性能监控模块
监控应用性能并提供优化建议
"""

import time
import psutil
import threading
from datetime import datetime
from kivy.clock import Clock

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.is_monitoring = False
        self.stats = {
            'cpu_usage': [],
            'memory_usage': [],
            'frame_times': [],
            'operation_times': {},
            'error_count': 0
        }
        
        # 性能阈值
        self.thresholds = {
            'cpu_warning': 70,      # CPU使用率警告阈值
            'cpu_critical': 90,     # CPU使用率严重阈值
            'memory_warning': 80,   # 内存使用率警告阈值
            'memory_critical': 95,  # 内存使用率严重阈值
            'frame_time_warning': 50,  # 帧时间警告阈值(ms)
        }
        
        self.callbacks = []
    
    def start_monitoring(self):
        """开始性能监控"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        
        # 启动监控线程
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
        
        # 启动Kivy时钟监控
        Clock.schedule_interval(self._update_frame_stats, 1.0)
        
        print("📊 性能监控已启动")
    
    def stop_monitoring(self):
        """停止性能监控"""
        self.is_monitoring = False
        Clock.unschedule(self._update_frame_stats)
        print("📊 性能监控已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.is_monitoring:
            try:
                # CPU使用率
                cpu_percent = psutil.cpu_percent(interval=1)
                self.stats['cpu_usage'].append({
                    'timestamp': datetime.now(),
                    'value': cpu_percent
                })
                
                # 内存使用率
                memory = psutil.virtual_memory()
                self.stats['memory_usage'].append({
                    'timestamp': datetime.now(),
                    'value': memory.percent
                })
                
                # 保留最近100个数据点
                if len(self.stats['cpu_usage']) > 100:
                    self.stats['cpu_usage'].pop(0)
                if len(self.stats['memory_usage']) > 100:
                    self.stats['memory_usage'].pop(0)
                
                # 检查性能阈值
                self._check_performance_thresholds(cpu_percent, memory.percent)
                
                time.sleep(5)  # 5秒采样间隔
                
            except Exception as e:
                print(f"性能监控错误: {e}")
                time.sleep(10)
    
    def _update_frame_stats(self, dt):
        """更新帧统计"""
        frame_time = dt * 1000  # 转换为毫秒
        
        self.stats['frame_times'].append({
            'timestamp': datetime.now(),
            'value': frame_time
        })
        
        # 保留最近60个帧时间
        if len(self.stats['frame_times']) > 60:
            self.stats['frame_times'].pop(0)
        
        # 检查帧时间
        if frame_time > self.thresholds['frame_time_warning']:
            self._notify_performance_issue('frame_time', frame_time)
    
    def _check_performance_thresholds(self, cpu_percent, memory_percent):
        """检查性能阈值"""
        # CPU检查
        if cpu_percent > self.thresholds['cpu_critical']:
            self._notify_performance_issue('cpu_critical', cpu_percent)
        elif cpu_percent > self.thresholds['cpu_warning']:
            self._notify_performance_issue('cpu_warning', cpu_percent)
        
        # 内存检查
        if memory_percent > self.thresholds['memory_critical']:
            self._notify_performance_issue('memory_critical', memory_percent)
        elif memory_percent > self.thresholds['memory_warning']:
            self._notify_performance_issue('memory_warning', memory_percent)
    
    def _notify_performance_issue(self, issue_type, value):
        """通知性能问题"""
        issue_info = {
            'type': issue_type,
            'value': value,
            'timestamp': datetime.now(),
            'suggestion': self._get_performance_suggestion(issue_type)
        }
        
        # 通知回调
        for callback in self.callbacks:
            try:
                callback(issue_info)
            except Exception as e:
                print(f"性能回调错误: {e}")
    
    def _get_performance_suggestion(self, issue_type):
        """获取性能优化建议"""
        suggestions = {
            'cpu_warning': "CPU使用率较高，建议关闭不必要的后台功能。",
            'cpu_critical': "CPU使用率过高，建议重启应用或设备。",
            'memory_warning': "内存使用率较高，建议清理缓存数据。",
            'memory_critical': "内存不足，建议立即重启应用。",
            'frame_time': "界面响应缓慢，建议优化显示设置。"
        }
        
        return suggestions.get(issue_type, "性能异常，建议检查设备状态。")
    
    def measure_operation_time(self, operation_name):
        """测量操作时间的装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    operation_time = (end_time - start_time) * 1000  # 毫秒
                    
                    # 记录操作时间
                    if operation_name not in self.stats['operation_times']:
                        self.stats['operation_times'][operation_name] = []
                    
                    self.stats['operation_times'][operation_name].append({
                        'timestamp': datetime.now(),
                        'duration': operation_time
                    })
                    
                    # 保留最近20个记录
                    if len(self.stats['operation_times'][operation_name]) > 20:
                        self.stats['operation_times'][operation_name].pop(0)
                    
                    # 检查慢操作
                    if operation_time > 1000:  # 超过1秒
                        self._notify_performance_issue('slow_operation', {
                            'operation': operation_name,
                            'duration': operation_time
                        })
            
            return wrapper
        return decorator
    
    def add_performance_callback(self, callback):
        """添加性能监控回调"""
        self.callbacks.append(callback)
    
    def get_performance_summary(self):
        """获取性能摘要"""
        summary = {
            'monitoring': self.is_monitoring,
            'data_points': len(self.stats['cpu_usage']),
            'current_status': 'good'
        }
        
        # 计算平均值
        if self.stats['cpu_usage']:
            recent_cpu = [s['value'] for s in self.stats['cpu_usage'][-10:]]
            summary['avg_cpu'] = sum(recent_cpu) / len(recent_cpu)
        
        if self.stats['memory_usage']:
            recent_memory = [s['value'] for s in self.stats['memory_usage'][-10:]]
            summary['avg_memory'] = sum(recent_memory) / len(recent_memory)
        
        if self.stats['frame_times']:
            recent_frames = [s['value'] for s in self.stats['frame_times'][-10:]]
            summary['avg_frame_time'] = sum(recent_frames) / len(recent_frames)
        
        # 评估整体状态
        if (summary.get('avg_cpu', 0) > self.thresholds['cpu_warning'] or
            summary.get('avg_memory', 0) > self.thresholds['memory_warning'] or
            summary.get('avg_frame_time', 0) > self.thresholds['frame_time_warning']):
            summary['current_status'] = 'warning'
        
        return summary
    
    def clear_stats(self):
        """清除统计数据"""
        self.stats = {
            'cpu_usage': [],
            'memory_usage': [],
            'frame_times': [],
            'operation_times': {},
            'error_count': 0
        }
        print("📊 性能统计数据已清除")
    
    def export_performance_report(self):
        """导出性能报告"""
        try:
            report_path = 'HealthApp_Python/logs/performance_report.txt'
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"健康追踪应用 - 性能报告\n")
                f.write(f"生成时间: {datetime.now()}\n\n")
                
                summary = self.get_performance_summary()
                f.write("性能摘要:\n")
                f.write(f"状态: {summary['current_status']}\n")
                f.write(f"平均CPU使用率: {summary.get('avg_cpu', 0):.1f}%\n")
                f.write(f"平均内存使用率: {summary.get('avg_memory', 0):.1f}%\n")
                f.write(f"平均帧时间: {summary.get('avg_frame_time', 0):.1f}ms\n\n")
                
                # 操作时间统计
                f.write("操作性能统计:\n")
                for operation, times in self.stats['operation_times'].items():
                    if times:
                        avg_time = sum(t['duration'] for t in times) / len(times)
                        f.write(f"{operation}: {avg_time:.1f}ms (平均)\n")
            
            return report_path
            
        except Exception as e:
            print(f"导出性能报告失败: {e}")
            return None



