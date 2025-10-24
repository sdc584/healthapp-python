@echo off
echo 🚀 GitHub仓库推送脚本
echo.

echo 📋 请按照以下步骤操作：
echo.
echo 1. 打开浏览器，访问 https://github.com
echo 2. 登录您的GitHub账户
echo 3. 点击右上角的 "+" 号，选择 "New repository"
echo 4. 仓库名称：healthapp-python
echo 5. 描述：Health App Python Kivy application
echo 6. 选择 "Public"（公开）
echo 7. 不要勾选 "Add a README file"
echo 8. 点击 "Create repository"
echo.
echo 9. 复制仓库URL（类似：https://github.com/YOUR_USERNAME/healthapp-python.git）
echo.

set /p REPO_URL="请输入您的GitHub仓库URL: "

if "%REPO_URL%"=="" (
    echo ❌ 未输入仓库URL，退出
    pause
    exit /b 1
)

echo.
echo 🔗 添加远程仓库...
git remote add origin %REPO_URL%

echo.
echo 📤 推送代码到GitHub...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ 代码推送成功！
    echo.
    echo 🎯 下一步：
    echo 1. 访问您的GitHub仓库页面
    echo 2. 点击 "Actions" 标签
    echo 3. 选择 "Build Android APK" 工作流
    echo 4. 点击 "Run workflow" 按钮
    echo 5. 等待构建完成（约10-15分钟）
    echo 6. 下载生成的APK文件
) else (
    echo.
    echo ❌ 推送失败，请检查：
    echo - GitHub用户名是否正确
    echo - 仓库URL是否正确
    echo - 是否有推送权限
)

echo.
pause

