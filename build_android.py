#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android构建脚本
自动化构建Android APK的工具脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """检查构建环境要求"""
    print("🔍 检查构建环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本需要3.8或更高")
        return False
    
    # 检查buildozer是否安装
    try:
        subprocess.run(['buildozer', '--version'], 
                      capture_output=True, check=True)
        print("✅ Buildozer已安装")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Buildozer未安装，请运行: pip install buildozer")
        return False
    
    # 检查Java
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True)
        print("✅ Java环境正常")
    except FileNotFoundError:
        print("⚠️ Java未安装，请安装JDK 8或11")
    
    return True

def setup_android_sdk():
    """设置Android SDK"""
    print("📱 配置Android SDK...")
    
    # 检查Android SDK
    android_home = os.environ.get('ANDROID_HOME')
    if not android_home:
        print("⚠️ ANDROID_HOME环境变量未设置")
        print("请设置为Android SDK路径，例如:")
        print("Windows: C:\\Users\\用户名\\AppData\\Local\\Android\\Sdk")
        print("Linux/Mac: ~/Android/Sdk")
        return False
    
    if not os.path.exists(android_home):
        print(f"❌ Android SDK路径不存在: {android_home}")
        return False
    
    print(f"✅ Android SDK路径: {android_home}")
    return True

def clean_build():
    """清理构建目录"""
    print("🧹 清理构建目录...")
    
    dirs_to_clean = ['.buildozer', 'bin']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ 已清理: {dir_name}")
            except Exception as e:
                print(f"⚠️ 清理失败 {dir_name}: {e}")

def install_dependencies():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                      check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def build_debug():
    """构建调试版APK"""
    print("🔨 构建调试版APK...")
    
    try:
        # 初始化buildozer（如果需要）
        if not os.path.exists('.buildozer'):
            print("🆕 初始化Buildozer...")
            subprocess.run(['buildozer', 'init'], check=True)
        
        # 构建调试版
        subprocess.run(['buildozer', 'android', 'debug'], check=True)
        
        # 检查输出文件
        apk_files = list(Path('bin').glob('*.apk'))
        if apk_files:
            apk_file = apk_files[0]
            print(f"✅ APK构建成功: {apk_file}")
            print(f"📁 文件大小: {apk_file.stat().st_size / (1024*1024):.1f} MB")
            return str(apk_file)
        else:
            print("❌ 未找到生成的APK文件")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return None

def build_release():
    """构建发布版APK"""
    print("🚀 构建发布版APK...")
    
    try:
        subprocess.run(['buildozer', 'android', 'release'], check=True)
        
        # 检查输出文件
        apk_files = list(Path('bin').glob('*release*.apk'))
        if apk_files:
            apk_file = apk_files[0]
            print(f"✅ 发布版APK构建成功: {apk_file}")
            return str(apk_file)
        else:
            print("❌ 未找到生成的发布版APK文件")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 发布版构建失败: {e}")
        return None

def install_apk(apk_path):
    """安装APK到设备"""
    if not apk_path or not os.path.exists(apk_path):
        print("❌ APK文件不存在")
        return False
    
    print("📱 安装APK到设备...")
    
    try:
        # 检查设备连接
        result = subprocess.run(['adb', 'devices'], 
                              capture_output=True, text=True)
        
        if 'device' not in result.stdout:
            print("❌ 未检测到Android设备")
            print("请确保:")
            print("1. 设备已连接并开启USB调试")
            print("2. 已安装adb工具")
            return False
        
        # 安装APK
        subprocess.run(['adb', 'install', '-r', apk_path], check=True)
        print("✅ APK安装成功")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ APK安装失败: {e}")
        return False

def show_help():
    """显示帮助信息"""
    print("""
🏃‍♂️ 健康追踪应用 - Android构建工具

用法:
    python build_android.py [选项]

选项:
    --help, -h      显示此帮助信息
    --clean         清理构建目录
    --check         检查构建环境
    --debug         构建调试版APK
    --release       构建发布版APK
    --install       安装APK到设备
    --all           完整构建流程

示例:
    python build_android.py --debug          # 仅构建调试版
    python build_android.py --all            # 完整流程
    python build_android.py --clean --debug  # 清理后构建
    """)

def main():
    """主函数"""
    args = sys.argv[1:]
    
    if not args or '--help' in args or '-h' in args:
        show_help()
        return
    
    print("🏃‍♂️ 健康追踪应用 - Android构建工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists('main.py'):
        print("❌ 请在项目根目录运行此脚本")
        return
    
    # 执行选项
    if '--check' in args:
        if not check_requirements():
            return
        if not setup_android_sdk():
            return
        print("✅ 环境检查通过")
    
    if '--clean' in args:
        clean_build()
    
    if '--all' in args or '--debug' in args or '--release' in args:
        # 检查环境
        if not check_requirements():
            return
        
        if not setup_android_sdk():
            return
        
        # 安装依赖
        if not install_dependencies():
            return
        
        # 构建APK
        apk_path = None
        
        if '--release' in args:
            apk_path = build_release()
        else:
            apk_path = build_debug()
        
        if apk_path and ('--install' in args or '--all' in args):
            install_apk(apk_path)
        
        if apk_path:
            print("\n🎉 构建完成！")
            print(f"📁 APK文件: {apk_path}")
            print("\n📱 安装命令:")
            print(f"adb install -r {apk_path}")
        else:
            print("\n❌ 构建失败")
    
    elif '--install' in args:
        # 查找现有APK文件
        apk_files = list(Path('bin').glob('*.apk'))
        if apk_files:
            install_apk(str(apk_files[0]))
        else:
            print("❌ 未找到APK文件，请先构建")

if __name__ == '__main__':
    main()


