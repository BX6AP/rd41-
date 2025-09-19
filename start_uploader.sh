#!/bin/bash

# SondeHub 上傳器啟動腳本

echo "🚀 啟動 SondeHub 上傳器服務..."

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安裝，請先安裝 Python3"
    exit 1
fi

# 檢查必要的 Python 套件
echo "📦 檢查 Python 套件..."
python3 -c "import flask, requests, flask_cors" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 安裝必要的 Python 套件..."
    pip3 install flask requests flask-cors
fi

# 啟動服務
echo "🌟 啟動 Web 服務..."
echo "📡 服務地址: http://localhost:5001"
echo "🔍 健康檢查: http://localhost:5001/api/health"
echo ""
echo "按 Ctrl+C 停止服務"
echo ""

python3 sondehub_uploader_server.py
