#!/usr/bin/env python3
"""
SondeHub 上傳器後端服務
提供 API 端點用於解碼 Base64 編碼的 gzip 數據並上傳到 SondeHub
"""

import base64
import gzip
import json
import requests
import logging
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SondeHub API 端點
SONDEHUB_URL = "https://api.v2.sondehub.org/sondes/telemetry"

@app.route('/')
def index():
    """主頁面"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SondeHub 上傳器</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .section { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: #fafafa; }
        h2 { color: #2c3e50; margin-bottom: 15px; }
        textarea { width: 100%; height: 150px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: monospace; font-size: 12px; }
        button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 14px; }
        button:hover { background: #2980b9; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .info { background: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .json-display { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 12px; white-space: pre-wrap; max-height: 400px; overflow-y: auto; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-card { background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #3498db; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .stat-card h4 { margin: 0 0 10px 0; color: #2c3e50; }
        .stat-card .value { font-size: 1.5em; font-weight: bold; color: #3498db; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 SondeHub 上傳器</h1>
        
        <div class="section">
            <h2>📥 輸入 Base64 數據</h2>
            <textarea id="base64Input" placeholder="請貼上 Base64 編碼的 gzip 數據...">H4sIAJwfzGgC/4WST4/TMBDFv0qVc2v5T5zEvcFlT0gVXQFitbKmzWTXUuIE2+myQnx3PC4rijiQXOLnn9+8yfjhRxXnIb1AQOthwmq/qQL0bo6z79HCmmYbvlfbzR/sgiG62RMpWMfk7oQJGkLWZZyhx2DPMI7RPRXm/Zfm3cHeg1vQWfUXtszRpavVg9SM1w3vuu1GSMG0aLWstxv+eHsAfELvgWzJKLkJbcAzugv2JEou9Y6bnejuhd5zua81M6b5SvAEfh3gnNaAgdhP4CKMUHxel9L4x2MtSqsYHIykfBZaCsFNUdfTLbg73h1I7iEhBflf/RFSRqRiouFckVAaF5IzoZu8hpEAbZiSKndeDeE6D6HKMuG0kEHDZF49r5PrXXrNCmc8C0vAGHNvdIBzw2qyPEEiT1WICClSgfx5wdFe8vcup1H51ebtedt9JpI1Whptct5Wa14bqov5cvgnqtIYpjveKtF2vJNN6WkI+G1Ff6ZcNZd5pC1V9vTHpSzJB3tGn0rQTGSgodGXDQxhJvJNWZappFctxQqxFnYC508zhP46hg+1rKt/9uzwcp2G5uVentYQk6UhFXetVfHD4fYGVneHY/Vbvp0pyT8ffwHitlDeKAMAAA==</textarea>
            <br>
            <button onclick="decodeAndDisplay()">🔍 解碼並顯示</button>
            <button onclick="uploadToSondeHub()">🚀 上傳到 SondeHub</button>
            <button onclick="clearAll()">🗑️ 清除</button>
        </div>

        <div class="section">
            <h2>📊 解碼結果</h2>
            <div id="decodeResult" class="info">點擊「解碼並顯示」按鈕開始...</div>
        </div>

        <div class="section">
            <h2>📋 JSON 數據</h2>
            <div id="jsonDisplay" class="json-display" style="display: none;">解碼後將顯示 JSON 數據...</div>
        </div>

        <div class="section">
            <h2>📈 上傳狀態</h2>
            <div id="uploadStatus" class="info">等待上傳...</div>
        </div>

        <div class="stats" id="stats" style="display: none;">
            <div class="stat-card">
                <h4>原始大小</h4>
                <div class="value" id="originalSize">-</div>
            </div>
            <div class="stat-card">
                <h4>Base64 大小</h4>
                <div class="value" id="base64Size">-</div>
            </div>
            <div class="stat-card">
                <h4>數據包數量</h4>
                <div class="value" id="packetCount">-</div>
            </div>
            <div class="stat-card">
                <h4>探空儀 ID</h4>
                <div class="value" id="sondeId">-</div>
            </div>
        </div>
    </div>

    <script>
        let decodedData = null;

        async function decodeAndDisplay() {
            const base64Input = document.getElementById('base64Input').value.trim();
            const decodeResult = document.getElementById('decodeResult');
            const jsonDisplay = document.getElementById('jsonDisplay');
            const stats = document.getElementById('stats');

            if (!base64Input) {
                showMessage(decodeResult, '請輸入 Base64 數據', 'error');
                return;
            }

            try {
                const response = await fetch('/api/decode', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ base64_data: base64Input })
                });

                const result = await response.json();

                if (result.success) {
                    decodedData = result.data;
                    
                    const message = `✅ 解碼成功！
Base64 大小: ${base64Input.length} 字元
解壓後大小: ${result.decompressed_size} 字元
數據包數量: ${result.packet_count}`;

                    showMessage(decodeResult, message, 'success');
                    
                    // 顯示 JSON
                    jsonDisplay.textContent = JSON.stringify(result.data, null, 2);
                    jsonDisplay.style.display = 'block';
                    
                    // 更新統計
                    updateStats(result.data, result.decompressed_size, base64Input.length);
                } else {
                    showMessage(decodeResult, `❌ 解碼失敗: ${result.error}`, 'error');
                }

            } catch (error) {
                showMessage(decodeResult, `❌ 請求失敗: ${error.message}`, 'error');
            }
        }

        async function uploadToSondeHub() {
            if (!decodedData) {
                showMessage(document.getElementById('uploadStatus'), '請先解碼數據', 'error');
                return;
            }

            const uploadStatus = document.getElementById('uploadStatus');
            uploadStatus.textContent = '正在上傳到 SondeHub...';
            uploadStatus.className = 'info';

            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: decodedData })
                });

                const result = await response.json();

                if (result.success) {
                    const message = `✅ 上傳成功！
狀態碼: ${result.status_code}
上傳大小: ${result.upload_size} bytes
數據包數量: ${result.packet_count}`;

                    showMessage(uploadStatus, message, 'success');
                } else {
                    showMessage(uploadStatus, `❌ 上傳失敗: ${result.error}`, 'error');
                }

            } catch (error) {
                showMessage(uploadStatus, `❌ 請求失敗: ${error.message}`, 'error');
            }
        }

        function updateStats(jsonData, decompressedSize, base64Size) {
            const stats = document.getElementById('stats');
            const originalSize = document.getElementById('originalSize');
            const base64SizeEl = document.getElementById('base64Size');
            const packetCount = document.getElementById('packetCount');
            const sondeId = document.getElementById('sondeId');

            const packetCountValue = Array.isArray(jsonData) ? jsonData.length : 1;
            const firstPacket = Array.isArray(jsonData) ? jsonData[0] : jsonData;
            const sondeIdValue = firstPacket?.serial || firstPacket?.id || 'N/A';

            originalSize.textContent = `${decompressedSize} bytes`;
            base64SizeEl.textContent = `${base64Size} bytes`;
            packetCount.textContent = packetCountValue;
            sondeId.textContent = sondeIdValue;

            stats.style.display = 'grid';
        }

        function showMessage(element, message, type) {
            element.textContent = message;
            element.className = type;
        }

        function clearAll() {
            document.getElementById('base64Input').value = '';
            document.getElementById('decodeResult').textContent = '點擊「解碼並顯示」按鈕開始...';
            document.getElementById('decodeResult').className = 'info';
            document.getElementById('jsonDisplay').style.display = 'none';
            document.getElementById('uploadStatus').textContent = '等待上傳...';
            document.getElementById('uploadStatus').className = 'info';
            document.getElementById('stats').style.display = 'none';
            decodedData = null;
        }

        // 頁面載入時自動解碼預設數據
        window.onload = function() {
            decodeAndDisplay();
        };
    </script>
</body>
</html>
    """)

