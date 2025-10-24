#!/bin/bash
# 自动创建GitHub仓库并推送代码

echo "🚀 自动创建GitHub仓库并推送代码..."

# 检查是否已登录GitHub
if ! gh auth status >/dev/null 2>&1; then
    echo "❌ 请先登录GitHub CLI"
    echo "运行: gh auth login"
    exit 1
fi

# 创建仓库
echo "📦 创建GitHub仓库..."
gh repo create healthapp-python --public --description "Health App Python Kivy application with complete functionality"

# 添加远程仓库
echo "🔗 添加远程仓库..."
git remote add origin https://github.com/$(gh api user --jq .login)/healthapp-python.git

# 推送代码
echo "📤 推送代码到GitHub..."
git branch -M main
git push -u origin main

echo "✅ 完成！"
echo "🎯 下一步："
echo "1. 访问 https://github.com/$(gh api user --jq .login)/healthapp-python"
echo "2. 点击 'Actions' 标签"
echo "3. 选择 'Build Android APK' 工作流"
echo "4. 点击 'Run workflow' 按钮"
echo "5. 等待构建完成并下载APK"

