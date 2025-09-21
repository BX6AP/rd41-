#!/usr/bin/env python3
"""
SondeHub Uploader Backend Service
Provides API endpoints for decoding Base64 encoded gzip data and uploading to SondeHub
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SondeHub API endpoint
SONDEHUB_URL = "https://api.v2.sondehub.org/sondes/telemetry"

# TODO: Add rate limiting to prevent API abuse
# FIXME: Handle network timeouts more gracefully

@app.route('/')
def index():
    """Main page"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SondeHub Uploader</title>
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
        <h1>🚀 SondeHub Uploader</h1>
        
        <div class="section">
            <h2>📥 Input Base64 Data</h2>
            <textarea id="base64Input" placeholder="Please paste Base64 encoded gzip data...">H4sIAJwfzGgC/4WST4/TMBDFv0qVc2v5T5zEvcFlT0gVXQFitbKmzWTXUuIE2+myQnx3PC4rijiQXOLnn9+8yfjhRxXnIb1AQOthwmq/qQL0bo6z79HCmmYbvlfbzR/sgiG62RMpWMfk7oQJGkLWZZyhx2DPMI7RPRXm/Zfm3cHeg1vQWfUXtszRpavVg9SM1w3vuu1GSMG0aLWstxv+eHsAfELvgWzJKLkJbcAzugv2JEou9Y6bnejuhd5zua81M6b5SvAEfh3gnNaAgdhP4CKMUHxel9L4x2MtSqsYHIykfBZaCsFNUdfTLbg73h1I7iEhBflf/RFSRqRiouFckVAaF5IzoZu8hpEAbZiSKndeDeE6D6HKMuG0kEHDZF49r5PrXXrNCmc8C0vAGHNvdIBzw2qyPEEiT1WICClSgfx5wdFe8vcup1H51ebtedt9JpI1Whptct5Wa14bqov5cvgnqtIYpjveKtF2vJNN6WkI+G1Ff6ZcNZd5pC1V9vTHpSzJB3tGn0rQTGSgodGXDQxhJvJNWZappFctxQqxFnYC508zhP46hg+1rKt/9uzwcp2G5uVentYQk6UhFXetVfHD4fYGVneHY/Vbvp0pyT8ffwHitlDeKAMAAA==</textarea>
            <br>
            <button onclick="decodeAndDisplay()">🔍 Decode and Display</button>
            <button onclick="uploadToSondeHub()">🚀 Upload to SondeHub</button>
            <button onclick="clearAll()">🗑️ Clear</button>
        </div>

        <div class="section">
            <h2>📊 Decode Result</h2>
            <div id="decodeResult" class="info">Click "Decode and Display" button to start...</div>
        </div>

        <div class="section">
            <h2>📋 JSON Data</h2>
            <div id="jsonDisplay" class="json-display" style="display: none;">JSON data will be displayed after decoding...</div>
        </div>

        <div class="section">
            <h2>📈 Upload Status</h2>
            <div id="uploadStatus" class="info">Waiting for upload...</div>
        </div>

        <div class="stats" id="stats" style="display: none;">
            <div class="stat-card">
                <h4>Original Size</h4>
                <div class="value" id="originalSize">-</div>
            </div>
            <div class="stat-card">
                <h4>Base64 Size</h4>
                <div class="value" id="base64Size">-</div>
            </div>
            <div class="stat-card">
                <h4>Packet Count</h4>
                <div class="value" id="packetCount">-</div>
            </div>
            <div class="stat-card">
                <h4>Sonde ID</h4>
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
                showMessage(decodeResult, 'Please enter Base64 data', 'error');
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
                    
                    const message = `✅ Decode successful!
Base64 size: ${base64Input.length} characters
Decompressed size: ${result.decompressed_size} characters
Packet count: ${result.packet_count}`;

                    showMessage(decodeResult, message, 'success');
                    
                    // 顯示 JSON
                    jsonDisplay.textContent = JSON.stringify(result.data, null, 2);
                    jsonDisplay.style.display = 'block';
                    
                    // 更新統計
                    updateStats(result.data, result.decompressed_size, base64Input.length);
                } else {
                    showMessage(decodeResult, `❌ Decode failed: ${result.error}`, 'error');
                }

            } catch (error) {
                showMessage(decodeResult, `❌ Request failed: ${error.message}`, 'error');
            }
        }

        async function uploadToSondeHub() {
            if (!decodedData) {
                showMessage(document.getElementById('uploadStatus'), 'Please decode data first', 'error');
                return;
            }

            const uploadStatus = document.getElementById('uploadStatus');
            uploadStatus.textContent = 'Uploading to SondeHub...';
            uploadStatus.className = 'info';

            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: decodedData })
                });

                const result = await response.json();

                if (result.success) {
                    const message = `✅ Upload successful!
Status code: ${result.status_code}
Upload size: ${result.upload_size} bytes
Packet count: ${result.packet_count}`;

                    showMessage(uploadStatus, message, 'success');
                } else {
                    showMessage(uploadStatus, `❌ Upload failed: ${result.error}`, 'error');
                }

            } catch (error) {
                showMessage(uploadStatus, `❌ Request failed: ${error.message}`, 'error');
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
            document.getElementById('decodeResult').textContent = 'Click "Decode and Display" button to start...';
            document.getElementById('decodeResult').className = 'info';
            document.getElementById('jsonDisplay').style.display = 'none';
            document.getElementById('uploadStatus').textContent = 'Waiting for upload...';
            document.getElementById('uploadStatus').className = 'info';
            document.getElementById('stats').style.display = 'none';
            decodedData = null;
        }

        // Auto-decode default data when page loads
        window.onload = function() {
            decodeAndDisplay();
        };
    </script>
