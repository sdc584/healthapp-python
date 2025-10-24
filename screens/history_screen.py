# -*- coding: utf-8 -*-
"""
历史记录屏幕
显示历史跑步和饮食记录
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.app import App
from datetime import datetime, timedelta
import calendar

class HistoryScreen(Screen):
    """历史记录屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.now()
        self.selected_date = None
        
        self.build_ui()
        
    def build_ui(self):
        """构建用户界面"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        
        header_layout.add_widget(Label(text='历史记录', font_size='24sp',
            font_name='Chinese'
        ))
        
        # 筛选按钮
        filter_btn = Button(
            text='本月',
            size_hint_x=0.3,
            background_color=[0.2, 0.6, 1, 1]
        ,
            font_name='Chinese'
        )
        filter_btn.bind(on_press=self.show_filter_options)
        header_layout.add_widget(filter_btn)
        
        main_layout.add_widget(header_layout)
        
        # 日历区域
        calendar_section = BoxLayout(orientation='vertical', size_hint_y=0.4)
        
        # 月份导航
        month_nav = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        
        prev_btn = Button(text='<', size_hint_x=0.2,
            font_name='Chinese'
        )
        prev_btn.bind(on_press=self.prev_month)
        month_nav.add_widget(prev_btn)
        
        self.month_label = Label(
            text=self.current_date.strftime('%Y年%m月'),
            font_size='18sp',
            font_name='Chinese'
        )
        month_nav.add_widget(self.month_label)
        
        next_btn = Button(text='>', size_hint_x=0.2,
            font_name='Chinese'
        )
        next_btn.bind(on_press=self.next_month)
        month_nav.add_widget(next_btn)
        
        calendar_section.add_widget(month_nav)
        
        # 日历网格
        self.calendar_grid = GridLayout(cols=7, size_hint_y=0.85, spacing=2)
        calendar_section.add_widget(self.calendar_grid)
        
        main_layout.add_widget(calendar_section)
        
        # 记录详情区域
        details_section = BoxLayout(orientation='vertical', size_hint_y=0.5)
        
        self.details_title = Label(
            text='选择日期查看记录',
            size_hint_y=0.1,
            font_size='16sp'
        ,
            font_name='Chinese'
        )
        details_section.add_widget(self.details_title)
        
        # 滚动区域
        scroll = ScrollView(size_hint_y=0.9)
        self.details_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10
        )
        self.details_layout.bind(minimum_height=self.details_layout.setter('height'))
        scroll.add_widget(self.details_layout)
        details_section.add_widget(scroll)
        
        main_layout.add_widget(details_section)
        
        self.add_widget(main_layout)
        
        # 初始化日历
        self.update_calendar()
        
    def update_calendar(self):
        """更新日历显示"""
        self.calendar_grid.clear_widgets()
        
        # 星期标题
        weekdays = ['一', '二', '三', '四', '五', '六', '日']
        for day in weekdays:
            label = Label(text=day, size_hint_y=None, height=30, font_size='14sp',
            font_name='Chinese'
        )
            self.calendar_grid.add_widget(label)
        
        # 获取月份信息
        year = self.current_date.year
        month = self.current_date.month
        
        # 获取该月的日历
        cal = calendar.monthcalendar(year, month)
        
        for week in cal:
            for day in week:
                if day == 0:
                    # 空白日期
                    label = Label(text='', size_hint_y=None, height=40,
            font_name='Chinese'
        )
                    self.calendar_grid.add_widget(label)
                else:
                    # 创建日期按钮
                    date_str = f"{year:04d}-{month:02d}-{day:02d}"
                    
                    # 检查是否有记录
                    has_data = self.has_data_for_date(date_str)
                    
                    btn = Button(
                        text=str(day),
                        size_hint_y=None,
                        height=40,
                        background_color=[0.2, 0.8, 0.2, 1] if has_data else [0.5, 0.5, 0.5, 1],
                        font_name='Chinese'
                    )
                    btn.bind(on_press=lambda x, date=date_str: self.select_date(date))
                    self.calendar_grid.add_widget(btn)
    
    def has_data_for_date(self, date_str):
        """检查指定日期是否有数据"""
        try:
            app = App.get_running_app()
            if not app or not hasattr(app, 'storage'):
                return False
            
            # 检查跑步记录
            run_data = app.storage.load_daily_run_data(date_str)
            if run_data.get('runs'):
                return True
            
            # 检查饮食记录
            food_data = app.storage.load_daily_food_data(date_str)
            if food_data.get('foods'):
                return True
            
            return False
            
        except:
            return False
    
    def prev_month(self, instance):
        """上一月"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year-1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month-1)
        
        self.month_label.text = self.current_date.strftime('%Y年%m月')
        self.update_calendar()
    
    def next_month(self, instance):
        """下一月"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year+1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month+1)
        
        self.month_label.text = self.current_date.strftime('%Y年%m月')
        self.update_calendar()
    
    def select_date(self, date_str):
        """选择日期"""
        self.selected_date = date_str
        self.details_title.text = f'{date_str} 的记录'
        self.load_date_details(date_str)
    
    def load_date_details(self, date_str):
        """加载日期详情"""
        self.details_layout.clear_widgets()
        
        try:
            app = App.get_running_app()
            if not app or not hasattr(app, 'storage'):
                self.details_layout.add_widget(Label(text='无法加载数据', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
                return
            
            # 加载跑步记录
            run_data = app.storage.load_daily_run_data(date_str)
            runs = run_data.get('runs', [])
            
            if runs:
                # 跑步记录标题
                run_title = Label(
                    text=f'跑步记录 ({len(runs)}次)',
                    size_hint_y=None,
                    height=30,
                    font_size='16sp',
                    color=[0.8, 0.8, 1, 1],
                    font_name='Chinese'
                )
                self.details_layout.add_widget(run_title)
                
                for i, run in enumerate(runs):
                    run_item = self.create_run_item(run, i+1)
                    self.details_layout.add_widget(run_item)
            
            # 加载饮食记录
            food_data = app.storage.load_daily_food_data(date_str)
            foods = food_data.get('foods', [])
            nutrition = food_data.get('nutrition', {})
            
            if foods:
                # 饮食记录标题
                food_title = Label(
                    text=f'饮食记录 ({len(foods)}项)',
                    size_hint_y=None,
                    height=30,
                    font_size='16sp',
                    color=[0.8, 1, 0.8, 1],
                    font_name='Chinese'
                )
                self.details_layout.add_widget(food_title)
                
                # 营养汇总
                nutrition_summary = Label(
                    text=f'总热量: {nutrition.get("calories", 0):.0f}kcal | ' + 
                         f'蛋白质: {nutrition.get("protein", 0):.1f}g | ' +
                         f'碳水: {nutrition.get("carbs", 0):.1f}g | ' +
                         f'脂肪: {nutrition.get("fat", 0):.1f}g',
                    size_hint_y=None,
                    height=30,
                    font_size='12sp',
                    color=[0.7, 0.7, 0.7, 1],
                    font_name='Chinese'
                )
                self.details_layout.add_widget(nutrition_summary)
                
                # 按餐次分组显示
                meals = {}
                for food in foods:
                    meal_type = food.get('meal_type', '加餐')
                    if meal_type not in meals:
                        meals[meal_type] = []
                    meals[meal_type].append(food)
                
                for meal_type, meal_foods in meals.items():
                    meal_label = Label(
                        text=f'{meal_type}:',
                        size_hint_y=None,
                        height=25,
                        font_size='14sp'
                    ,
            font_name='Chinese'
        )
                    self.details_layout.add_widget(meal_label)
                    
                    for food in meal_foods:
                        food_item = self.create_food_item(food)
                        self.details_layout.add_widget(food_item)
            
            # 如果没有记录
            if not runs and not foods:
                no_data = Label(
                    text='该日期没有记录',
                    size_hint_y=None,
                    height=40,
                    color=[0.7, 0.7, 0.7, 1]
                ,
            font_name='Chinese'
        )
                self.details_layout.add_widget(no_data)
                
        except Exception as e:
            error_label = Label(
                text=f'加载数据失败: {e}',
                size_hint_y=None,
                height=40,
                color=[1, 0.5, 0.5, 1]
            ,
            font_name='Chinese'
        )
            self.details_layout.add_widget(error_label)
    
    def create_run_item(self, run, index):
        """创建跑步项目"""
        layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10
        )
        
        # 序号
        index_label = Label(
            text=f'{index}.',
            size_hint_x=0.1,
            font_size='14sp'
        ,
            font_name='Chinese'
        )
        layout.add_widget(index_label)
        
        # 跑步信息
        distance = run.get('distance', 0) / 1000  # 转换为公里
        duration = run.get('duration', 0)
        calories = run.get('calories', 0)
        
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        if hours > 0:
            duration_str = f'{hours}h{minutes}m'
        else:
            duration_str = f'{minutes}m'
        
        info_label = Label(
            text=f'距离: {distance:.2f}km | 时长: {duration_str} | 消耗: {calories:.0f}kcal',
            size_hint_x=0.8,
            font_size='12sp',
            text_size=(None, None),
            halign='left',
            font_name='Chinese'
        )
        layout.add_widget(info_label)
        
        # 详情按钮
        detail_btn = Button(
            text='详情',
            size_hint_x=0.1,
            background_color=[0.2, 0.6, 1, 1]
        ,
            font_name='Chinese'
        )
        detail_btn.bind(on_press=lambda x: self.show_run_details(run))
        layout.add_widget(detail_btn)
        
        return layout
    
    def create_food_item(self, food):
        """创建食物项目"""
        layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=40,
            spacing=5
        )
        
        # 食物信息
        name = food.get('name', '未知食物')
        calories = food.get('calories', 0)
        
        info_label = Label(
            text=f'  • {name} ({calories:.0f}kcal)',
            size_hint_x=0.9,
            font_size='12sp',
            text_size=(None, None),
            halign='left',
            font_name='Chinese'
        )
        layout.add_widget(info_label)
        
        return layout
    
    def show_run_details(self, run):
        """显示跑步详情"""
        popup = Popup(
            title='跑步详情',
            size_hint=(0.8, 0.7)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # 基本信息
        distance = run.get('distance', 0) / 1000
        duration = run.get('duration', 0)
        calories = run.get('calories', 0)
        avg_pace = run.get('average_pace', 0)
        
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        
        pace_min = int(avg_pace)
        pace_sec = int((avg_pace - pace_min) * 60)
        
        info_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.6)
        
        info_grid.add_widget(Label(text='距离:', halign='left',
            font_name='Chinese'
        ))
        info_grid.add_widget(Label(text=f'{distance:.2f} km', halign='left',
            font_name='Chinese'
        ))
        
        info_grid.add_widget(Label(text='时长:', halign='left',
            font_name='Chinese'
        ))
        info_grid.add_widget(Label(text=f'{hours:02d}:{minutes:02d}:{seconds:02d}', halign='left',
            font_name='Chinese'
        ))
        
        info_grid.add_widget(Label(text='平均配速:', halign='left',
            font_name='Chinese'
        ))
        info_grid.add_widget(Label(text=f'{pace_min}\'{pace_sec:02d}"/km', halign='left',
            font_name='Chinese'
        ))
        
        info_grid.add_widget(Label(text='消耗卡路里:', halign='left',
            font_name='Chinese'
        ))
        info_grid.add_widget(Label(text=f'{calories:.0f} kcal', halign='left',
            font_name='Chinese'
        ))
        
        content.add_widget(info_grid)
        
        # 关闭按钮
        close_btn = Button(text='关闭', size_hint_y=0.15,
            font_name='Chinese'
        )
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.content = content
        popup.open()
    
    def show_filter_options(self, instance):
        """显示筛选选项"""
        popup = Popup(
            title='选择时间范围',
            size_hint=(0.6, 0.5)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # 筛选选项
        options = [
            ('本周', 7),
            ('本月', 30),
            ('近3个月', 90)
        ]
        
        for text, days in options:
            btn = Button(text=text, size_hint_y=0.25,
            font_name='Chinese'
        )
            btn.bind(on_press=lambda x, d=days: self.apply_filter(d, popup))
            content.add_widget(btn)
        
        popup.content = content
        popup.open()
    
    def apply_filter(self, days, popup):
        """应用筛选"""
        popup.dismiss()
        
        # 这里可以实现筛选逻辑
        # 暂时只是切换到当前月份
        self.current_date = datetime.now()
        self.month_label.text = self.current_date.strftime('%Y年%m月')
        self.update_calendar()
