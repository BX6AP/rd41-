# Radiosonde Auto-RX Debug 指南

## 問題描述

在運行 radiosonde_auto_rx 時遇到以下問題：
1. Web UI 無法顯示遙測數據
2. JavaScript 錯誤：`sonde_id_data.batt.toFixed is not a function`
3. 感測器資料無法顯示，即使有 RD41 信號

## 環境信息

- **系統**: Linux 6.12.44-v8+
- **工作目錄**: `/home/pi/radiosonde_auto_rx`
- **服務**: auto_rx.service
- **Sonde 類型**: RD41 (實驗用)

## 問題診斷過程

### 1. 初始錯誤檢查

**錯誤信息**:
```
2025-09-21 05:30:48 UTC – ERROR Decoder (RTLSDR 0) RD94RD41 406.025 - JSON object missing required field version. Have you re-built the decoders? (./build.sh)
```

**解決方案**: 重新編譯解碼器
```bash
cd /home/pi/radiosonde_auto_rx
./build.sh
```

### 2. GPS 鎖定問題

**錯誤信息**:
```
2025-09-21 05:02:18 UTC – WARNING Sonde 000007000 can only see 0 GNSS sats - discarding position as bad.
2025-09-21 05:07:54 UTC – WARNING Sonde 000007000 position breached radius cap by 1587.1 km.
```

**問題**: 數據被過濾器丟棄，無法顯示感測器資料

### 3. JavaScript 錯誤

**錯誤信息**:
```
(索引):804 Uncaught TypeError: sonde_id_data.batt.toFixed is not a function
```

**位置**: `auto_rx/autorx/templates/index.html` 第804行

**原因**: `batt` 字段值為 `-1`（無效值），不是數字類型，直接調用 `toFixed()` 導致錯誤

## 解決方案

### 1. 修復 JavaScript 錯誤

**文件**: `auto_rx/autorx/templates/index.html`

**修復前**:
```javascript
if (sonde_id_data.hasOwnProperty('batt') && sonde_id_data.batt >= 0){
    sonde_id_data.batt = sonde_id_data.batt.toFixed(1);
}
```

**修復後**:
```javascript
if (sonde_id_data.hasOwnProperty('batt') && typeof sonde_id_data.batt === 'number' && sonde_id_data.batt >= 0){
    sonde_id_data.batt = sonde_id_data.batt.toFixed(1);
}
```

**修復位置**:
- 第783行
- 第809行

### 2. 修改數據過濾邏輯

**文件**: `auto_rx/auto_rx.py`

**GPS 鎖定檢查修復**:
```python
# 修復前
if (telemetry["lat"] == 0.0) and (telemetry["lon"] == 0.0):
    logging.warning("Zero Lat/Lon. Sonde %s does not have GPS lock." % telemetry["id"])
    return False

# 修復後
if (telemetry["lat"] == 0.0) and (telemetry["lon"] == 0.0):
    logging.warning("Zero Lat/Lon. Sonde %s does not have GPS lock." % telemetry["id"])
    # Don't return False - allow sensor data to pass through
    # return False
```

**衛星數量檢查修復**:
```python
# 修復前
if "sats" in telemetry:
    if telemetry["sats"] < 4:
        logging.warning("Sonde %s can only see %d GNSS sats - discarding position as bad." % (telemetry["id"], telemetry["sats"]))
        return False

# 修復後
if "sats" in telemetry:
    if telemetry["sats"] < 4:
        logging.warning("Sonde %s can only see %d GNSS sats - discarding position as bad." % (telemetry["id"], telemetry["sats"]))
        # Don't return False - allow sensor data to pass through
        # return False
```

**時間驗證修復**:
```python
# 修復前
if abs(_delta_time) > (3600 * config["sonde_time_threshold"]):
    logging.warning("Sonde reported time too far from current UTC time. Either sonde time or system time is invalid. (Threshold: %d hours)" % config["sonde_time_threshold"])
    return False

# 修復後
if abs(_delta_time) > (3600 * config["sonde_time_threshold"]):
    logging.warning("Sonde reported time too far from current UTC time. Either sonde time or system time is invalid. (Threshold: %d hours)" % config["sonde_time_threshold"])
    # Modified: Allow data through even with time issues for sensor data display
    # return False
```

