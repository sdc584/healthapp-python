#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用启动脚本
用于快速启动和测试健康追踪应用
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖包"""
    print("📦 检查Python依赖...")
    
    required_packages = [
        'kivy',
        'requests',
        'plyer'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️ 缺少依赖包: {', '.join(missing_packages)}")
        print("正在自动安装...")
        
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                '-r', 'requirements.txt'
            ], check=True)
            print("✅ 依赖安装完成")
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败，请手动运行:")
            print("pip install -r requirements.txt")
            return False
    
    return True

def create_data_directory():
    """创建数据目录"""
    data_dir = Path('data')
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
        print("📁 创建数据目录: data/")
        
        # 创建子目录
        (data_dir / 'runs').mkdir(exist_ok=True)
        (data_dir / 'foods').mkdir(exist_ok=True)

def show_app_info():
    """显示应用信息"""
    print("🏃‍♂️ 健康追踪应用 - Python版本")
    print("=" * 50)
    print("📱 功能特性:")
    print("  • GPS跑步追踪")
    print("  • 食物扫码识别")
    print("  • 营养数据分析")
    print("  • 历史记录查看")
    print("  • 云端数据同步")
    print()
    print("🛠️ 技术栈: Python + Kivy")
    print("📁 项目目录:", Path().absolute())
    print("=" * 50)
    print()

def run_desktop():
    """桌面模式运行"""
    print("🖥️ 启动桌面版本...")
    
    # 检查main.py是否存在
    if not Path('main.py').exists():
        print("❌ 找不到main.py文件")
        return False
    
    try:
        # 启动应用
        subprocess.run([sys.executable, 'main.py'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 应用启动失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ 应用已关闭")
        return True

def show_menu():
    """显示菜单"""
    print("请选择运行模式:")
    print("1. 🖥️  桌面运行 (推荐)")
    print("2. 📱 Android构建")
    print("3. 🔍 环境检查")
    print("4. 📖 查看说明")
    print("0. 🚪 退出")
    print()
    
    try:
        choice = input("请输入选择 (0-4): ").strip()
        return choice
    except KeyboardInterrupt:
        print("\n👋 再见!")
        return '0'

def build_android():
    """Android构建"""
    print("📱 Android构建...")
    
    try:
        # 检查构建脚本
        if Path('build_android.py').exists():
            subprocess.run([sys.executable, 'build_android.py', '--check'])
            
            print("\n构建选项:")
            print("1. 调试版APK")
            print("2. 发布版APK") 
            print("3. 返回主菜单")
            
            build_choice = input("请选择 (1-3): ").strip()
            
            if build_choice == '1':
                subprocess.run([sys.executable, 'build_android.py', '--debug'])
            elif build_choice == '2':
                subprocess.run([sys.executable, 'build_android.py', '--release'])
            
        else:
            print("❌ 找不到构建脚本 build_android.py")
            
    except Exception as e:
        print(f"❌ 构建失败: {e}")

def check_environment():
    """环境检查"""
    print("🔍 环境检查...")
    print()
    
    # Python版本
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Python版本: {python_version}")
    
    if sys.version_info >= (3, 8):
        print("✅ Python版本符合要求")
    else:
        print("❌ Python版本需要3.8或更高")
    
    print()
    
    # 检查依赖
    check_dependencies()
    
    print()
    
    # 检查文件结构
    print("📁 检查项目文件...")
    required_files = [
        'main.py',
        'requirements.txt',
        'buildozer.spec',
        'screens/run_screen.py',
        'screens/food_screen.py',
        'services/gps_service.py',
        'utils/storage_manager.py'
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    
    print()
    
    # 系统信息
    print("💻 系统信息:")
    print(f"操作系统: {sys.platform}")
    print(f"当前目录: {Path().absolute()}")

def show_documentation():
    """显示文档"""
    print("📖 应用说明")
    print("=" * 50)
    
    doc_text = """
🏃‍♂️ 健康追踪应用 - 使用指南

📱 主要功能:

1. 跑步追踪 (Run Screen)
   • 点击"开始跑步"开始GPS追踪
   • 实时显示距离、时间、配速
   • 支持暂停、恢复、停止功能
   • 自动保存跑步记录

2. 饮食记录 (Food Screen)  
   • 点击"扫描条形码"识别食物
   • 手动添加食物和营养信息
   • 支持早中晚餐分类
   • 自动计算营养统计

3. 今日总览 (Today Screen)
   • 卡路里摄入环形图
   • 三大营养素进度条
   • 今日运动数据汇总

4. 历史记录 (History Screen)
   • 日历视图查看历史
   • 跑步和饮食记录详情
   • 数据筛选和统计

5. 个人资料 (Profile Screen)
   • 编辑个人信息
   • BMI和基础代谢计算
   • 应用设置和数据统计

🎮 操作提示:
• 首次使用需要授予GPS和相机权限
• 数据自动保存到本地
• 支持离线使用，联网后可同步
• 点击底部导航栏切换功能

🔧 技术特性:
• 跨平台运行 (Windows/Linux/Mac/Android)
• 本地数据存储，隐私安全
• 开源免费，可自定义扩展
• 集成免费食物API数据库
"""
    
    print(doc_text)
    
    input("按Enter键返回菜单...")

def main():
    """主函数"""
    # 显示应用信息
    show_app_info()
    
    # 创建数据目录
    create_data_directory()
    
    # 主循环
    while True:
        choice = show_menu()
        
        if choice == '1':
            # 检查依赖
            if not check_dependencies():
                continue
            
            # 运行桌面版
            run_desktop()
            
        elif choice == '2':
            # Android构建
            build_android()
            
        elif choice == '3':
            # 环境检查
            check_environment()
            input("\n按Enter键继续...")
            
        elif choice == '4':
            # 查看说明
            show_documentation()
            
        elif choice == '0':
            print("👋 感谢使用健康追踪应用！")
            break
            
        else:
            print("❌ 无效选择，请重新输入")
        
        print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 应用已退出")
    except Exception as e:
        print(f"\n💥 发生错误: {e}")
        print("请检查应用配置或联系开发者")
