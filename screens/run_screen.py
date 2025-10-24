# -*- coding: utf-8 -*-
"""
跑步追踪屏幕
实现GPS追踪、实时数据显示、地图轨迹功能
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import Line, Color, Ellipse
from kivy.uix.widget import Widget
from kivy.app import App
from datetime import datetime
import math

class MapWidget(Widget):
    """地图显示组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.route_points = []
        self.current_location = None
        
    def update_location(self, lat, lon):
        """更新当前位置"""
        self.current_location = (lat, lon)
        self.route_points.append((lat, lon))
        self.draw_route()
        
    def draw_route(self):
        """绘制跑步路线"""
        self.canvas.clear()
        
        if len(self.route_points) < 2:
            return
            
        with self.canvas:
            # 绘制路线
            Color(0, 1, 0, 1)  # 绿色路线
            points = []
            
            # 将GPS坐标转换为屏幕坐标
            for lat, lon in self.route_points:
                x, y = self.gps_to_screen(lat, lon)
                points.extend([x, y])
            
            if len(points) >= 4:
                Line(points=points, width=3)
            
            # 绘制当前位置
            if self.current_location:
                Color(1, 0, 0, 1)  # 红色当前位置
                x, y = self.gps_to_screen(*self.current_location)
                Ellipse(pos=(x-5, y-5), size=(10, 10))
    
    def gps_to_screen(self, lat, lon):
        """GPS坐标转屏幕坐标（简化实现）"""
        # 这里是简化的坐标转换，实际应用需要更复杂的地图投影
        if not self.route_points:
            return self.center_x, self.center_y
            
        # 计算相对于第一个点的偏移
        first_lat, first_lon = self.route_points[0]
        
        # 简单的线性映射
        lat_offset = (lat - first_lat) * 100000  # 放大倍数
        lon_offset = (lon - first_lon) * 100000
        
        x = self.center_x + lon_offset
        y = self.center_y + lat_offset
        
        return x, y
    
    def clear_route(self):
        """清除路线"""
        self.route_points = []
        self.current_location = None
        self.canvas.clear()