### 3. 服務重啟

```bash
sudo systemctl restart auto_rx
sudo systemctl status auto_rx
```

## 驗證修復

### 1. 檢查 API 數據

```bash
curl -s http://localhost:5000/get_telemetry_archive | head -20
```

**預期結果**: 應該看到包含感測器資料的 JSON 數據

### 2. 檢查日誌

```bash
journalctl -u auto_rx --no-pager -n 20
```

**預期結果**: 警告信息仍然顯示，但數據能正常通過

### 3. Web UI 檢查

訪問 `http://localhost:5000` 檢查遙測表格是否正常更新

## 關鍵學習點

### 1. 數據類型檢查的重要性

在 JavaScript 中調用數字方法前，必須確保變量是數字類型：
```javascript
// 錯誤做法
value.toFixed(1)

// 正確做法
if (typeof value === 'number' && value >= 0) {
    value.toFixed(1)
}
```

### 2. 過濾邏輯的平衡

- **原始設計**: 嚴格過濾確保數據質量
- **實驗需求**: 需要看到感測器資料，即使沒有GPS鎖定
- **解決方案**: 保留警告信息，但允許數據通過

### 3. 調試步驟

1. **檢查錯誤日誌**: `journalctl -u auto_rx`
2. **檢查 API 端點**: `curl http://localhost:5000/get_telemetry_archive`
3. **檢查瀏覽器控制台**: 查看 JavaScript 錯誤
4. **檢查數據流**: 從解碼器到 Web UI 的完整數據流

## 常見問題排查

### 1. Web UI 不更新

**可能原因**:
- JavaScript 錯誤阻止更新
- 數據被過濾器丟棄
- WebSocket 連接問題

**排查方法**:
```bash
# 檢查服務狀態
sudo systemctl status auto_rx

# 檢查 API 數據
curl -s http://localhost:5000/get_telemetry_archive

# 檢查瀏覽器控制台錯誤
# 按 F12 打開開發者工具
```

### 2. 感測器資料不顯示

**可能原因**:
- 數據被過濾器丟棄
- JavaScript 格式化錯誤
- 數據結構問題

**排查方法**:
```bash
# 檢查原始數據
curl -s http://localhost:5000/get_telemetry_archive | jq '.["000000000"].latest_telem'

# 檢查日誌中的過濾信息
journalctl -u auto_rx | grep -E "(WARNING|ERROR)"
```

### 3. 服務無法啟動

**可能原因**:
- 配置文件錯誤
- 端口被占用
- 權限問題

**排查方法**:
```bash
# 檢查服務狀態
sudo systemctl status auto_rx

# 檢查配置文件
python3 -c "import autorx.config; print(autorx.config.read_auto_rx_config('auto_rx/station.cfg'))"

# 檢查端口占用
netstat -tlnp | grep 5000
```

## 配置文件位置

- **主配置**: `auto_rx/station.cfg`
- **Web 模板**: `auto_rx/autorx/templates/index.html`
- **主程序**: `auto_rx/auto_rx.py`
- **Web 服務**: `auto_rx/autorx/web.py`

## 有用的命令

```bash
# 重啟服務
sudo systemctl restart auto_rx

# 查看實時日誌
journalctl -u auto_rx -f

# 檢查 API 數據
curl -s http://localhost:5000/get_telemetry_archive

# 檢查服務狀態
sudo systemctl status auto_rx

# 檢查端口占用
netstat -tlnp | grep 5000
```

## 注意事項

1. **警告信息是正常的**: GPS 和時間警告不會影響功能
2. **數據格式**: 確保所有感測器數據都有適當的類型檢查
3. **服務重啟**: 修改代碼後需要重啟服務才能生效
4. **瀏覽器緩存**: 修改 Web 模板後可能需要清除瀏覽器緩存

---

**創建時間**: 2025-09-21  
**問題類型**: Web UI 顯示問題 + JavaScript 錯誤  
**解決狀態**: ✅ 已解決
