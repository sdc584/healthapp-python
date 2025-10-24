# 在Android Studio中打开Python Kivy项目

## 方法1：直接作为Python项目打开

1. **打开Android Studio**
2. **选择 "Open" 或 "Open an Existing Project"**
3. **浏览到项目目录**：`E:\app\HealthApp_Python`
4. **选择项目根目录**（包含main.py的目录）
5. **点击 "OK"**

## 方法2：配置Python解释器

1. **打开项目后，点击 File → Settings**
2. **选择 Project → Python Interpreter**
3. **点击齿轮图标 → Add**
4. **选择 "Existing Environment"**
5. **浏览到conda环境**：`E:\Anaconda3\envs\healthapp-python\python.exe`
6. **点击 "OK"**

## 方法3：安装Python插件（如果需要）

1. **File → Settings → Plugins**
2. **搜索 "Python"**
3. **安装 "Python" 插件**
4. **重启Android Studio**

## 运行Python应用

1. **右键点击 main.py**
2. **选择 "Run 'main'"**
3. **或者点击工具栏的运行按钮**

## 项目结构说明

```
HealthApp_Python/
├── main.py                 # 主程序入口
├── screens/               # 屏幕模块
│   ├── run_screen.py      # 跑步追踪
│   ├── food_screen.py     # 饮食记录
│   ├── today_screen.py    # 今日概览
│   ├── history_screen.py  # 历史记录
│   └── profile_screen.py  # 个人资料
├── services/              # 服务模块
├── utils/                 # 工具模块
└── data/                  # 数据存储
```

## 注意事项

- 确保使用正确的Python解释器（healthapp-python环境）
- Kivy应用会在桌面运行，不是Android模拟器
- 如需打包为Android APK，需要使用Buildozer