class RunScreen(Screen):
    """跑步追踪主屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 跑步状态
        self.is_running = False
        self.is_paused = False
        self.start_time = None
        self.pause_time = 0
        self.total_distance = 0
        self.current_speed = 0
        self.average_speed = 0
        
        # GPS数据
        self.last_location = None
        self.locations_history = []
        self.gps_status = 'unknown'
        self.location_accuracy = 999
        
        # 步数计数器（GPS信号弱时使用）
        self.use_pedometer = False
        self.step_count = 0
        self.pedometer_distance = 0
        
        # 状态指示器
        self.gps_status_label = None
        
        # 计时器
        self.timer_event = None
        
        self.build_ui()
    
    def build_ui(self):
        """构建用户界面"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题和状态
        title_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        
        title = Label(
            text='跑步追踪',
            font_size='24sp',
            color=[1, 1, 1, 1],
            size_hint_x=0.7,
            font_name='Chinese'
        )
        title_layout.add_widget(title)
        
        # GPS状态指示器
        self.gps_status_label = Label(
            text='GPS: 未知',
            font_size='14sp',
            color=[1, 1, 0, 1],
            size_hint_x=0.3
        ,
            font_name='Chinese'
        )
        title_layout.add_widget(self.gps_status_label)
        
        main_layout.add_widget(title_layout)
        
        # 数据显示区域
        stats_layout = GridLayout(cols=2, size_hint_y=0.3, spacing=10)
        
        # 距离显示
        self.distance_label = Label(
            text='距离: 0.00 km',
            font_size='18sp',
            color=[1, 1, 1, 1]
        ,
            font_name='Chinese'
        )
        stats_layout.add_widget(self.distance_label)
        
        # 时间显示
        self.time_label = Label(
            text='时间: 00:00:00',
            font_size='18sp',
            color=[1, 1, 1, 1]
        ,
            font_name='Chinese'
        )
        stats_layout.add_widget(self.time_label)
        
        # 当前配速
        self.pace_label = Label(
            text='配速: 0\'00"/km',
            font_size='18sp',
            color=[1, 1, 1, 1]
        ,
            font_name='Chinese'
        )
        stats_layout.add_widget(self.pace_label)
        
        # 平均配速
        self.avg_pace_label = Label(
            text='平均: 0\'00"/km',
            font_size='18sp',
            color=[1, 1, 1, 1]
        ,
            font_name='Chinese'
        )
        stats_layout.add_widget(self.avg_pace_label)
        
        # 步数显示（GPS信号弱时显示）
        self.steps_label = Label(
            text='步数: 0',
            font_size='16sp',
            color=[0.8, 0.8, 1, 1]
        ,
            font_name='Chinese'
        )
        stats_layout.add_widget(self.steps_label)
        
        # 数据源指示器
        self.source_label = Label(
            text='数据源: GPS',
            font_size='12sp',
            color=[0.7, 0.7, 0.7, 1]
        ,
            font_name='Chinese'
        )
        stats_layout.add_widget(self.source_label)
        
        main_layout.add_widget(stats_layout)
        
        # 地图显示
        self.map_widget = MapWidget(size_hint_y=0.4)
        main_layout.add_widget(self.map_widget)
        
        # 控制按钮
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)
        
        # 开始/暂停按钮
        self.start_button = Button(
            text='开始跑步',
            background_color=[0, 1, 0, 1],
            font_size='18sp'
        ,
            font_name='Chinese'
        )
        self.start_button.bind(on_press=self.toggle_running)
        button_layout.add_widget(self.start_button)
        
        # 停止按钮
        self.stop_button = Button(
            text='停止',
            background_color=[1, 0, 0, 1],
            font_size='18sp',
            disabled=True
        ,
            font_name='Chinese'
        )
        self.stop_button.bind(on_press=self.stop_running)
        button_layout.add_widget(self.stop_button)
        
        main_layout.add_widget(button_layout)
        self.add_widget(main_layout)
    
    def toggle_running(self, instance):
        """切换跑步状态"""
        if not self.is_running:
            self.start_running()
        else:
            if self.is_paused:
                self.resume_running()
            else:
                self.pause_running()
    
    def start_running(self):
        """开始跑步"""
        self.is_running = True
        self.is_paused = False
        self.start_time = datetime.now()
        self.total_distance = 0
        self.pause_time = 0
        self.locations_history = []
        
        # 清除地图
        self.map_widget.clear_route()
        
        # 更新按钮状态
        self.start_button.text = '暂停'
        self.start_button.background_color = [1, 1, 0, 1]  # 黄色
        self.stop_button.disabled = False
        
        # 开始GPS追踪
        self.start_gps_tracking()
        
        # 初始化步数计数器
        self.init_pedometer()
        
        # 开始计时器
        self.timer_event = Clock.schedule_interval(self.update_display, 1)
        
        print("开始跑步")
    
    def pause_running(self):
        """暂停跑步"""
        self.is_paused = True
        self.pause_start_time = datetime.now()
        
        # 更新按钮
        self.start_button.text = '继续'
        self.start_button.background_color = [0, 1, 0, 1]  # 绿色
        
        # 停止GPS追踪
        self.stop_gps_tracking()
        
        print("暂停跑步")
    
    def resume_running(self):
        """恢复跑步"""
        self.is_paused = False
        
        # 累计暂停时间
        if hasattr(self, 'pause_start_time'):
            pause_duration = (datetime.now() - self.pause_start_time).total_seconds()
            self.pause_time += pause_duration
        
        # 更新按钮
        self.start_button.text = '暂停'
        self.start_button.background_color = [1, 1, 0, 1]  # 黄色
        
        # 重新开始GPS追踪
        self.start_gps_tracking()
        
        print("恢复跑步")
    
    def stop_running(self, instance):
        """停止跑步"""
        if not self.is_running:
            return
            
        # 停止计时器和GPS
        if self.timer_event:
            self.timer_event.cancel()
        self.stop_gps_tracking()
        
        # 保存跑步记录
        self.save_run_record()
        
        # 重置状态
        self.reset_run_state()
        
        print("停止跑步")
    
    def reset_run_state(self):
        """重置跑步状态"""
        self.is_running = False
        self.is_paused = False
        self.start_time = None
        self.pause_time = 0
        
        # 重置按钮
        self.start_button.text = '开始跑步'
        self.start_button.background_color = [0, 1, 0, 1]
        self.stop_button.disabled = True
        
        # 重置显示
        self.distance_label.text = '距离: 0.00 km'
        self.time_label.text = '时间: 00:00:00'
        self.pace_label.text = '配速: 0\'00"/km'
        self.avg_pace_label.text = '平均: 0\'00"/km'
    
    def start_gps_tracking(self):
        """开始GPS追踪"""
        try:
            app = App.get_running_app()
            if hasattr(app, 'gps_service'):
                app.gps_service.start_tracking(self.on_location_update)
        except Exception as e:
            print(f"GPS追踪启动失败: {e}")
            # 模拟GPS数据（用于测试）
            Clock.schedule_interval(self.simulate_gps, 2)
    
    def stop_gps_tracking(self):
        """停止GPS追踪"""
        try:
            app = App.get_running_app()
            if hasattr(app, 'gps_service'):
                app.gps_service.stop_tracking()
        except Exception as e:
            print(f"GPS追踪停止失败: {e}")
    
    def simulate_gps(self, dt):
        """模拟GPS数据（用于测试）"""
        if not self.is_running or self.is_paused:
            return False
            
        # 模拟移动
        if not self.last_location:
            lat, lon = 39.9042, 116.4074  # 北京坐标
        else:
            lat, lon = self.last_location
            # 随机移动
            import random
            lat += (random.random() - 0.5) * 0.001
            lon += (random.random() - 0.5) * 0.001
        
        self.on_location_update(lat, lon, 0)
        return True
    
    def on_location_update(self, lat, lon, altitude, accuracy=999, status='unknown'):
        """GPS位置更新回调（包含GPS状态）"""
        if not self.is_running or self.is_paused:
            return
        
        # 更新GPS状态显示
        self.gps_status = status
        self.location_accuracy = accuracy
        self.update_gps_status_display()
        
        # 检查是否需要切换到步数模式
        if accuracy > 20 or status in ['weak', 'unavailable']:
            if not self.use_pedometer:
                self.switch_to_pedometer_mode()
        else:
            if self.use_pedometer:
                self.switch_to_gps_mode()
        
        # 如果使用GPS模式，处理GPS数据
        if not self.use_pedometer:
            current_location = (lat, lon)
            
            # 计算距离
            if self.last_location:
                distance = self.calculate_distance(self.last_location, current_location)
                self.total_distance += distance
                
                # 计算速度（km/h）
                if len(self.locations_history) > 0:
                    time_diff = 2  # 假设2秒间隔
                    self.current_speed = (distance / 1000) / (time_diff / 3600)
            
            # 更新地图
            self.map_widget.update_location(lat, lon)
            
            # 保存位置历史
            self.last_location = current_location
            self.locations_history.append({
                'lat': lat,
                'lon': lon,
                'timestamp': datetime.now(),
                'distance': self.total_distance,
                'accuracy': accuracy,
                'source': 'gps'
            })
    
    def calculate_distance(self, loc1, loc2):
        """计算两点间距离（米）"""
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        
        # 使用Haversine公式
        R = 6371000  # 地球半径（米）
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lon/2) * math.sin(delta_lon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distance = R * c
        return distance
    
    def update_display(self, dt):
        """更新显示数据"""
        if not self.is_running:
            return False
        
        # 如果暂停状态，不更新时间显示
        if self.is_paused:
            return True
            
        # 计算运动时间
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            total_seconds = elapsed.total_seconds() - self.pause_time
            
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            
            self.time_label.text = f'时间: {hours:02d}:{minutes:02d}:{seconds:02d}'
            
            # 更新距离
            self.distance_label.text = f'距离: {self.total_distance/1000:.2f} km'
            
            # 更新步数显示
            if self.use_pedometer:
                self.steps_label.text = f'步数: {self.step_count}'
            else:
                self.steps_label.text = '步数: --'
            
            # 计算配速
            if self.total_distance > 0 and total_seconds > 0:
                # 配速：分钟/公里
                pace_seconds = (total_seconds / 60) / (self.total_distance / 1000)
                pace_min = int(pace_seconds)
                pace_sec = int((pace_seconds - pace_min) * 60)
                self.avg_pace_label.text = f'平均: {pace_min}\'{pace_sec:02d}"/km'
                
                # 当前配速
                if self.current_speed > 0:
                    current_pace = 60 / self.current_speed
                    curr_min = int(current_pace)
                    curr_sec = int((current_pace - curr_min) * 60)
                    self.pace_label.text = f'配速: {curr_min}\'{curr_sec:02d}"/km'
        
        return True
    
    def save_run_record(self):
        """保存跑步记录"""
        if not self.start_time or self.total_distance < 100:  # 最少100米
            return
            
        # 计算总时间
        elapsed = datetime.now() - self.start_time
        total_seconds = elapsed.total_seconds() - self.pause_time
        
        # 计算平均配速
        avg_pace = 0
        if self.total_distance > 0:
            avg_pace = (total_seconds / 60) / (self.total_distance / 1000)
        
        # 构建记录数据
        run_record = {
            'date': self.start_time.strftime('%Y-%m-%d'),
            'start_time': self.start_time.isoformat(),
            'duration': total_seconds,
            'distance': self.total_distance,
            'average_pace': avg_pace,
            'route': self.locations_history,
            'calories': int(self.total_distance * 0.05),  # 简单估算卡路里
        }
        
        try:
            # 保存到本地存储
            app = App.get_running_app()
            if hasattr(app, 'storage'):
                app.storage.save_run_record(run_record)
            
            # 显示保存成功提示
            self.show_save_success(run_record)
            
        except Exception as e:
            print(f"保存跑步记录失败: {e}")
    
    def show_save_success(self, record):
        """显示保存成功弹窗"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(text='跑步完成！', font_size='20sp',
            font_name='Chinese'
        ))
        content.add_widget(Label(text=f'距离: {record["distance"]/1000:.2f} km',
            font_name='Chinese'
        ))
        content.add_widget(Label(text=f'时间: {record["duration"]//60:.0f}:{record["duration"]%60:.0f}',
            font_name='Chinese'
        ))
        content.add_widget(Label(text=f'卡路里: {record["calories"]} kcal',
            font_name='Chinese'
        ))
        
        # 添加备注输入
        note_input = TextInput(
            hint_text='添加备注（可选）',
            multiline=True,
            size_hint_y=0.3
        )
        content.add_widget(note_input)
        
        # 按钮
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)
        
        close_btn = Button(text='确定',
            font_name='Chinese'
        )
        btn_layout.add_widget(close_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='跑步记录已保存',
            content=content,
            size_hint=(0.8, 0.6)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def init_pedometer(self):
        """初始化步数计数器"""
        try:
            app = App.get_running_app() if self.manager else None
            if app and hasattr(app, 'pedometer_service'):
                # 设置用户身高来计算步长
                user_height = app.user_data.get('height', 170)
                app.pedometer_service.set_user_height(user_height)
        except Exception as e:
            print(f"初始化步数计数器失败: {e}")
    
    def switch_to_pedometer_mode(self):
        """切换到步数计数器模式"""
        if self.use_pedometer:
            return
            
        print("📱 GPS信号弱，切换到步数计数模式")
        self.use_pedometer = True
        
        # 启动步数计数器
        try:
            app = App.get_running_app() if self.manager else None
            if app and hasattr(app, 'pedometer_service'):
                app.pedometer_service.start_counting(self.on_step_update)
        except Exception as e:
            print(f"启动步数计数失败: {e}")
        
        # 更新UI显示
        self.source_label.text = '数据源: 步数估算'
        self.source_label.color = [1, 0.8, 0.4, 1]
    
    def switch_to_gps_mode(self):
        """切换到GPS模式"""
        if not self.use_pedometer:
            return
            
        print("📡 GPS信号恢复，切换到GPS模式")
        self.use_pedometer = False
        
        # 停止步数计数器
        try:
            app = App.get_running_app() if self.manager else None
            if app and hasattr(app, 'pedometer_service'):
                app.pedometer_service.stop_counting()
        except Exception as e:
            print(f"停止步数计数失败: {e}")
        
        # 更新UI显示
        self.source_label.text = '数据源: GPS'
        self.source_label.color = [0.7, 0.7, 0.7, 1]
    
    def on_step_update(self, steps, estimated_distance):
        """步数更新回调"""
        if not self.is_running or self.is_paused or not self.use_pedometer:
            return
        
        self.step_count = steps
        self.pedometer_distance = estimated_distance
        
        # 使用步数估算的总距离
        self.total_distance = self.pedometer_distance
        
        # 保存步数记录
        self.locations_history.append({
            'steps': steps,
            'estimated_distance': estimated_distance,
            'timestamp': datetime.now(),
            'source': 'pedometer'
        })
    
    def update_gps_status_display(self):
        """更新GPS状态显示"""
        if self.gps_status == 'good':
            self.gps_status_label.text = f'GPS: 良好 ({self.location_accuracy:.0f}m)'
            self.gps_status_label.color = [0, 1, 0, 1]  # 绿色
        elif self.gps_status == 'weak':
            self.gps_status_label.text = f'GPS: 信号弱 ({self.location_accuracy:.0f}m)'
            self.gps_status_label.color = [1, 1, 0, 1]  # 黄色
        elif self.gps_status in ['unavailable', 'disabled']:
            self.gps_status_label.text = 'GPS: 不可用'
            self.gps_status_label.color = [1, 0, 0, 1]  # 红色
        else:
            self.gps_status_label.text = 'GPS: 未知'
            self.gps_status_label.color = [0.7, 0.7, 0.7, 1]  # 灰色
