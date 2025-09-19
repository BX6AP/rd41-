# RS41 探空儀數據上傳到 SondeHub 的流程

## 概述

本文檔詳細說明當 `radiosonde_auto_rx` 系統接收到 RS41 探空儀信號並成功解碼後，如何將遙測數據上傳到 SondeHub 全球追蹤平台的完整流程。

## 系統架構

```
RS41 探空儀 → RTLSDR → 解碼器 → 數據處理 → SondeHub 上傳器 → SondeHub API
```

## 詳細流程

### 1. 信號接收與解碼

#### 1.1 信號掃描
- 系統使用 RTLSDR 在 400.05-407.0 MHz 頻率範圍內掃描
- 檢測到 402 MHz 附近的 RS41 信號峰值
- 自動切換到解碼模式

#### 1.2 解碼鏈
```bash
rtl_fm -f 402047000 -s 48000 | iq_dec | fsk_demod | rs41mod --json
```

#### 1.3 解碼輸出
解碼器產生 JSON 格式的遙測數據：
```json
{
  "frame": 1037,
  "id": "W1521109",
  "datetime": "2025-09-18T14:57:48.996Z",
  "lat": 23.16001,
  "lon": 120.15609,
  "alt": 22.21,
  "temp": 26.1,
  "humidity": 0.0,
  "pressure": 1009.43,
  "batt": 3.0,
  "sats": 5,
  "vel_h": 0.0,
  "vel_v": 0.96,
  "heading": 0.0,
  "snr": 22.4,
  "f_centre": 402047625.0,
  "f_error": 625.0,
  "ppm": -56.125,
  "rs41_mainboard": "RSM424",
  "rs41_mainboard_fw": 20506,
  "bt": 65535,
  "ref_position": "GPS",
  "ref_datetime": "GPS"
}
```

### 2. 數據處理與過濾

#### 2.1 遙測過濾器 (`telemetry_filter`)
```python
# 位置：auto_rx/auto_rx.py
def telemetry_filter(telemetry):
    # 檢查基本欄位
    if not all(key in telemetry for key in ["id", "lat", "lon", "alt", "datetime"]):
        return False
    
    # 允許 GPS 未鎖定的數據通過（修改後）
    if (telemetry["lat"] == 0.0) and (telemetry["lon"] == 0.0):
        logging.warning("Zero Lat/Lon. Sonde %s does not have GPS lock." % telemetry["id"])
        # 不返回 False - 允許感測器數據通過
    
    # 允許低衛星數量的數據通過（修改後）
    if "sats" in telemetry:
        if telemetry["sats"] < 4:
            logging.warning("Sonde %s can only see %d GNSS sats - discarding position as bad." % (telemetry["id"], telemetry["sats"]))
            # 不返回 False - 允許感測器數據通過
    
    return True
```

#### 2.2 數據格式化
- 添加 `datetime_dt` 欄位（datetime 物件）
- 添加 `freq` 和 `freq_float` 欄位
- 添加 `type` 欄位（探空儀類型）
- 添加 `sdr_device_idx` 欄位

### 3. SondeHub 上傳器

#### 3.1 上傳器初始化
```python
# 位置：auto_rx/autorx/sondehub.py
class SondehubUploader:
    def __init__(self, 
                 upload_rate=15,           # 上傳頻率（秒）
                 upload_timeout=20,        # 上傳超時
                 upload_retries=5,         # 重試次數
                 user_callsign="BX6AP_Taipei_3",  # 站台呼號
                 user_position=[25.046088, 121.517524, 0],  # 站台位置
                 user_antenna="",          # 天線資訊
                 contact_email="none@none.com"):  # 聯絡信箱
```

