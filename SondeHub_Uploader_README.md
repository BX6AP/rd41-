# SondeHub 上傳器

這是一個用於解碼 Base64 編碼的 gzip 數據並上傳到 SondeHub 的 Web 應用程式。

## 功能特色

- 🔍 **Base64 解碼**: 解碼 Base64 編碼的 gzip 數據
- 📦 **gzip 解壓縮**: 自動解壓縮 gzip 格式的數據
- 📋 **JSON 預覽**: 顯示解碼後的 JSON 數據
- 🚀 **SondeHub 上傳**: 直接上傳到 SondeHub API
- 📊 **統計資訊**: 顯示數據大小、壓縮比等統計
- 🌐 **Web 介面**: 友好的 Web 使用者介面

## 檔案說明

### 1. 純前端版本
- `simple_sondehub_uploader.html` - 純 HTML/JavaScript 版本
- 需要現代瀏覽器支援 (Chrome 80+, Firefox 65+)
- 使用瀏覽器內建的 DecompressionStream API

### 2. 後端服務版本
- `sondehub_uploader_server.py` - Flask 後端服務
- `start_uploader.sh` - 啟動腳本
- 支援所有瀏覽器
- 提供 RESTful API

## 使用方法

### 方法一：純前端版本

1. 直接在瀏覽器中打開 `simple_sondehub_uploader.html`
2. 貼上 Base64 編碼的 gzip 數據
3. 點擊「解碼並顯示」查看數據
4. 點擊「上傳到 SondeHub」上傳數據

### 方法二：後端服務版本

1. 啟動服務：
```bash
cd /home/pi/radiosonde_auto_rx
./start_uploader.sh
```

2. 在瀏覽器中打開 `http://localhost:5001`

3. 使用步驟與純前端版本相同

## API 端點

### POST /api/decode
解碼 Base64 編碼的 gzip 數據

**請求體：**
```json
{
  "base64_data": "H4sIAJwfzGgC/4WST4/TMBDFv0qVc2v5T5zEvcFlT0gVXQFitbKmzWTXUuIE2+myQnx3PC4rijiQXOLnn9+8yfjhRxXnIb1AQOthwmq/qQL0bo6z79HCmmYbvlfbzR/sgiG62RMpWMfk7oQJGkLWZZyhx2DPMI7RPRXm/Zfm3cHeg1vQWfUXtszRpavVg9SM1w3vuu1GSMG0aLWstxv+eHsAfELvgWzJKLkJbcAzugv2JEou9Y6bnejuhd5zua81M6b5SvAEfh3gnNaAgdhP4CKMUHxel9L4x2MtSqsYHIykfBZaCsFNUdfTLbg73h1I7iEhBflf/RFSRqRiouFckVAaF5IzoZu8hpEAbZiSKndeDeE6D6HKMuG0kEHDZF49r5PrXXrNCmc8C0vAGHNvdIBzw2qyPEEiT1WICClSgfx5wdFe8vcup1H51ebtedt9JpI1Whptct5Wa14bqov5cvgnqtIYpjveKtF2vJNN6WkI+G1Ff6ZcNZd5pC1V9vTHpSzJB3tGn0rQTGSgodGXDQxhJvJNWZappFctxQqxFnYC508zhP46hg+1rKt/9uzwcp2G5uVentYQk6UhFXetVfHD4fYGVneHY/Vbvp0pyT8ffwHitlDeKAMAAA=="
}
```

**回應：**
```json
{
  "success": true,
  "data": [...],
  "decompressed_size": 808,
  "packet_count": 1
}
```

### POST /api/upload
上傳數據到 SondeHub

**請求體：**
```json
{
  "data": [...]
}
```

**回應：**
```json
{
  "success": true,
  "status_code": 200,
  "upload_size": 475,
  "packet_count": 1
}
```

### GET /api/health
健康檢查

**回應：**
```json
{
  "status": "healthy",
  "service": "SondeHub Uploader",
  "version": "1.0.0"
}
```

## 範例使用

### 使用 curl 命令

1. **解碼數據：**
```bash
curl -X POST http://localhost:5001/api/decode \
  -H "Content-Type: application/json" \
  -d '{"base64_data": "H4sIAJwfzGgC/4WST4/TMBDFv0qVc2v5T5zEvcFlT0gVXQFitbKmzWTXUuIE2+myQnx3PC4rijiQXOLnn9+8yfjhRxXnIb1AQOthwmq/qQL0bo6z79HCmmYbvlfbzR/sgiG62RMpWMfk7oQJGkLWZZyhx2DPMI7RPRXm/Zfm3cHeg1vQWfUXtszRpavVg9SM1w3vuu1GSMG0aLWstxv+eHsAfELvgWzJKLkJbcAzugv2JEou9Y6bnejuhd5zua81M6b5SvAEfh3gnNaAgdhP4CKMUHxel9L4x2MtSqsYHIykfBZaCsFNUdfTLbg73h1I7iEhBflf/RFSRqRiouFckVAaF5IzoZu8hpEAbZiSKndeDeE6D6HKMuG0kEHDZF49r5PrXXrNCmc8C0vAGHNvdIBzw2qyPEEiT1WICClSgfx5wdFe8vcup1H51ebtedt9JpI1Whptct5Wa14bqov5cvgnqtIYpjveKtF2vJNN6WkI+G1Ff6ZcNZd5pC1V9vTHpSzJB3tGn0rQTGSgodGXDQxhJvJNWZappFctxQqxFnYC508zhP46hg+1rKt/9uzwcp2G5uVentYQk6UhFXetVfHD4fYGVneHY/Vbvp0pyT8ffwHitlDeKAMAAA=="}'
```

2. **上傳數據：**
```bash
curl -X POST http://localhost:5001/api/upload \
  -H "Content-Type: application/json" \
  -d '{"data": [{"software_name": "radiosonde_auto_rx", "type": "RS41", "serial": "W1521109", ...}]}'
```

## 系統需求

### 純前端版本
- 現代瀏覽器 (Chrome 80+, Firefox 65+, Safari 16+)
- 支援 DecompressionStream API

### 後端服務版本
- Python 3.6+
- Flask
- requests
- flask-cors

## 安裝依賴

```bash
pip3 install flask requests flask-cors
```

## 故障排除

### 1. 解碼失敗
- 檢查 Base64 數據是否完整
- 確認數據是有效的 gzip 格式
- 檢查 JSON 格式是否正確

### 2. 上傳失敗
- 檢查網路連接
- 確認 SondeHub API 可訪問
- 檢查數據格式是否符合 SondeHub 要求

### 3. 瀏覽器相容性
- 使用純前端版本需要支援 DecompressionStream 的瀏覽器
- 建議使用後端服務版本以獲得更好的相容性

## 技術細節

### 數據流程
1. Base64 解碼 → 二進制數據
2. gzip 解壓縮 → JSON 字串
3. JSON 解析 → 物件陣列
4. 重新壓縮 → gzip 格式
5. HTTPS PUT → SondeHub API

### 壓縮效果
- 原始 JSON: ~800 bytes
- gzip 壓縮後: ~475 bytes
- 壓縮比: ~60%

### 安全考量
- 使用 HTTPS 傳輸
- 驗證輸入數據格式
- 錯誤處理和日誌記錄

## 授權

本專案使用 MIT 授權條款。

## 支援

如有問題或建議，請聯繫開發團隊。
