@echo off
echo 正在初始化 Git 仓库...
git init

echo 正在添加文件...
git add .

echo 正在提交...
git commit -m "Initial commit: Crypto exchange coverage analysis app"

echo 请输入你的 GitHub 仓库地址（例如：https://github.com/yourusername/crypto-exchange-coverage.git）
set /p REPO_URL="git@github.com:fejinrunkasoon/crypto-exchange-future-coverage.git "

echo 正在添加远程仓库...
git remote add origin %REPO_URL%

echo 正在推送到 GitHub...
git branch -M main
git push -u origin main

echo 完成！
pause