</body>
</html>
    """)

@app.route('/api/decode', methods=['POST'])
def decode_base64_gzip():
    """Decode Base64 encoded gzip data"""
    try:
        data = request.get_json()
        base64_data = data.get('base64_data', '').strip()
        
        if not base64_data:
            return jsonify({'success': False, 'error': 'Please provide Base64 data'})
        
        # 解碼 Base64
        try:
            binary_data = base64.b64decode(base64_data)
        except Exception as e:
            return jsonify({'success': False, 'error': f'Base64 decode failed: {str(e)}'})
        
        # 檢查是否為 gzip 格式
        if len(binary_data) < 2 or binary_data[0] != 0x1f or binary_data[1] != 0x8b:
            return jsonify({'success': False, 'error': 'Not a valid gzip format'})
        
        # 解壓 gzip
        try:
            decompressed_data = gzip.decompress(binary_data)
        except Exception as e:
            return jsonify({'success': False, 'error': f'gzip decompression failed: {str(e)}'})
        
        # 解析 JSON
        try:
            json_data = json.loads(decompressed_data.decode('utf-8'))
        except Exception as e:
            return jsonify({'success': False, 'error': f'JSON parsing failed: {str(e)}'})
        
        packet_count = len(json_data) if isinstance(json_data, list) else 1
        
        logger.info(f"Successfully decoded data: {len(decompressed_data)} bytes, {packet_count} packets")
        
        return jsonify({
            'success': True,
            'data': json_data,
            'decompressed_size': len(decompressed_data),
            'packet_count': packet_count
        })
        
    except Exception as e:
        logger.error(f"Decode error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': f'Error occurred during decoding: {str(e)}'})

@app.route('/api/upload', methods=['POST'])
def upload_to_sondehub():
    """Upload data to SondeHub"""
    try:
        data = request.get_json()
        json_data = data.get('data')
        
        if not json_data:
            return jsonify({'success': False, 'error': 'Please provide data to upload'})
        
        # Prepare upload data
        json_string = json.dumps(json_data)
        json_bytes = json_string.encode('utf-8')
        
        # Compress data
        # TODO: Consider using different compression levels for different data sizes
        compressed_data = gzip.compress(json_bytes)
        
        # Prepare HTTP headers
        from email.utils import formatdate
        headers = {
            'User-Agent': 'sondehub-uploader-server/1.0.0',
            'Content-Type': 'application/json',
            'Content-Encoding': 'gzip',
            'Date': formatdate()
        }
        
        # Upload to SondeHub
        # Note: Sometimes the timeout is too short for large batches
        # TODO: Make timeout configurable based on data size
        try:
            response = requests.put(
                SONDEHUB_URL,
                data=compressed_data,
                headers=headers,
                timeout=30
            )
            
            packet_count = len(json_data) if isinstance(json_data, list) else 1
            
            if response.status_code == 200:
                logger.info(f"Successfully uploaded to SondeHub: {packet_count} packets")
                return jsonify({
                    'success': True,
                    'status_code': response.status_code,
                    'upload_size': len(compressed_data),
                    'packet_count': packet_count
                })
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"SondeHub upload failed: {error_msg}")
                return jsonify({
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                })
                
        except requests.exceptions.RequestException as e:
            logger.error(f"SondeHub upload request failed: {str(e)}")
            return jsonify({'success': False, 'error': f'Upload request failed: {str(e)}'})
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': f'Error occurred during upload: {str(e)}'})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SondeHub Uploader',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting SondeHub Uploader Service...")
    print("📡 Service URL: http://localhost:5001")
    print("🔍 Health Check: http://localhost:5001/api/health")
    print("📖 API Documentation:")
    print("  POST /api/decode - Decode Base64 encoded gzip data")
    print("  POST /api/upload - Upload data to SondeHub")
    print("  GET  /api/health - Health check")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