@app.route('/api/decode', methods=['POST'])
def decode_base64_gzip():
    """解碼 Base64 編碼的 gzip 數據"""
    try:
        data = request.get_json()
        base64_data = data.get('base64_data', '').strip()
        
        if not base64_data:
            return jsonify({'success': False, 'error': '請提供 Base64 數據'})
        
        # 解碼 Base64
        try:
            binary_data = base64.b64decode(base64_data)
        except Exception as e:
            return jsonify({'success': False, 'error': f'Base64 解碼失敗: {str(e)}'})
        
        # 檢查是否為 gzip 格式
        if len(binary_data) < 2 or binary_data[0] != 0x1f or binary_data[1] != 0x8b:
            return jsonify({'success': False, 'error': '不是有效的 gzip 格式'})
        
        # 解壓 gzip
        try:
            decompressed_data = gzip.decompress(binary_data)
        except Exception as e:
            return jsonify({'success': False, 'error': f'gzip 解壓失敗: {str(e)}'})
        
        # 解析 JSON
        try:
            json_data = json.loads(decompressed_data.decode('utf-8'))
        except Exception as e:
            return jsonify({'success': False, 'error': f'JSON 解析失敗: {str(e)}'})
        
        packet_count = len(json_data) if isinstance(json_data, list) else 1
        
        logger.info(f"成功解碼數據: {len(decompressed_data)} bytes, {packet_count} 個數據包")
        
        return jsonify({
            'success': True,
            'data': json_data,
            'decompressed_size': len(decompressed_data),
            'packet_count': packet_count
        })
        
    except Exception as e:
        logger.error(f"解碼錯誤: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': f'解碼過程發生錯誤: {str(e)}'})

@app.route('/api/upload', methods=['POST'])
def upload_to_sondehub():
    """上傳數據到 SondeHub"""
    try:
        data = request.get_json()
        json_data = data.get('data')
        
        if not json_data:
            return jsonify({'success': False, 'error': '請提供要上傳的數據'})
        
        # 準備上傳數據
        json_string = json.dumps(json_data)
        json_bytes = json_string.encode('utf-8')
        
        # 壓縮數據
        compressed_data = gzip.compress(json_bytes)
        
        # 準備 HTTP 標頭
        from email.utils import formatdate
        headers = {
            'User-Agent': 'sondehub-uploader-server/1.0.0',
            'Content-Type': 'application/json',
            'Content-Encoding': 'gzip',
            'Date': formatdate()
        }
        
        # 上傳到 SondeHub
        try:
            response = requests.put(
                SONDEHUB_URL,
                data=compressed_data,
                headers=headers,
                timeout=30
            )
            
            packet_count = len(json_data) if isinstance(json_data, list) else 1
            
            if response.status_code == 200:
                logger.info(f"成功上傳到 SondeHub: {packet_count} 個數據包")
                return jsonify({
                    'success': True,
                    'status_code': response.status_code,
                    'upload_size': len(compressed_data),
                    'packet_count': packet_count
                })
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"SondeHub 上傳失敗: {error_msg}")
                return jsonify({
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                })
                
        except requests.exceptions.RequestException as e:
            logger.error(f"SondeHub 上傳請求失敗: {str(e)}")
            return jsonify({'success': False, 'error': f'上傳請求失敗: {str(e)}'})
        
    except Exception as e:
        logger.error(f"上傳錯誤: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': f'上傳過程發生錯誤: {str(e)}'})

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'service': 'SondeHub Uploader',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 啟動 SondeHub 上傳器服務...")
    print("📡 服務地址: http://localhost:5001")
    print("🔍 健康檢查: http://localhost:5001/api/health")
    print("📖 API 文檔:")
    print("  POST /api/decode - 解碼 Base64 編碼的 gzip 數據")
    print("  POST /api/upload - 上傳數據到 SondeHub")
    print("  GET  /api/health - 健康檢查")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
