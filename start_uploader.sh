#!/bin/bash

# SondeHub Uploader Startup Script
# Created: 2025-01-17
# Last modified: 2025-01-20
# Note: This script has been tested on Raspberry Pi 4 with Python 3.9

echo "🚀 Starting SondeHub Uploader Service..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed, please install Python3 first"
    exit 1
fi

# Check required Python packages
echo "📦 Checking Python packages..."
python3 -c "import flask, requests, flask_cors" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installing required Python packages..."
    pip3 install flask requests flask-cors
fi

# Start service
echo "🌟 Starting Web Service..."
echo "📡 Service URL: http://localhost:5001"
echo "🔍 Health Check: http://localhost:5001/api/health"
echo ""
echo "Press Ctrl+C to stop service"
echo ""

python3 sondehub_uploader_server.py