#### 3.2 數據格式轉換
```python
def reformat_data(self, telemetry):
    """將內部格式轉換為 SondeHub 通用格式"""
    _output = {
        # 基本資訊
        "software_name": "radiosonde_auto_rx",
        "software_version": "1.8.2-beta6",
        "uploader_callsign": "BX6AP_Taipei_3",
        "uploader_position": [25.046088, 121.517524, 0],
        "uploader_antenna": "",
        "time_received": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        
        # 探空儀資訊
        "manufacturer": "Vaisala",
        "type": "RS41",
        "serial": "W1521109",
        "subtype": "RS41-SGP",
        
        # 時間和位置
        "datetime": "2025-09-18T14:57:48.996Z",
        "lat": 23.16001,
        "lon": 120.15609,
        "alt": 22.21,
        "frame": 1037,
        
        # 感測器數據
        "temp": 26.1,
        "humidity": 0.0,
        "pressure": 1009.43,
        "batt": 3.0,
        "sats": 5,
        
        # 運動數據
        "vel_v": 0.96,
        "vel_h": 0.0,
        "heading": 0.0,
        
        # 技術數據
        "frequency": 402.048,
        "snr": 22.4,
        "f_centre": 402047625.0,
        "f_error": 625.0,
        "ppm": -56.125,
        
        # RS41 特定數據
        "rs41_mainboard": "RSM424",
        "rs41_mainboard_fw": "20506",
        "burst_timer": 65535,
        
        # 參考資訊
        "ref_position": "GPS",
        "ref_datetime": "GPS"
    }
    return _output
```

### 4. 數據緩衝與上傳

#### 4.1 傳輸方式說明
**SondeHub 上傳使用 HTTP/HTTPS，不是 UDP！**

- **SondeHub API**: 使用 `requests.put()` 通過 HTTPS 上傳
- **OziMux 輸出**: 使用 UDP 廣播到本地網路（用於追蹤軟體）
- **APRS 上傳**: 使用 TCP 連接到 APRS 伺服器

#### 4.2 數據緩衝
```python
def add_telemetry(self, telemetry):
    """將遙測數據添加到上傳緩衝區"""
    # 轉換數據格式
    _formatted_data = self.reformat_data(telemetry)
    
    if _formatted_data:
        # 添加到緩衝區
        self.telemetry_buffer.append(_formatted_data)
        
        # 檢查是否需要上傳
        if len(self.telemetry_buffer) >= self.upload_threshold:
            self.upload_telemetry()
```

#### 4.3 SondeHub 上傳過程（HTTPS）
```python
def upload_telemetry(self):
    """上傳緩衝區中的遙測數據到 SondeHub（使用 HTTPS）"""
    if not self.telemetry_buffer:
        return
    
    # 準備上傳數據
    _upload_data = {
        "software_name": "radiosonde_auto_rx",
        "software_version": "1.8.2-beta6",
        "uploader_callsign": "BX6AP_Taipei_3",
        "uploader_position": [25.046088, 121.517524, 0],
        "uploader_antenna": "",
        "time_received": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "sondes": self.telemetry_buffer
    }
    
    # 壓縮數據
    _json_data = json.dumps(_upload_data).encode('utf-8')
    _compressed_data = gzip.compress(_json_data)
    
    # 設置 HTTP 標頭
    _headers = {
        "User-Agent": "autorx-1.8.2-beta6",
        "Content-Encoding": "gzip",
        "Content-Type": "application/json",
        "Date": formatdate(timeval=None, localtime=False, usegmt=True),
    }
    
    # 發送 HTTPS PUT 請求
    try:
        _req = requests.put(
            self.SONDEHUB_URL,  # https://api.v2.sondehub.org/sondes/telemetry
            _compressed_data,
            timeout=(self.upload_timeout, 6.1),
            headers=_headers,
        )
        
        if _req.status_code == 200:
            logging.info("Uploaded %d telemetry packets to Sondehub in %.1f seconds." % 
                        (len(self.telemetry_buffer), time.time() - _start_time))
            self.telemetry_buffer = []  # 清空緩衝區
        else:
            logging.error("Sondehub Uploader - Upload failed with status %d" % _req.status_code)
            
    except Exception as e:
        logging.error("Sondehub Uploader - Upload error: %s" % str(e))
```

#### 4.4 OziMux UDP 廣播（本地追蹤軟體）
```python
def send_ozimux_telemetry(self, telemetry):
    """發送 UDP 廣播到本地追蹤軟體"""
    _short_time = telemetry["datetime_dt"].strftime("%H:%M:%S")
    _sentence = "TELEMETRY,%s,%.5f,%.5f,%d\n" % (
        _short_time,
        telemetry["lat"],
        telemetry["lon"],
        telemetry["alt"],
    )
    
    try:
        _ozisock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _ozisock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        _ozisock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 發送到 UDP 廣播地址
        _ozisock.sendto(
            _sentence.encode("ascii"), 
            (self.ozimux_host, self.ozimux_port)  # 預設 port 8942
        )
        _ozisock.close()
        
    except Exception as e:
        self.log_error("Failed to send OziMux packet: %s" % str(e))
```

