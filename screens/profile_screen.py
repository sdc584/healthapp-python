# -*- coding: utf-8 -*-
"""
个人资料屏幕
显示和编辑用户基本信息
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.app import App
from datetime import datetime

class ProfileScreen(Screen):
    """个人资料屏幕"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data = {}
        
        self.build_ui()
        
    def build_ui(self):
        """构建用户界面"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title = Label(
            text='个人资料',
            size_hint_y=0.1,
            font_size='24sp',
            color=[1, 1, 1, 1],
            font_name='Chinese'
        )
        main_layout.add_widget(title)
        
        # 用户信息区域
        info_section = BoxLayout(orientation='vertical', size_hint_y=0.6, spacing=20)
        
        # 基本信息网格
        info_grid = GridLayout(cols=2, spacing=15, size_hint_y=0.7)
        
        # 用户名
        info_grid.add_widget(Label(text='用户名:', font_size='18sp', halign='left',
            font_name='Chinese'
        ))
        self.username_label = Label(text='用户', font_size='18sp', halign='left', color=[0.8, 0.8, 1, 1],
            font_name='Chinese'
        )
        info_grid.add_widget(self.username_label)
        
        # 身高
        info_grid.add_widget(Label(text='身高:', font_size='18sp', halign='left',
            font_name='Chinese'
        ))
        self.height_label = Label(text='170 cm', font_size='18sp', halign='left', color=[0.8, 0.8, 1, 1],
            font_name='Chinese'
        )
        info_grid.add_widget(self.height_label)
        
        # 体重
        info_grid.add_widget(Label(text='体重:', font_size='18sp', halign='left',
            font_name='Chinese'
        ))
        self.weight_label = Label(text='60 kg', font_size='18sp', halign='left', color=[0.8, 0.8, 1, 1],
            font_name='Chinese'
        )
        info_grid.add_widget(self.weight_label)
        
        # BMI
        info_grid.add_widget(Label(text='BMI:', font_size='18sp', halign='left',
            font_name='Chinese'
        ))
        self.bmi_label = Label(text='20.8', font_size='18sp', halign='left', color=[0.8, 1, 0.8, 1],
            font_name='Chinese'
        )
        info_grid.add_widget(self.bmi_label)
        
        # 基础代谢
        info_grid.add_widget(Label(text='基础代谢:', font_size='18sp', halign='left',
            font_name='Chinese'
        ))
        self.bmr_label = Label(text='1400 kcal', font_size='18sp', halign='left', color=[1, 0.8, 0.8, 1],
            font_name='Chinese'
        )
        info_grid.add_widget(self.bmr_label)
        
        # 每日目标
        info_grid.add_widget(Label(text='卡路里目标:', font_size='18sp', halign='left',
            font_name='Chinese'
        ))
        self.calorie_goal_label = Label(text='2000 kcal', font_size='18sp', halign='left', color=[1, 1, 0.8, 1],
            font_name='Chinese'
        )
        info_grid.add_widget(self.calorie_goal_label)
        
        info_section.add_widget(info_grid)
        
        # 编辑按钮
        edit_btn = Button(
            text='编辑资料',
            size_hint_y=0.3,
            font_size='18sp',
            background_color=[0.2, 0.8, 0.2, 1],
            font_name='Chinese'
        )
        edit_btn.bind(on_press=self.edit_profile)
        info_section.add_widget(edit_btn)
        
        main_layout.add_widget(info_section)
        
        # 功能按钮区域
        button_section = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=10)
        
        # 设置按钮
        settings_btn = Button(
            text='应用设置',
            font_size='16sp',
            background_color=[0.5, 0.5, 1, 1],
            font_name='Chinese'
        )
        settings_btn.bind(on_press=self.show_settings)
        button_section.add_widget(settings_btn)
        
        # 数据统计按钮  
        stats_btn = Button(
            text='数据统计',
            font_size='16sp',
            background_color=[1, 0.5, 0.5, 1],
            font_name='Chinese'
        )
        stats_btn.bind(on_press=self.show_statistics)
        button_section.add_widget(stats_btn)
        
        # 关于按钮
        about_btn = Button(
            text='关于应用',
            font_size='16sp',
            background_color=[0.7, 0.7, 0.7, 1],
            font_name='Chinese'
        )
        about_btn.bind(on_press=self.show_about)
        button_section.add_widget(about_btn)
        
        main_layout.add_widget(button_section)
        
        self.add_widget(main_layout)
        
        # 设置进入事件
        self.bind(on_enter=self.load_profile)
    
    def load_profile(self, *args):
        """加载用户资料"""
        try:
            app = App.get_running_app()
            if app and hasattr(app, 'user_data'):
                self.user_data = app.user_data.copy()
                self.update_display()
            
        except Exception as e:
            print(f"加载用户资料失败: {e}")
    
    def update_display(self):
        """更新显示"""
        try:
            # 基本信息
            self.username_label.text = self.user_data.get('name', '用户')
            
            height = self.user_data.get('height', 170)
            weight = self.user_data.get('weight', 60)
            
            self.height_label.text = f'{height} cm'
            self.weight_label.text = f'{weight} kg'
            
            # 计算BMI
            bmi = self.calculate_bmi(height, weight)
            bmi_color = self.get_bmi_color(bmi)
            self.bmi_label.text = f'{bmi:.1f}'
            self.bmi_label.color = bmi_color
            
            # 计算基础代谢
            bmr = self.calculate_bmr(height, weight, self.user_data.get('age', 25), self.user_data.get('gender', 'male'))
            self.bmr_label.text = f'{bmr:.0f} kcal'
            
            # 卡路里目标
            calorie_goal = self.user_data.get('daily_calorie_goal', 2000)
            self.calorie_goal_label.text = f'{calorie_goal} kcal'
            
        except Exception as e:
            print(f"更新显示失败: {e}")
    
    def calculate_bmi(self, height, weight):
        """计算BMI"""
        try:
            height_m = height / 100  # 转换为米
            return weight / (height_m ** 2)
        except:
            return 0
    
    def get_bmi_color(self, bmi):
        """根据BMI获取颜色"""
        if bmi < 18.5:
            return [0.5, 0.5, 1, 1]  # 蓝色 - 偏瘦
        elif bmi < 24:
            return [0.5, 1, 0.5, 1]  # 绿色 - 正常
        elif bmi < 28:
            return [1, 1, 0.5, 1]    # 黄色 - 超重
        else:
            return [1, 0.5, 0.5, 1]  # 红色 - 肥胖
    
    def calculate_bmr(self, height, weight, age, gender):
        """计算基础代谢率"""
        try:
            if gender.lower() == 'male':
                # 男性公式
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                # 女性公式
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            return bmr
        except:
            return 1400
    
    def edit_profile(self, instance):
        """编辑资料"""
        popup = Popup(
            title='Edit Profile',
            size_hint=(0.9, 0.8)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # 添加中文标题
        title_label = Label(
            text='个人资料编辑',
            font_size='20sp',
            size_hint_y=None,
            height=40,
            color=[1, 1, 1, 1],
            font_name='Chinese'
        )
        content.add_widget(title_label)
        
        # 滚动区域
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView()
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # 用户名
        form_layout.add_widget(Label(text='用户名:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        name_input = TextInput(
            text=self.user_data.get('name', ''),
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        form_layout.add_widget(name_input)
        
        # 身高
        form_layout.add_widget(Label(text='身高(cm):',
            font_name='Chinese', size_hint_y=None, height=40))
        height_input = TextInput(
            text=str(self.user_data.get('height', 170)),
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        form_layout.add_widget(height_input)
        
        # 体重
        form_layout.add_widget(Label(text='体重(kg):',
            font_name='Chinese', size_hint_y=None, height=40))
        weight_input = TextInput(
            text=str(self.user_data.get('weight', 60)),
            input_filter='float',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        form_layout.add_widget(weight_input)
        
        # 年龄
        form_layout.add_widget(Label(text='年龄:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        age_input = TextInput(
            text=str(self.user_data.get('age', 25)),
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        form_layout.add_widget(age_input)
        
        # 性别
        form_layout.add_widget(Label(text='性别:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        from kivy.uix.spinner import Spinner
        gender_spinner = Spinner(
            text=self.user_data.get('gender', 'male'),
            values=['male', 'female'],
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        form_layout.add_widget(gender_spinner)
        
        # 卡路里目标
        form_layout.add_widget(Label(text='卡路里目标:', size_hint_y=None, height=40,
            font_name='Chinese'
        ))
        calorie_input = TextInput(
            text=str(self.user_data.get('daily_calorie_goal', 2000)),
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        form_layout.add_widget(calorie_input)
        
        scroll.add_widget(form_layout)
        content.add_widget(scroll)
        
        # 按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        
        cancel_btn = Button(text='取消',
            font_name='Chinese'
        )
        cancel_btn.bind(on_press=popup.dismiss)
        button_layout.add_widget(cancel_btn)
        
        save_btn = Button(text='保存', background_color=[0, 0.8, 0, 1],
            font_name='Chinese'
        )
        save_btn.bind(on_press=lambda x: self.save_profile({
            'name': name_input.text,
            'height': int(height_input.text or 170),
            'weight': float(weight_input.text or 60),
            'age': int(age_input.text or 25),
            'gender': gender_spinner.text,
            'daily_calorie_goal': int(calorie_input.text or 2000)
        }, popup))
        button_layout.add_widget(save_btn)
        
        content.add_widget(button_layout)
        
        popup.content = content
        popup.open()
    
    def save_profile(self, data, popup):
        """保存资料"""
        try:
            # 更新数据
            self.user_data.update(data)
            
            # 保存到应用
            app = App.get_running_app()
            if app:
                app.user_data.update(data)
                app.save_user_data()
            
            # 更新显示
            self.update_display()
            
            popup.dismiss()
            
            # 显示成功信息
            success_popup = Popup(
                title='保存成功',
                content=Label(text='个人资料已更新',
                    font_name='Chinese'
                ),
                size_hint=(0.6, 0.3)
            )
            success_popup.open()
            
        except Exception as e:
            error_popup = Popup(
                title='保存失败',
                content=Label(text=f'保存失败: {e}',
                    font_name='Chinese'
                ),
                size_hint=(0.6, 0.3)
            )
            error_popup.open()
    
    def show_settings(self, instance):
        """显示设置"""
        popup = Popup(
            title='Settings',
            size_hint=(0.8, 0.6)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(text='设置功能开发中...', font_size='18sp',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='• 通知设置',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='• 数据同步',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='• 隐私设置',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='• 单位设置',
            font_name='Chinese'
        ))
        
        close_btn = Button(text='关闭', size_hint_y=0.2,
            font_name='Chinese'
        )
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.content = content
        popup.open()
    
    def show_statistics(self, instance):
        """显示统计信息"""
        popup = Popup(
            title='Statistics',
            size_hint=(0.8, 0.7)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        try:
            app = App.get_running_app()
            if app and hasattr(app, 'storage'):
                # 获取统计数据
                stats = app.storage.get_user_statistics()
                
                stats_grid = GridLayout(cols=2, spacing=10)
                
                stats_grid.add_widget(Label(text='总跑步次数:',
                    font_name='Chinese'))
                stats_grid.add_widget(Label(text=f'{stats.get("total_runs", 0)} 次',
                    font_name='Chinese'))
                
                stats_grid.add_widget(Label(text='总跑步距离:',
                    font_name='Chinese'))
                stats_grid.add_widget(Label(text=f'{stats.get("total_distance", 0)/1000:.1f} km',
                    font_name='Chinese'))
                
                stats_grid.add_widget(Label(text='总运动时间:',
                    font_name='Chinese'))
                total_duration = stats.get("total_duration", 0)
                hours = int(total_duration // 3600)
                minutes = int((total_duration % 3600) // 60)
                stats_grid.add_widget(Label(text=f'{hours}h {minutes}m',
                    font_name='Chinese'))
                
                stats_grid.add_widget(Label(text='食物记录数:',
                    font_name='Chinese'))
                stats_grid.add_widget(Label(text=f'{stats.get("total_foods", 0)} 项',
                    font_name='Chinese'))
                
                content.add_widget(stats_grid)
            else:
                content.add_widget(Label(text='暂无统计数据',
                    font_name='Chinese'))
                
        except Exception as e:
            content.add_widget(Label(text=f'获取统计失败: {e}',
                font_name='Chinese'))
        
        close_btn = Button(text='关闭', size_hint_y=0.2,
            font_name='Chinese'
        )
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.content = content
        popup.open()
    
    def show_about(self, instance):
        """显示关于信息"""
        popup = Popup(
            title='About',
            size_hint=(0.8, 0.6)
        )
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(text='健康追踪应用', font_size='20sp', color=[1, 1, 1, 1],
            font_name='Chinese'
        ))
        content.add_widget(Label(text='版本 1.0.0', font_size='16sp',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='功能特性:',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='• GPS 跑步追踪',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='• 食物扫码识别',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='• 营养数据分析',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='• 历史记录查看',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='',
            font_name='Chinese'
        ))
        content.add_widget(Label(text='技术栈: Python + Kivy',
            font_name='Chinese'
        ))
        
        close_btn = Button(text='关闭', size_hint_y=0.15,
            font_name='Chinese'
        )
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.content = content
        popup.open()
