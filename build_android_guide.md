# 将Python Kivy应用打包为Android APK

## 方法1：使用Buildozer（推荐）

### 1. 安装Buildozer
```bash
# 在WSL或Linux环境中
pip install buildozer
```

### 2. 初始化Buildozer配置
```bash
buildozer init
```

### 3. 配置buildozer.spec文件
```ini
[app]
title = 健康追踪应用
package.name = healthapp
package.domain = com.healthapp

[buildozer]
log_level = 2
warn_on_root = 1

[android]
api = 30
minapi = 21
ndk = 25b
sdk = 30
```

### 4. 构建APK
```bash
buildozer android debug
```

## 方法2：使用Python-for-Android

### 1. 安装p4a
```bash
pip install python-for-android
```

### 2. 创建APK
```bash
p4a apk --private . --package=com.healthapp --name="健康追踪" --version=1.0
```

## 方法3：使用KivyMD的Android模板

### 1. 使用KivyMD模板
```bash
git clone https://github.com/kivymd/KivyMD.git
cd KivyMD/examples/android_template
```

### 2. 替换代码
将您的Python代码复制到模板中

## 注意事项

1. **需要Linux/WSL环境**：Buildozer在Windows上需要WSL
2. **依赖管理**：确保所有Python依赖都支持Android
3. **权限配置**：在AndroidManifest.xml中配置必要权限
4. **性能优化**：Android环境下的性能考虑

## 当前状态

- ✅ Python应用在桌面正常运行
- ❌ 尚未打包为Android APK
- 🔄 需要额外步骤才能在模拟器中运行
