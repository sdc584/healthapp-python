# 🏃‍♂️ 健康追踪应用 - Python版本

使用纯Python + Kivy框架开发的跨平台移动健康应用，支持跑步追踪和饮食记录功能。

## 📱 功能特性

### ✅ 核心功能
- **🏃‍♂️ 跑步追踪**: 实时GPS定位、路径记录、配速计算
- **🍎 饮食记录**: 条形码扫描、手动录入、营养分析
- **📊 数据统计**: 今日总览、历史记录、个人资料
- **☁️ 云端同步**: Firebase数据同步（可选）
- **📱 跨平台**: 支持Android、iOS、Windows、Linux

### 🛠️ 技术栈
- **Python 3.8+**: 核心开发语言
- **Kivy 2.1.0**: 跨平台GUI框架
- **Plyer**: 平台API访问（GPS、相机等）
- **Requests**: HTTP请求和API调用
- **Firebase**: 云端数据存储和同步
- **Open Food Facts API**: 免费食物数据库

## 📁 项目结构

```
HealthApp_Python/
├── main.py                 # 应用入口
├── requirements.txt        # 依赖包列表
├── buildozer.spec         # Android构建配置
├── README.md              # 项目说明
├── screens/               # 界面屏幕
│   ├── run_screen.py      # 跑步追踪界面
│   ├── food_screen.py     # 饮食记录界面
│   ├── today_screen.py    # 今日总览界面
│   ├── history_screen.py  # 历史记录界面
│   └── profile_screen.py  # 个人资料界面
├── services/              # 服务模块
│   ├── gps_service.py     # GPS定位服务
│   ├── food_api_service.py # 食物API服务
│   └── firebase_service.py # Firebase云服务
├── utils/                 # 工具模块
│   └── storage_manager.py # 本地数据存储
└── data/                  # 数据存储目录
    ├── user_data.json     # 用户信息
    ├── runs/              # 跑步记录
    └── foods/             # 饮食记录
```

## 🚀 快速开始

### 1. 环境准备

**Python环境**:
```bash
# Python 3.8+
python --version

# 安装依赖
pip install -r requirements.txt
```

**Android开发环境** (如需构建APK):
- Android Studio
- Android SDK (API 33)
- Java Development Kit (JDK 8/11)

### 2. 桌面运行

```bash
# 直接运行
python main.py
```

### 3. Android构建

**安装Buildozer**:
```bash
pip install buildozer
```

**构建APK**:
```bash
# 初始化构建环境
buildozer init

# 构建调试版APK
buildozer android debug

# 构建发布版APK
buildozer android release
```

### 4. Android Studio运行

1. **打开Android Studio**
2. **导入项目**: 选择 `HealthApp_Python` 文件夹
3. **配置SDK**: 确保Android SDK已正确配置
4. **构建APK**: 
   ```bash
   cd HealthApp_Python
   buildozer android debug
   ```
5. **安装到设备**: 
   ```bash
   adb install bin/healthapp-1.0.0-armeabi-v7a-debug.apk
   ```

## 📋 详细功能说明

### 🏃‍♂️ 跑步追踪模块

**功能特性**:
- 实时GPS位置追踪
- 跑步路径地图显示
- 距离、时间、配速计算
- 跑步记录保存和查看
- 卡路里消耗估算

**技术实现**:
- 使用Plyer GPS API获取位置
- 自定义地图组件绘制路径
- Haversine公式计算距离
- 本地JSON存储跑步数据

### 🍎 饮食记录模块

**功能特性**:
- 条形码扫描食物识别
- 手动添加食物信息
- 营养成分自动计算
- 餐次分类管理（早中晚餐）
- 每日营养统计

**技术实现**:
- Plyer Camera API条码扫描
- Open Food Facts API食物查询
- 自定义营养计算算法
- 份量和份数灵活调整

### 📊 数据统计模块

**功能特性**:
- 今日卡路里环形图
- 三大营养素进度条
- 历史记录日历视图
- 个人健康指标计算
- 数据导出和备份

**技术实现**:
- Canvas自定义绘制图表
- JSON本地数据存储
- Firebase云端同步
- BMI和基础代谢计算

## ⚙️ 配置说明

### Firebase配置

编辑 `services/firebase_service.py`:

```python
self.config = {
    'apiKey': 'your_api_key',
    'authDomain': 'your_project.firebaseapp.com',
    'databaseURL': 'https://your_project.firebaseio.com',
    'projectId': 'your_project',
    'storageBucket': 'your_project.appspot.com',
    'messagingSenderId': '123456789012',
    'appId': '1:123456789012:android:abcdef123456'
}
```

### Android权限配置

`buildozer.spec` 中已配置必要权限:
- `ACCESS_FINE_LOCATION`: GPS定位
- `CAMERA`: 相机扫码
- `INTERNET`: 网络访问
- `WRITE_EXTERNAL_STORAGE`: 数据存储

## 🔧 开发说明

### 添加新功能

1. **创建新屏幕**: 在 `screens/` 目录添加新的屏幕类
2. **添加导航**: 在 `main.py` 中注册新屏幕
3. **数据处理**: 使用 `utils/storage_manager.py` 处理本地数据
4. **云端同步**: 通过 `services/firebase_service.py` 同步数据

### 自定义样式

Kivy使用Python代码定义UI样式，可以在各个屏幕文件中自定义：

```python
button = Button(
    text='按钮',
    background_color=[0.2, 0.6, 1, 1],  # RGBA颜色
    font_size='18sp'
)
```

### 调试技巧

**桌面调试**:
```bash
# 启用详细日志
python main.py --verbose
```

**Android调试**:
```bash
# 查看应用日志
adb logcat | grep python

# 构建调试版本
buildozer android debug
```

## 🐛 常见问题

### Q: GPS在模拟器中不工作？
A: GPS功能需要真机测试，模拟器中会使用模拟数据。

### Q: 条码扫描权限被拒绝？
A: 确保在Android设置中授予应用相机权限。

### Q: 构建APK失败？
A: 检查Android SDK路径和Java版本是否正确配置。

### Q: 数据无法同步？
A: 检查网络连接和Firebase配置是否正确。

## 📞 技术支持

### 开发环境要求
- Python 3.8+
- Android SDK API 33
- 4GB+ RAM
- 10GB+ 存储空间

### 性能优化建议
1. 使用真机测试GPS功能
2. 定期清理本地数据缓存
3. 优化图像资源大小
4. 启用ProGuard代码混淆

### 部署建议
1. 配置正确的签名密钥
2. 测试多种Android版本
3. 优化APK大小
4. 提交Google Play审核

## 🎯 未来规划

### 短期目标
- [ ] 集成更多食物数据库
- [ ] 添加运动类型识别
- [ ] 实现数据图表可视化
- [ ] 支持多语言界面

### 长期规划
- [ ] 添加社交分享功能
- [ ] 集成智能手表数据
- [ ] AI健康建议推荐
- [ ] 云端AI图像识别

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

---

**🎉 恭喜！现在您拥有了一个功能完整的Python健康追踪应用！**

如有任何问题或建议，请提交Issue或联系开发团队。


