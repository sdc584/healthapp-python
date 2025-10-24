@echo off
echo 🚀 自动创建GitHub仓库并推送代码...

REM 检查GitHub CLI是否可用
gh --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ GitHub CLI不可用，使用手动方法
    goto :manual
)

REM 检查是否已登录
gh auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 请先登录GitHub CLI
    echo 运行: gh auth login
    pause
    exit /b 1
)

echo 📦 创建GitHub仓库...
gh repo create healthapp-python --public --description "Health App Python Kivy application with complete functionality"

echo 🔗 添加远程仓库...
for /f "tokens=*" %%i in ('gh api user --jq .login') do set GITHUB_USER=%%i
git remote add origin https://github.com/%GITHUB_USER%/healthapp-python.git

echo 📤 推送代码到GitHub...
git branch -M main
git push -u origin main

echo ✅ 完成！
echo 🎯 下一步：
echo 1. 访问 https://github.com/%GITHUB_USER%/healthapp-python
echo 2. 点击 'Actions' 标签
echo 3. 选择 'Build Android APK' 工作流
echo 4. 点击 'Run workflow' 按钮
echo 5. 等待构建完成并下载APK
goto :end

:manual
echo 📋 手动操作步骤：
echo 1. 访问 https://github.com/new
echo 2. 仓库名称: healthapp-python
echo 3. 选择 Public
echo 4. 点击 Create repository
echo 5. 复制仓库URL
echo 6. 运行: git remote set-url origin YOUR_REPO_URL
echo 7. 运行: git push -u origin main

:end
pause

