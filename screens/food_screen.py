# -*- coding: utf-8 -*-
"""
饮食记录屏幕
实现食物扫码、手动录入、营养计算功能
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.app import App
from datetime import datetime
import threading

class FoodEditPopup(Popup):
    """食物编辑弹窗"""
    
    def __init__(self, food_data=None, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.food_data = food_data or {}
        self.callback = callback
        self.title = 'Edit Food'  # 使用英文标题避免中文字体问题
        self.size_hint = (0.9, 0.8)
        self.title_size = '18sp'
        
        self.build_content()
    
    def build_content(self):
        """构建弹窗内容"""
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # 标题
        title_label = Label(
            text='食物信息编辑',
            size_hint_y=0.1,
            font_size='18sp',
            font_name='Chinese'
        )
        main_layout.add_widget(title_label)
        
        # 滚动视图
        scroll = ScrollView()
        content_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # 食物基本信息
        content_layout.add_widget(Label(text='食物名称:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        self.name_input = TextInput(
            text=self.food_data.get('name', ''),
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        content_layout.add_widget(self.name_input)
        
        content_layout.add_widget(Label(text='品牌:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        self.brand_input = TextInput(
            text=self.food_data.get('brand', ''),
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        content_layout.add_widget(self.brand_input)
        
        # 份量选择
        content_layout.add_widget(Label(text='份量:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        serving_layout = BoxLayout(size_hint_y=None, height=40)
        
        self.serving_input = TextInput(
            text=str(self.food_data.get('serving_size', 100)),
            input_filter='float',
            multiline=False,
            size_hint_x=0.7,
            font_name='Chinese'
        )
        serving_layout.add_widget(self.serving_input)
        serving_layout.add_widget(Label(text='g', size_hint_x=0.3,
            font_name='Chinese'
        ))
        content_layout.add_widget(serving_layout)
        
        # 份数选择
        content_layout.add_widget(Label(text='份数:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        self.servings_spinner = Spinner(
            text=str(self.food_data.get('servings', 1)),
            values=['0.5', '1', '1.5', '2', '2.5', '3'],
            size_hint_y=None,
            height=40
        )
        content_layout.add_widget(self.servings_spinner)
        
        # 营养信息
        content_layout.add_widget(Label(text='热量(kcal):',
            font_name='Chinese', size_hint_y=None, height=40))
        self.calories_input = TextInput(
            text=str(self.food_data.get('calories', 0)),
            input_filter='float',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        content_layout.add_widget(self.calories_input)
        
        content_layout.add_widget(Label(text='蛋白质(g):',
            font_name='Chinese', size_hint_y=None, height=40))
        self.protein_input = TextInput(
            text=str(self.food_data.get('protein', 0)),
            input_filter='float',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        content_layout.add_widget(self.protein_input)
        
        content_layout.add_widget(Label(text='碳水化合物(g):',
            font_name='Chinese', size_hint_y=None, height=40))
        self.carbs_input = TextInput(
            text=str(self.food_data.get('carbs', 0)),
            input_filter='float',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        content_layout.add_widget(self.carbs_input)
        
        content_layout.add_widget(Label(text='脂肪(g):',
            font_name='Chinese', size_hint_y=None, height=40))
        self.fat_input = TextInput(
            text=str(self.food_data.get('fat', 0)),
            input_filter='float',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        content_layout.add_widget(self.fat_input)
        
        # 餐次选择
        content_layout.add_widget(Label(text='餐次:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        self.meal_spinner = Spinner(
            text=self.food_data.get('meal_type', '早餐'),
            values=['早餐', '午餐', '晚餐', '加餐'],
            size_hint_y=None,
            height=40
        )
        content_layout.add_widget(self.meal_spinner)
        
        # 日期时间
        content_layout.add_widget(Label(text='日期:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        current_date = self.food_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        self.date_input = TextInput(
            text=current_date,
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        content_layout.add_widget(self.date_input)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        # 按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        
        cancel_btn = Button(text='取消', background_color=[0.5, 0.5, 0.5, 1],
            font_name='Chinese'
        )
        cancel_btn.bind(on_press=self.dismiss)
        button_layout.add_widget(cancel_btn)
        
        save_btn = Button(text='保存', background_color=[0, 0.8, 0, 1],
            font_name='Chinese'
        )
        save_btn.bind(on_press=self.save_food)
        button_layout.add_widget(save_btn)
        
        main_layout.add_widget(button_layout)
        self.content = main_layout
    
    def save_food(self, instance):
        """保存食物数据"""
        try:
            # 获取基础数据
            serving_size = float(self.serving_input.text or 100)
            servings = float(self.servings_spinner.text or 1)
            
            # 计算实际营养值
            base_calories = float(self.calories_input.text or 0)
            base_protein = float(self.protein_input.text or 0)
            base_carbs = float(self.carbs_input.text or 0)
            base_fat = float(self.fat_input.text or 0)
            
            # 按照份量和份数计算
            multiplier = (serving_size / 100) * servings
            
            food_record = {
                'name': self.name_input.text,
                'brand': self.brand_input.text,
                'serving_size': serving_size,
                'servings': servings,
                'calories': base_calories * multiplier,
                'protein': base_protein * multiplier,
                'carbs': base_carbs * multiplier,
                'fat': base_fat * multiplier,
                'meal_type': self.meal_spinner.text,
                'date': self.date_input.text,
                'timestamp': datetime.now().isoformat()
            }
            
            if self.callback:
                self.callback(food_record)
            
            self.dismiss()
            
        except ValueError as e:
            # 显示错误信息
            error_popup = Popup(
                title='输入错误',
                content=Label(text='请检查数值输入是否正确',
            font_name='Chinese'
        ),
                size_hint=(0.6, 0.3)
            )
            error_popup.open()

class FoodScreen(Screen):
    """饮食记录主屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.today_foods = []
        self.daily_nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0
        }
        
        self.build_ui()
        self.load_today_data()
    
    def build_ui(self):
        """构建用户界面"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(
            text='饮食记录',
            size_hint_y=0.08,
            font_size='24sp',
            color=[1, 1, 1, 1]
        ,
            font_name='Chinese'
        )
        main_layout.add_widget(title)
        
        # 今日营养统计
        stats_layout = BoxLayout(orientation='vertical', size_hint_y=0.25)
        stats_title = Label(text='今日营养摄入', font_size='18sp', size_hint_y=0.3,
            font_name='Chinese'
        )
        stats_layout.add_widget(stats_title)
        
        # 营养数据网格
        nutrition_grid = GridLayout(cols=4, size_hint_y=0.7, spacing=5)
        
        self.calories_stat = Label(text='热量\n0 kcal', halign='center',
            font_name='Chinese'
        )
        self.protein_stat = Label(text='蛋白质\n0 g', halign='center',
            font_name='Chinese'
        )
        self.carbs_stat = Label(text='碳水\n0 g', halign='center',
            font_name='Chinese'
        )
        self.fat_stat = Label(text='脂肪\n0 g', halign='center',
            font_name='Chinese'
        )
        
        nutrition_grid.add_widget(self.calories_stat)
        nutrition_grid.add_widget(self.protein_stat)
        nutrition_grid.add_widget(self.carbs_stat)
        nutrition_grid.add_widget(self.fat_stat)
        
        stats_layout.add_widget(nutrition_grid)
        main_layout.add_widget(stats_layout)
        
        # 操作按钮
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.12, spacing=10)
        
        # 扫码按钮
        scan_btn = Button(
            text='扫描条形码',
            background_color=[0, 0.8, 1, 1],
            font_size='16sp'
        ,
            font_name='Chinese'
        )
        scan_btn.bind(on_press=self.scan_barcode)
        button_layout.add_widget(scan_btn)
        
        # 手动添加按钮
        add_btn = Button(
            text='手动添加',
            background_color=[0, 1, 0, 1],
            font_size='16sp'
        ,
            font_name='Chinese'
        )
        add_btn.bind(on_press=self.add_food_manually)
        button_layout.add_widget(add_btn)
        
        main_layout.add_widget(button_layout)
        
        # 今日食物列表
        food_list_title = Label(
            text='今日食物记录',
            size_hint_y=0.06,
            font_size='18sp'
        ,
            font_name='Chinese'
        )
        main_layout.add_widget(food_list_title)
        
        # 滚动列表
        scroll = ScrollView(size_hint_y=0.49)
        self.food_list_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=5
        )
        self.food_list_layout.bind(minimum_height=self.food_list_layout.setter('height'))
        scroll.add_widget(self.food_list_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def scan_barcode(self, instance):
        """扫描条形码"""
        # 检查相机权限
        app = App.get_running_app()
        if app and hasattr(app, 'camera_service'):
            camera_status = app.camera_service.get_camera_status()
            
            if not camera_status['available']:
                self.show_camera_unavailable_dialog()
                return
            
            if not camera_status['permission_granted']:
                self.show_permission_dialog()
                return
        
        # 显示扫码界面
        scan_popup = Popup(
            title='扫描条形码',
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # 状态指示器
        self.scan_status_label = Label(
            text='📷 准备扫描，请将条形码对准相机',
            size_hint_y=0.1,
            font_size='14sp',
            color=[0.8, 0.8, 1, 1]
        ,
            font_name='Chinese'
        )
        content.add_widget(self.scan_status_label)
        
        # 相机预览区域（简化显示）
        camera_frame = BoxLayout(orientation='vertical', size_hint_y=0.5)
        
        camera_area = Label(
            text='📱\n\n[相机取景框]\n\n将条形码放入框内\n自动识别中...',
            halign='center',
            color=[1, 1, 1, 1],
            font_size='16sp'
        ,
            font_name='Chinese'
        )
        camera_frame.add_widget(camera_area)
        content.add_widget(camera_frame)
        
        # 手动输入区域
        manual_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        
        manual_layout.add_widget(Label(text='手动输入:', size_hint_x=0.3,
            font_name='Chinese'
        ))
        
        barcode_input = TextInput(
            hint_text='输入条形码数字',
            multiline=False,
            size_hint_x=0.7,
            input_filter='int',
            font_name='Chinese'
        )
        manual_layout.add_widget(barcode_input)
        
        content.add_widget(manual_layout)
        
        # 按钮区域
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.25, spacing=10)
        
        # 开始扫描按钮
        scan_btn = Button(
            text='开始扫描',
            background_color=[0, 0.8, 1, 1]
        ,
            font_name='Chinese'
        )
        scan_btn.bind(on_press=lambda x: self.start_camera_scan(scan_popup, camera_area))
        btn_layout.add_widget(scan_btn)
        
        # 搜索按钮
        search_btn = Button(
            text='搜索条码',
            background_color=[0, 1, 0, 1]
        ,
            font_name='Chinese'
        )
        search_btn.bind(on_press=lambda x: self.search_barcode(barcode_input.text, scan_popup))
        btn_layout.add_widget(search_btn)
        
        # 取消按钮
        cancel_btn = Button(
            text='取消',
            background_color=[0.7, 0.7, 0.7, 1]
        ,
            font_name='Chinese'
        )
        cancel_btn.bind(on_press=lambda x: self.cancel_scan(scan_popup))
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        scan_popup.content = content
        scan_popup.open()
    
    def show_camera_unavailable_dialog(self):
        """显示相机不可用对话框"""
        popup = Popup(
            title='相机不可用',
            size_hint=(0.8, 0.4)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(
            text='相机功能不可用，请使用手动输入功能。',
            font_name='Chinese'
        ))
        
        close_btn = Button(text='确定', size_hint_y=0.3, font_name='Chinese')
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.content = content
        popup.open()
    
    def show_permission_dialog(self):
        """显示权限请求对话框"""
        popup = Popup(
            title='需要相机权限',
            size_hint=(0.8, 0.4)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(
            text='请授予相机权限以使用扫码功能。',
            font_name='Chinese'
        ))
        
        close_btn = Button(text='确定', size_hint_y=0.3, font_name='Chinese')
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.content = content
        popup.open()
    
    def simulate_barcode_scan(self, popup):
        """模拟条形码扫描（用于测试）"""
        # 模拟扫描到的食物数据
        mock_food = {
            'name': '苹果',
            'brand': '新鲜水果',
            'calories': 52,
            'protein': 0.3,
            'carbs': 14,
            'fat': 0.2,
            'barcode': '1234567890123'
        }
        
        popup.dismiss()
        self.show_food_from_scan(mock_food)
    
    def search_barcode(self, barcode, popup):
        """根据条形码搜索食物"""
        if not barcode.strip():
            return
            
        popup.dismiss()
        
        # 显示加载提示
        loading_popup = Popup(
            title='搜索中...',
            content=Label(text='正在查询食物信息...',
            font_name='Chinese'
        ),
            size_hint=(0.6, 0.3),
            auto_dismiss=False
        )
        loading_popup.open()
        
        # 异步搜索
        def search_thread():
            try:
                app = App.get_running_app()
                if hasattr(app, 'food_api'):
                    food_data = app.food_api.search_by_barcode(barcode)
                    
                    # 在主线程中更新UI
                    Clock.schedule_once(
                        lambda dt: self.handle_barcode_result(food_data, loading_popup), 0
                    )
                else:
                    # 模拟API调用失败
                    Clock.schedule_once(
                        lambda dt: self.handle_barcode_result(None, loading_popup), 1
                    )
            except Exception as e:
                Clock.schedule_once(
                    lambda dt: self.handle_barcode_result(None, loading_popup), 0
                )
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def handle_barcode_result(self, food_data, loading_popup):
        """处理条形码搜索结果"""
        loading_popup.dismiss()
        
        if food_data:
            self.show_food_from_scan(food_data)
        else:
            # 未找到结果，提示手动输入
            no_result_popup = Popup(
                title='未找到食物',
                size_hint=(0.7, 0.4)
            )
            
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            content.add_widget(Label(text='未找到该条形码对应的食物信息',
            font_name='Chinese'
        ))
            content.add_widget(Label(text='请选择手动添加或重新扫描',
            font_name='Chinese'
        ))
            
            btn_layout = BoxLayout(orientation='horizontal', spacing=10)
            
            manual_btn = Button(text='手动添加',
            font_name='Chinese'
        )
            manual_btn.bind(on_press=lambda x: [no_result_popup.dismiss(), self.add_food_manually(None)])
            btn_layout.add_widget(manual_btn)
            
            close_btn = Button(text='取消',
            font_name='Chinese'
        )
            close_btn.bind(on_press=no_result_popup.dismiss)
            btn_layout.add_widget(close_btn)
            
            content.add_widget(btn_layout)
            no_result_popup.content = content
            no_result_popup.open()
    
    def show_food_from_scan(self, food_data):
        """显示扫描到的食物信息"""
        # 打开编辑弹窗，预填充扫描数据
        edit_popup = FoodEditPopup(
            food_data=food_data,
            callback=self.add_food_record
        )
        edit_popup.open()
    
    def add_food_manually(self, instance):
        """手动添加食物"""
        edit_popup = FoodEditPopup(callback=self.add_food_record)
        edit_popup.open()
    
    def add_food_record(self, food_record):
        """添加食物记录"""
        try:
            # 保存到今日列表
            self.today_foods.append(food_record)
            
            # 更新营养统计
            self.daily_nutrition['calories'] += food_record['calories']
            self.daily_nutrition['protein'] += food_record['protein']
            self.daily_nutrition['carbs'] += food_record['carbs']
            self.daily_nutrition['fat'] += food_record['fat']
            
            # 更新显示
            self.update_nutrition_display()
            self.update_food_list()
            
            # 保存到存储
            self.save_food_data()
            
        except Exception as e:
            print(f"添加食物记录失败: {e}")
    
    def update_nutrition_display(self):
        """更新营养统计显示"""
        self.calories_stat.text = f'热量\n{self.daily_nutrition["calories"]:.0f} kcal'
        self.protein_stat.text = f'蛋白质\n{self.daily_nutrition["protein"]:.1f} g'
        self.carbs_stat.text = f'碳水\n{self.daily_nutrition["carbs"]:.1f} g'
        self.fat_stat.text = f'脂肪\n{self.daily_nutrition["fat"]:.1f} g'
    
    def update_food_list(self):
        """更新食物列表显示"""
        # 清空现有列表
        self.food_list_layout.clear_widgets()
        
        # 按餐次分组
        meals = {'早餐': [], '午餐': [], '晚餐': [], '加餐': []}
        for food in self.today_foods:
            meal_type = food.get('meal_type', '加餐')
            meals[meal_type].append(food)
        
        # 显示各餐次
        for meal_type, foods in meals.items():
            if not foods:
                continue
                
            # 餐次标题
            meal_header = Label(
                text=f'{meal_type} ({len(foods)}项)',
                size_hint_y=None,
                height=30,
                font_size='16sp',
                color=[0.8, 0.8, 1, 1],
                font_name='Chinese'
            )
            self.food_list_layout.add_widget(meal_header)
            
            # 食物项目
            for food in foods:
                food_item = self.create_food_item(food)
                self.food_list_layout.add_widget(food_item)
    
    def create_food_item(self, food_data):
        """创建食物项目组件"""
        item_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            spacing=10
        )
        
        # 食物信息
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        name_label = Label(
            text=f'{food_data["name"]} - {food_data.get("brand", "")}',
            size_hint_y=0.6,
            text_size=(None, None),
            halign='left',
            font_name='Chinese'
        )
        info_layout.add_widget(name_label)
        
        nutrition_label = Label(
            text=f'{food_data["calories"]:.0f}kcal | P:{food_data["protein"]:.1f}g C:{food_data["carbs"]:.1f}g F:{food_data["fat"]:.1f}g',
            size_hint_y=0.4,
            font_size='12sp',
            color=[0.7, 0.7, 0.7, 1],
            text_size=(None, None),
            halign='left',
            font_name='Chinese'
        )
        info_layout.add_widget(nutrition_label)
        
        item_layout.add_widget(info_layout)
        
        # 操作按钮
        btn_layout = BoxLayout(orientation='horizontal', size_hint_x=0.3, spacing=5)
        
        edit_btn = Button(
            text='编辑',
            size_hint_x=0.5,
            background_color=[0, 0.8, 1, 1]
        ,
            font_name='Chinese'
        )
        edit_btn.bind(on_press=lambda x: self.edit_food_item(food_data))
        btn_layout.add_widget(edit_btn)
        
        delete_btn = Button(
            text='删除',
            size_hint_x=0.5,
            background_color=[1, 0.3, 0.3, 1]
        ,
            font_name='Chinese'
        )
        delete_btn.bind(on_press=lambda x: self.delete_food_item(food_data))
        btn_layout.add_widget(delete_btn)
        
        item_layout.add_widget(btn_layout)
        
        return item_layout
    
    def edit_food_item(self, food_data):
        """编辑食物项目"""
        def update_callback(updated_food):
            # 找到并更新原记录
            for i, food in enumerate(self.today_foods):
                if food.get('timestamp') == food_data.get('timestamp'):
                    # 更新营养统计（减去原来的，加上新的）
                    self.daily_nutrition['calories'] -= food['calories']
                    self.daily_nutrition['protein'] -= food['protein']
                    self.daily_nutrition['carbs'] -= food['carbs']
                    self.daily_nutrition['fat'] -= food['fat']
                    
                    self.daily_nutrition['calories'] += updated_food['calories']
                    self.daily_nutrition['protein'] += updated_food['protein']
                    self.daily_nutrition['carbs'] += updated_food['carbs']
                    self.daily_nutrition['fat'] += updated_food['fat']
                    
                    # 更新记录
                    self.today_foods[i] = updated_food
                    break
            
            # 更新显示
            self.update_nutrition_display()
            self.update_food_list()
            self.save_food_data()
        
        edit_popup = FoodEditPopup(
            food_data=food_data,
            callback=update_callback
        )
        edit_popup.open()
    
    def delete_food_item(self, food_data):
        """删除食物项目"""
        # 确认弹窗
        confirm_popup = Popup(
            title='确认删除',
            size_hint=(0.6, 0.3)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f'确定要删除"{food_data["name"]}"吗？',
            font_name='Chinese'
        ))
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10)
        
        confirm_btn = Button(text='确定删除', background_color=[1, 0.3, 0.3, 1],
            font_name='Chinese'
        )
        confirm_btn.bind(on_press=lambda x: self.perform_delete(food_data, confirm_popup))
        btn_layout.add_widget(confirm_btn)
        
        cancel_btn = Button(text='取消',
            font_name='Chinese'
        )
        cancel_btn.bind(on_press=confirm_popup.dismiss)
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        confirm_popup.content = content
        confirm_popup.open()
    
    def perform_delete(self, food_data, popup):
        """执行删除操作"""
        popup.dismiss()
        
        # 从列表中移除
        for i, food in enumerate(self.today_foods):
            if food.get('timestamp') == food_data.get('timestamp'):
                # 更新营养统计
                self.daily_nutrition['calories'] -= food['calories']
                self.daily_nutrition['protein'] -= food['protein']
                self.daily_nutrition['carbs'] -= food['carbs']
                self.daily_nutrition['fat'] -= food['fat']
                
                # 移除记录
                self.today_foods.pop(i)
                break
        
        # 更新显示
        self.update_nutrition_display()
        self.update_food_list()
        self.save_food_data()
    
    def load_today_data(self):
        """加载今日数据"""
        try:
            app = App.get_running_app()
            if app and hasattr(app, 'storage'):
                today = datetime.now().strftime('%Y-%m-%d')
                data = app.storage.load_daily_food_data(today)
                
                self.today_foods = data.get('foods', [])
                self.daily_nutrition = data.get('nutrition', {
                    'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0
                })
                
                self.update_nutrition_display()
                self.update_food_list()
                
        except Exception as e:
            print(f"加载今日数据失败: {e}")
    
    def save_food_data(self):
        """保存食物数据"""
        try:
            app = App.get_running_app()
            if app and hasattr(app, 'storage'):
                today = datetime.now().strftime('%Y-%m-%d')
                data = {
                    'foods': self.today_foods,
                    'nutrition': self.daily_nutrition,
                    'date': today
                }
                print(f"🍎 食物屏幕：保存 {today} 的数据，共 {len(self.today_foods)} 个食物")
                print(f"📊 食物屏幕：营养数据 - 卡路里: {self.daily_nutrition['calories']}")
                app.storage.save_daily_food_data(today, data)
                print(f"✅ 食物屏幕：数据保存成功")
                
        except Exception as e:
            print(f"❌ 保存食物数据失败: {e}")