### 5. 傳輸方式比較

| 上傳目標 | 傳輸協定 | 用途 | 端口 | 說明 |
|---------|---------|------|------|------|
| **SondeHub** | HTTPS PUT | 全球追蹤平台 | 443 | 主要數據上傳，使用 `requests.put()` |
| **OziMux** | UDP 廣播 | 本地追蹤軟體 | 8942 | 用於 OziExplorer 等追蹤軟體 |
| **Payload Summary** | UDP 廣播 | 本地數據分發 | 55672 | 用於 Horus 追蹤工具 |
| **APRS** | TCP | 業餘無線電網路 | 14580 | 上傳到 radiosondy.info |

### 6. 上傳配置

#### 6.1 站台配置 (`station.cfg`)
```ini
[sondehub]
# 啟用 SondeHub 上傳
sondehub_enabled = True

# 上傳頻率（秒）
sondehub_upload_rate = 15

# 聯絡信箱
sondehub_contact_email = none@none.com

[location]
# 站台位置
station_lat = 25.046088
station_lon = 121.517524
station_alt = 0

[habitat]
# 站台呼號
uploader_callsign = BX6AP_Taipei_3
```

#### 5.2 API 端點
- **SondeHub API**: `https://api.v2.sondehub.org/sondes/telemetry`
- **站台位置 API**: `https://api.v2.sondehub.org/listeners`

### 6. 上傳日誌

#### 6.1 成功上傳
```
Sep 18 22:56:33 RS41 auto_rx[398560]: INFO:Sondehub Uploader - Uploaded 9 telemetry packets to Sondehub in 1.1 seconds.
Sep 18 22:56:49 RS41 auto_rx[398560]: INFO:Sondehub Uploader - Uploaded 16 telemetry packets to Sondehub in 1.2 seconds.
```

#### 6.2 站台資訊上傳
```
Sep 18 22:55:47 RS41 auto_rx[398560]: INFO:Sondehub Uploader - Uploaded station information to Sondehub.
```

### 7. 數據驗證

#### 7.1 必要欄位檢查
- `id`: 探空儀序列號
- `datetime`: 時間戳記
- `lat`, `lon`, `alt`: 位置資訊
- `frame`: 幀數

#### 7.2 數據品質檢查
- 溫度 > -273°C
- 濕度 >= 0%
- 壓力 >= 0 hPa
- 電池電壓 >= 0V
- 衛星數量 >= 0

### 8. 錯誤處理

#### 8.1 上傳失敗重試
- 最多重試 5 次
- 每次重試間隔遞增
- 記錄錯誤日誌

#### 8.2 數據格式錯誤
- 跳過無效數據
- 記錄警告訊息
- 繼續處理其他數據

### 9. 性能優化

#### 9.1 數據壓縮
- 使用 gzip 壓縮
- 減少網路傳輸量
- 提高上傳效率

#### 9.2 批量上傳
- 緩衝多個數據包
- 減少 API 調用次數
- 提高系統效率

### 10. 監控與除錯

#### 10.1 日誌監控
```bash
# 查看上傳日誌
journalctl -u auto_rx | grep "Sondehub Uploader"

# 查看解碼日誌
journalctl -u auto_rx | grep "RS41"
```

#### 10.2 Web 介面監控
- 訪問 `http://rs41.local:5000/`
- 查看遙測表格
- 監控實時數據

## 總結

RS41 探空儀數據上傳到 SondeHub 的流程包括：

1. **信號接收** → RTLSDR 接收 402 MHz 信號
2. **解碼處理** → fsk_demod + rs41mod 解碼鏈
3. **數據過濾** → 檢查必要欄位和數據品質
4. **格式轉換** → 轉換為 SondeHub 通用格式
5. **數據緩衝** → 批量收集數據包
6. **壓縮上傳** → gzip 壓縮後上傳到 API
7. **錯誤處理** → 重試機制和日誌記錄

整個流程確保了 RS41 探空儀的遙測數據能夠可靠、高效地傳輸到 SondeHub 全球追蹤平台，供全球用戶追蹤和科學研究使用。
