# -*- coding: utf-8 -*-
"""
今日总览屏幕
显示今日跑步和饮食数据统计
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.widget import Widget
from kivy.app import App
from datetime import datetime, timedelta
import math

class CircularProgress(Widget):
    """环形进度条组件"""
    
    def __init__(self, value=0, max_value=100, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.max_value = max_value
        self.bind(size=self.update_graphics)
        self.bind(pos=self.update_graphics)
        
    def update_graphics(self, *args):
        """更新绘图"""
        self.canvas.clear()
        
        if self.max_value <= 0:
            return
            
        with self.canvas:
            # 背景圆环
            Color(0.3, 0.3, 0.3, 1)
            center_x = self.center_x
            center_y = self.center_y
            radius = min(self.width, self.height) / 2 - 10
            
            # 绘制背景圆
            Line(circle=(center_x, center_y, radius), width=8)
            
            # 进度圆环
            if self.value > 0:
                Color(0.2, 0.8, 0.2, 1)  # 绿色进度
                progress = min(self.value / self.max_value, 1.0)
                angle_end = 360 * progress
                
                # 绘制进度弧
                Line(
                    circle=(center_x, center_y, radius, 0, angle_end),
                    width=8
                )
    
    def set_value(self, value):
        """设置数值"""
        self.value = value
        self.update_graphics()

class TodayScreen(Screen):
    """今日总览屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        
    def build_ui(self):
        """构建用户界面"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=15)
        
        # 标题
        title = Label(
            text='今日总览',
            size_hint_y=0.1,
            font_size='24sp',
            color=[1, 1, 1, 1]
        ,
            font_name='Chinese'
        )
        main_layout.add_widget(title)
        
        # 卡路里环形图区域
        calories_section = BoxLayout(orientation='vertical', size_hint_y=0.4)
        
        calories_title = Label(
            text='今日卡路里',
            size_hint_y=0.2,
            font_size='18sp'
        ,
            font_name='Chinese'
        )
        calories_section.add_widget(calories_title)
        
        # 环形图容器
        circle_container = BoxLayout(orientation='horizontal')
        
        # 环形进度条
        self.calorie_circle = CircularProgress(size_hint=(0.5, 1))
        circle_container.add_widget(self.calorie_circle)
        
        # 卡路里数据显示
        calorie_info = BoxLayout(orientation='vertical', size_hint=(0.5, 1))
        
        self.calorie_consumed = Label(
            text='摄入: 0 kcal',
            font_size='16sp',
            size_hint_y=0.33
        ,
            font_name='Chinese'
        )
        calorie_info.add_widget(self.calorie_consumed)
        
        self.calorie_burned = Label(
            text='消耗: 0 kcal',
            font_size='16sp',
            size_hint_y=0.33
        ,
            font_name='Chinese'
        )
        calorie_info.add_widget(self.calorie_burned)
        
        self.calorie_goal = Label(
            text='目标: 2000 kcal',
            font_size='16sp',
            size_hint_y=0.34
        ,
            font_name='Chinese'
        )
        calorie_info.add_widget(self.calorie_goal)
        
        circle_container.add_widget(calorie_info)
        calories_section.add_widget(circle_container)
        main_layout.add_widget(calories_section)
        
        # 三大营养素进度条
        nutrition_section = BoxLayout(orientation='vertical', size_hint_y=0.25)
        
        nutrition_title = Label(
            text='营养素摄入',
            size_hint_y=0.3,
            font_size='18sp'
        ,
            font_name='Chinese'
        )
        nutrition_section.add_widget(nutrition_title)
        
        # 蛋白质
        protein_layout = BoxLayout(orientation='horizontal', size_hint_y=0.23, spacing=10)
        protein_layout.add_widget(Label(text='蛋白质', size_hint_x=0.2,
            font_name='Chinese'
        ))
        
        self.protein_bar = ProgressBar(max=100, size_hint_x=0.6)
        protein_layout.add_widget(self.protein_bar)
        
        self.protein_label = Label(text='0/60g', size_hint_x=0.2,
            font_name='Chinese'
        )
        protein_layout.add_widget(self.protein_label)
        
        nutrition_section.add_widget(protein_layout)
        
        # 碳水化合物
        carbs_layout = BoxLayout(orientation='horizontal', size_hint_y=0.23, spacing=10)
        carbs_layout.add_widget(Label(text='碳水', size_hint_x=0.2,
            font_name='Chinese'
        ))
        
        self.carbs_bar = ProgressBar(max=100, size_hint_x=0.6)
        carbs_layout.add_widget(self.carbs_bar)
        
        self.carbs_label = Label(text='0/250g', size_hint_x=0.2,
            font_name='Chinese'
        )
        carbs_layout.add_widget(self.carbs_label)
        
        nutrition_section.add_widget(carbs_layout)
        
        # 脂肪
        fat_layout = BoxLayout(orientation='horizontal', size_hint_y=0.24, spacing=10)
        fat_layout.add_widget(Label(text='脂肪', size_hint_x=0.2,
            font_name='Chinese'
        ))
        
        self.fat_bar = ProgressBar(max=100, size_hint_x=0.6)
        fat_layout.add_widget(self.fat_bar)
        
        self.fat_label = Label(text='0/65g', size_hint_x=0.2,
            font_name='Chinese'
        )
        fat_layout.add_widget(self.fat_label)
        
        nutrition_section.add_widget(fat_layout)
        main_layout.add_widget(nutrition_section)
        
        # 今日运动摘要
        exercise_section = BoxLayout(orientation='vertical', size_hint_y=0.25)
        
        exercise_title = Label(
            text='今日运动',
            size_hint_y=0.3,
            font_size='18sp'
        ,
            font_name='Chinese'
        )
        exercise_section.add_widget(exercise_title)
        
        exercise_grid = GridLayout(cols=3, size_hint_y=0.7, spacing=10)
        
        # 跑步距离
        self.run_distance = Label(
            text='跑步距离\n0.0 km',
            halign='center',
            font_size='14sp'
        ,
            font_name='Chinese'
        )
        exercise_grid.add_widget(self.run_distance)
        
        # 运动时长
        self.run_duration = Label(
            text='运动时长\n00:00',
            halign='center',
            font_size='14sp'
        ,
            font_name='Chinese'
        )
        exercise_grid.add_widget(self.run_duration)
        
        # 消耗卡路里
        self.run_calories = Label(
            text='消耗卡路里\n0 kcal',
            halign='center',
            font_size='14sp'
        ,
            font_name='Chinese'
        )
        exercise_grid.add_widget(self.run_calories)
        
        exercise_section.add_widget(exercise_grid)
        main_layout.add_widget(exercise_section)
        
        self.add_widget(main_layout)
        
        # 设置更新事件
        self.bind(on_enter=self.load_today_data)
        
        # 添加刷新按钮
        refresh_btn = Button(
            text='刷新数据',
            size_hint_y=None,
            height=40,
            font_size='16sp',
            background_color=[0.2, 0.8, 0.2, 1],
            font_name='Chinese'
        )
        refresh_btn.bind(on_press=self.load_today_data)
        main_layout.add_widget(refresh_btn)
    
    def load_today_data(self, *args):
        """加载今日数据"""
        try:
            app = App.get_running_app()
            if not app:
                print("❌ 今日模块：无法获取应用实例")
                return
            
            today = datetime.now().strftime('%Y-%m-%d')
            print(f"📅 今日模块：加载 {today} 的数据")
            
            # 加载饮食数据
            if hasattr(app, 'storage'):
                food_data = app.storage.load_daily_food_data(today)
                foods = food_data.get('foods', [])
                print(f"🍎 今日模块：加载到 {len(foods)} 个食物记录")
                
                # 如果今天没有数据，尝试加载昨天的数据
                if len(foods) == 0:
                    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                    print(f"📅 今日模块：今天没有数据，尝试加载昨天 {yesterday} 的数据")
                    food_data = app.storage.load_daily_food_data(yesterday)
                    foods = food_data.get('foods', [])
                    print(f"🍎 今日模块：昨天加载到 {len(foods)} 个食物记录")
                
                # 重新计算营养数据
                nutrition = {
                    'calories': 0,
                    'protein': 0,
                    'carbs': 0,
                    'fat': 0
                }
                
                for food in foods:
                    nutrition['calories'] += food.get('calories', 0)
                    nutrition['protein'] += food.get('protein', 0)
                    nutrition['carbs'] += food.get('carbs', 0)
                    nutrition['fat'] += food.get('fat', 0)
                
                print(f"📊 今日模块：营养数据 - 卡路里: {nutrition['calories']}, 蛋白质: {nutrition['protein']}")
                self.update_nutrition_display(nutrition)
            else:
                print("❌ 今日模块：应用没有storage属性")
            
            # 加载运动数据
            if hasattr(app, 'storage'):
                run_data = app.storage.load_daily_run_data(today)
                runs = run_data.get('runs', [])
                print(f"🏃 今日模块：加载到 {len(runs)} 个跑步记录")
                
                # 如果今天没有跑步数据，尝试加载昨天的数据
                if len(runs) == 0:
                    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                    print(f"📅 今日模块：今天没有跑步数据，尝试加载昨天 {yesterday} 的数据")
                    run_data = app.storage.load_daily_run_data(yesterday)
                    runs = run_data.get('runs', [])
                    print(f"🏃 今日模块：昨天加载到 {len(runs)} 个跑步记录")
                
                self.update_exercise_display(run_data)
                
        except Exception as e:
            print(f"❌ 今日模块加载数据失败: {e}")
    
    def update_nutrition_display(self, nutrition):
        """更新营养显示"""
        try:
            # 获取营养数据
            calories_consumed = nutrition.get('calories', 0)
            protein = nutrition.get('protein', 0)
            carbs = nutrition.get('carbs', 0)
            fat = nutrition.get('fat', 0)
            
            # 目标值（可以从用户设置获取）
            calorie_goal = 2000
            protein_goal = 60
            carbs_goal = 250
            fat_goal = 65
            
            # 更新卡路里环形图
            self.calorie_circle.max_value = calorie_goal
            self.calorie_circle.set_value(calories_consumed)
            
            self.calorie_consumed.text = f'摄入: {calories_consumed:.0f} kcal'
            self.calorie_goal.text = f'目标: {calorie_goal} kcal'
            
            # 更新营养素进度条
            # 蛋白质
            protein_percent = min((protein / protein_goal) * 100, 100) if protein_goal > 0 else 0
            self.protein_bar.value = protein_percent
            self.protein_label.text = f'{protein:.1f}/{protein_goal}g'
            
            # 碳水化合物
            carbs_percent = min((carbs / carbs_goal) * 100, 100) if carbs_goal > 0 else 0
            self.carbs_bar.value = carbs_percent
            self.carbs_label.text = f'{carbs:.1f}/{carbs_goal}g'
            
            # 脂肪
            fat_percent = min((fat / fat_goal) * 100, 100) if fat_goal > 0 else 0
            self.fat_bar.value = fat_percent
            self.fat_label.text = f'{fat:.1f}/{fat_goal}g'
            
        except Exception as e:
            print(f"更新营养显示失败: {e}")
    
    def update_exercise_display(self, run_data):
        """更新运动显示"""
        try:
            total_distance = 0
            total_duration = 0
            total_calories = 0
            
            runs = run_data.get('runs', [])
            
            for run in runs:
                total_distance += run.get('distance', 0)
                total_duration += run.get('duration', 0)
                total_calories += run.get('calories', 0)
            
            # 更新显示
            self.run_distance.text = f'跑步距离\n{total_distance/1000:.1f} km'
            
            # 格式化时长
            hours = int(total_duration // 3600)
            minutes = int((total_duration % 3600) // 60)
            if hours > 0:
                duration_str = f'{hours}h{minutes}m'
            else:
                duration_str = f'{minutes}m'
            
            self.run_duration.text = f'运动时长\n{duration_str}'
            self.run_calories.text = f'消耗卡路里\n{total_calories:.0f} kcal'
            
            # 更新卡路里消耗
            self.calorie_burned.text = f'消耗: {total_calories:.0f} kcal'
            
        except Exception as e:
            print(f"更新运动显示失败: {e}")
