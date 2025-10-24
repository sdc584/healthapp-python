# -*- coding: utf-8 -*-
"""
UI辅助工具
提供中文友好的UI组件
"""

from kivy.uix.label import Label
from kivy.uix.button import Button
from chinese_config import get_chinese_font_name

def ChineseLabel(text='', **kwargs):
    """中文Label组件"""
    kwargs.setdefault('font_name', get_chinese_font_name())
    return Label(text=text, **kwargs)

def ChineseButton(text='', **kwargs):
    """中文Button组件"""
    kwargs.setdefault('font_name', get_chinese_font_name())
    return Button(text=text, **kwargs)

def patch_kivy_defaults():
    """修补Kivy的默认组件，使其支持中文"""
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    
    # 保存原始的初始化方法
    original_label_init = Label.__init__
    original_button_init = Button.__init__
    
    def patched_label_init(self, **kwargs):
        # 如果没有指定字体，使用中文字体
        if 'font_name' not in kwargs:
            kwargs['font_name'] = get_chinese_font_name()
        original_label_init(self, **kwargs)
    
    def patched_button_init(self, **kwargs):
        # 如果没有指定字体，使用中文字体
        if 'font_name' not in kwargs:
            kwargs['font_name'] = get_chinese_font_name()
        original_button_init(self, **kwargs)
    
    # 替换默认初始化方法
    Label.__init__ = patched_label_init
    Button.__init__ = patched_button_init
    
    print("✅ UI组件中文字体补丁已应用")



