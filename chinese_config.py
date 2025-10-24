# -*- coding: utf-8 -*-
"""
中文字体配置模块
统一管理应用的中文字体设置
"""

import os
from kivy.core.text import LabelBase
from kivy.config import Config
from kivy.resources import resource_add_path

def setup_chinese_display():
    """配置中文显示支持"""
    
    # 设置Kivy配置
    Config.set('graphics', 'width', '1200')
    Config.set('graphics', 'height', '800')
    Config.set('graphics', 'minimum_width', '800')
    Config.set('graphics', 'minimum_height', '600')
    
    # 注册中文字体
    register_chinese_fonts()

def register_chinese_fonts():
    """注册中文字体"""
    try:
        # Windows系统字体路径
        font_configs = [
            {
                'name': 'Chinese',
                'paths': [
                    'C:/Windows/Fonts/msyh.ttc',      # 微软雅黑
                    'C:/Windows/Fonts/simhei.ttf',    # 黑体  
                    'C:/Windows/Fonts/simsun.ttc',    # 宋体
                    'C:/Windows/Fonts/simkai.ttf',    # 楷体
                ]
            },
            {
                'name': 'ChineseBold', 
                'paths': [
                    'C:/Windows/Fonts/msyhbd.ttc',    # 微软雅黑粗体
                    'C:/Windows/Fonts/simhei.ttf',    # 黑体
                ]
            }
        ]
        
        default_font_path = None
        
        for config in font_configs:
            name = config['name']
            paths = config['paths']
            
            for font_path in paths:
                if os.path.exists(font_path):
                    LabelBase.register(
                        name=name, 
                        fn_regular=font_path
                    )
                    print(f"✅ {name}字体注册成功: {font_path}")
                    
                    # 记录第一个成功的字体作为默认字体
                    if name == 'Chinese' and default_font_path is None:
                        default_font_path = font_path
                    break
            else:
                print(f"⚠️  未找到{name}字体")
        
        # 注册默认字体，覆盖Kivy的默认字体
        if default_font_path:
            try:
                LabelBase.register(
                    name='DroidSans',
                    fn_regular=default_font_path
                )
                print(f"✅ 设置默认字体为中文字体: {default_font_path}")
            except Exception as e:
                print(f"⚠️ 设置默认字体失败: {e}")
                
    except Exception as e:
        print(f"字体注册失败: {e}")

def get_chinese_font_name():
    """获取中文字体名称"""
    return 'Chinese'

def get_chinese_bold_font_name():
    """获取中文粗体字体名称"""
    return 'ChineseBold'
