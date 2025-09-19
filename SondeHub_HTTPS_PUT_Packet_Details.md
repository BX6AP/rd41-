# SondeHub HTTPS PUT 請求封包內容詳解

## 概述

本文檔詳細說明 `radiosonde_auto_rx` 系統向 SondeHub 發送 HTTPS PUT 請求時的完整封包內容，包括 HTTP 標頭、請求主體、壓縮處理和傳輸細節。

## 1. HTTP 請求基本資訊

### 1.1 請求方法與 URL
```
方法: PUT
URL: https://api.v2.sondehub.org/sondes/telemetry
協定: HTTPS (TLS 1.2/1.3)
端口: 443
```

### 1.2 連接參數
```
連接超時: 20 秒
讀取超時: 6.1 秒
重試次數: 最多 5 次
重試策略: 指數退避
```

## 2. HTTP 標頭 (Headers)

### 2.1 標準標頭
```http
PUT /sondes/telemetry HTTP/1.1
Host: api.v2.sondehub.org
User-Agent: autorx-1.8.2-beta6
Content-Type: application/json
Content-Encoding: gzip
Content-Length: 438
Date: Mon, 18 Sep 2025 15:02:37 GMT
Connection: keep-alive
```

### 2.2 標頭說明
| 標頭 | 值 | 說明 |
|------|----|----|
| `User-Agent` | `autorx-1.8.2-beta6` | 識別上傳軟體和版本 |
| `Content-Type` | `application/json` | 指定內容類型為 JSON |
| `Content-Encoding` | `gzip` | 指定內容使用 gzip 壓縮 |
| `Content-Length` | `438` | 壓縮後的內容長度（字節） |
| `Date` | `Mon, 18 Sep 2025 15:02:37 GMT` | 請求發送時間（UTC） |

## 3. 請求主體 (Request Body)

### 3.1 JSON 數據結構
```json
[
  {
    "software_name": "radiosonde_auto_rx",
    "software_version": "1.8.2-beta6",
    "uploader_callsign": "BX6AP_Taipei_3",
    "uploader_position": [25.046088, 121.517524, 0],
    "uploader_antenna": "",
    "time_received": "2025-09-18T15:02:37.996Z",
    "manufacturer": "Vaisala",
    "type": "RS41",
    "serial": "W1521109",
    "subtype": "RS41-SGP",
    "datetime": "2025-09-18T15:02:37.996Z",
    "lat": 23.16017,
    "lon": 120.15602,
    "alt": 89.58712,
    "frame": 1326,
    "temp": 26.3,
    "humidity": 0.0,
    "pressure": 1009.43,
    "batt": 3.0,
    "sats": 6,
    "vel_v": -8.000380000000002,
    "vel_h": 1.1119492662446442,
    "heading": 180.0,
    "frequency": 402.047,
    "snr": 22.4,
    "f_centre": 402047625.0,
    "f_error": 625.0,
    "ppm": -5.125,
    "rs41_mainboard": "RSM424",
    "rs41_mainboard_fw": "20506",
    "burst_timer": 65535,
    "ref_position": "GPS",
    "ref_datetime": "GPS"
  }
]
```

### 3.2 欄位說明

#### 3.2.1 軟體資訊
| 欄位 | 類型 | 說明 | 範例值 |
|------|------|------|--------|
| `software_name` | string | 軟體名稱 | "radiosonde_auto_rx" |
| `software_version` | string | 軟體版本 | "1.8.2-beta6" |
| `uploader_callsign` | string | 上傳者呼號 | "BX6AP_Taipei_3" |
| `uploader_position` | array | 上傳者位置 [lat, lon, alt] | [25.046088, 121.517524, 0] |
| `uploader_antenna` | string | 天線資訊 | "" |
| `time_received` | string | 接收時間 (ISO 8601) | "2025-09-18T15:02:37.996Z" |

#### 3.2.2 探空儀基本資訊
| 欄位 | 類型 | 說明 | 範例值 |
|------|------|------|--------|
| `manufacturer` | string | 製造商 | "Vaisala" |
| `type` | string | 探空儀類型 | "RS41" |
| `serial` | string | 序列號 | "W1521109" |
| `subtype` | string | 子類型 | "RS41-SGP" |
| `datetime` | string | 數據時間 (ISO 8601) | "2025-09-18T15:02:37.996Z" |
| `frame` | integer | 幀數 | 1326 |

#### 3.2.3 位置資訊
| 欄位 | 類型 | 說明 | 範例值 |
|------|------|------|--------|
| `lat` | float | 緯度 (度) | 23.16017 |
| `lon` | float | 經度 (度) | 120.15602 |
| `alt` | float | 高度 (公尺) | 89.58712 |

#### 3.2.4 感測器數據
| 欄位 | 類型 | 說明 | 範例值 |
|------|------|------|--------|
| `temp` | float | 溫度 (°C) | 26.3 |
| `humidity` | float | 濕度 (%) | 0.0 |
| `pressure` | float | 壓力 (hPa) | 1009.43 |
| `batt` | float | 電池電壓 (V) | 3.0 |
| `sats` | integer | 衛星數量 | 6 |

#### 3.2.5 運動數據
| 欄位 | 類型 | 說明 | 範例值 |
|------|------|------|--------|
| `vel_v` | float | 垂直速度 (m/s) | -8.000380000000002 |
| `vel_h` | float | 水平速度 (m/s) | 1.1119492662446442 |
| `heading` | float | 航向 (度) | 180.0 |

#### 3.2.6 技術數據
| 欄位 | 類型 | 說明 | 範例值 |
|------|------|------|--------|
| `frequency` | float | 頻率 (MHz) | 402.047 |
| `snr` | float | 信噪比 (dB) | 22.4 |
| `f_centre` | float | 頻率中心 (Hz) | 402047625.0 |
| `f_error` | float | 頻率誤差 (Hz) | 625.0 |
| `ppm` | float | 頻率校正 (PPM) | -5.125 |

#### 3.2.7 RS41 特定數據
| 欄位 | 類型 | 說明 | 範例值 |
|------|------|------|--------|
| `rs41_mainboard` | string | 主機板型號 | "RSM424" |
| `rs41_mainboard_fw` | string | 韌體版本 | "20506" |
| `burst_timer` | integer | 爆發計時器 | 65535 |

#### 3.2.8 參考資訊
| 欄位 | 類型 | 說明 | 範例值 |
|------|------|------|--------|
| `ref_position` | string | 位置參考 | "GPS" |
| `ref_datetime` | string | 時間參考 | "GPS" |

## 4. 數據壓縮處理

### 4.1 壓縮流程
```python
# 1. 序列化 JSON
_telem_json = json.dumps(telem_list).encode("utf-8")

# 2. gzip 壓縮
_compressed_payload = gzip.compress(_telem_json)

# 3. 設置 Content-Encoding 標頭
headers["Content-Encoding"] = "gzip"
```

### 4.2 壓縮效果
| 項目 | 大小 | 說明 |
|------|------|------|
| 原始 JSON | 730 bytes | 未壓縮的 JSON 數據 |
| gzip 壓縮後 | 438 bytes | 壓縮後的數據 |
| 壓縮比 | 60% | 節省 40% 的傳輸量 |
| 壓縮時間 | < 1ms | 壓縮處理時間 |

## 5. TLS 加密傳輸

### 5.1 加密參數
```
協定: TLS 1.2 或 TLS 1.3
加密套件: AES-256-GCM 或 ChaCha20-Poly1305
證書驗證: 啟用
HSTS: 支援
```

### 5.2 傳輸層安全
- **端到端加密**: 從客戶端到 SondeHub 伺服器
- **證書驗證**: 驗證伺服器身份
- **完整性檢查**: 防止數據篡改
- **重放攻擊防護**: 時間戳記驗證

## 6. 實際傳輸封包

### 6.1 完整 HTTP 請求
```http
PUT /sondes/telemetry HTTP/1.1
Host: api.v2.sondehub.org
User-Agent: autorx-1.8.2-beta6
Content-Type: application/json
Content-Encoding: gzip
Content-Length: 438
Date: Mon, 18 Sep 2025 15:02:37 GMT
Connection: keep-alive

[gzip 壓縮的 JSON 數據 - 438 bytes]
```

### 6.2 傳輸統計
```
總封包大小: ~500-600 bytes (包含 HTTP 標頭)
有效數據: 438 bytes (壓縮後)
HTTP 標頭: ~150 bytes
TLS 開銷: ~50-100 bytes
```

## 7. 伺服器回應

### 7.1 成功回應 (HTTP 200)
```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 0
Date: Mon, 18 Sep 2025 15:02:38 GMT
Server: nginx/1.18.0
```

### 7.2 錯誤回應範例
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
Content-Length: 45
Date: Mon, 18 Sep 2025 15:02:38 GMT

{"error": "Invalid telemetry data format"}
```

### 7.3 回應處理
| 狀態碼 | 說明 | 處理方式 |
|--------|------|----------|
| 200 | 成功 | 清空緩衝區，繼續上傳 |
| 400 | 請求錯誤 | 記錄錯誤，跳過此批次 |
| 500 | 伺服器錯誤 | 重試上傳 |
| 其他 | 其他錯誤 | 根據錯誤類型決定重試或跳過 |

## 8. 上傳頻率與批量處理

### 8.1 上傳策略
```
上傳頻率: 每 15 秒
批量大小: 1-50 個數據包
緩衝策略: 時間觸發 + 數量觸發
```

### 8.2 批量上傳範例
```json
[
  {
    "software_name": "radiosonde_auto_rx",
    "software_version": "1.8.2-beta6",
    "uploader_callsign": "BX6AP_Taipei_3",
    "uploader_position": [25.046088, 121.517524, 0],
    "uploader_antenna": "",
    "time_received": "2025-09-18T15:02:37.996Z",
    "manufacturer": "Vaisala",
    "type": "RS41",
    "serial": "W1521109",
    "subtype": "RS41-SGP",
    "datetime": "2025-09-18T15:02:37.996Z",
    "lat": 23.16017,
    "lon": 120.15602,
    "alt": 89.58712,
    "frame": 1326,
    "temp": 26.3,
    "humidity": 0.0,
    "pressure": 1009.43,
    "batt": 3.0,
    "sats": 6,
    "vel_v": -8.000380000000002,
    "vel_h": 1.1119492662446442,
    "heading": 180.0,
    "frequency": 402.047,
    "snr": 22.4,
    "f_centre": 402047625.0,
    "f_error": 625.0,
    "ppm": -5.125,
    "rs41_mainboard": "RSM424",
    "rs41_mainboard_fw": "20506",
    "burst_timer": 65535,
    "ref_position": "GPS",
    "ref_datetime": "GPS"
  },
  {
    "software_name": "radiosonde_auto_rx",
    "software_version": "1.8.2-beta6",
    "uploader_callsign": "BX6AP_Taipei_3",
    "uploader_position": [25.046088, 121.517524, 0],
    "uploader_antenna": "",
    "time_received": "2025-09-18T15:02:52.996Z",
    "manufacturer": "Vaisala",
    "type": "RS41",
    "serial": "W1521109",
    "subtype": "RS41-SGP",
    "datetime": "2025-09-18T15:02:52.996Z",
    "lat": 23.16025,
    "lon": 120.15601,
    "alt": 95.23456,
    "frame": 1327,
    "temp": 26.2,
    "humidity": 0.0,
    "pressure": 1009.41,
    "batt": 3.0,
    "sats": 6,
    "vel_v": -7.850000000000001,
    "vel_h": 1.0899999999999999,
    "heading": 180.0,
    "frequency": 402.047,
    "snr": 22.3,
    "f_centre": 402047625.0,
    "f_error": 625.0,
    "ppm": -5.125,
    "rs41_mainboard": "RSM424",
    "rs41_mainboard_fw": "20506",
    "burst_timer": 65535,
    "ref_position": "GPS",
    "ref_datetime": "GPS"
  }
]
```

## 9. 監控與除錯

### 9.1 上傳日誌
```
Sep 18 22:56:33 RS41 auto_rx[398560]: INFO:Sondehub Uploader - Uploaded 9 telemetry packets to Sondehub in 1.1 seconds.
Sep 18 22:56:49 RS41 auto_rx[398560]: INFO:Sondehub Uploader - Uploaded 16 telemetry packets to Sondehub in 1.2 seconds.
```

### 9.2 壓縮統計日誌
```
Sep 18 22:56:33 RS41 auto_rx[398560]: DEBUG:Pre-compression: 730 bytes, post: 438 bytes. 60.0 % compression ratio, in 0.001 s
```

### 9.3 錯誤日誌
```
Sep 18 22:56:33 RS41 auto_rx[398560]: ERROR:Sondehub Uploader - Upload Failed: Connection timeout
Sep 18 22:56:33 RS41 auto_rx[398560]: ERROR:Sondehub Uploader - Upload failed with status 500
```

## 10. 性能優化

### 10.1 壓縮優化
- 使用 gzip 壓縮減少 40% 傳輸量
- 批量上傳減少 HTTP 請求次數
- 連接復用減少 TLS 握手開銷

### 10.2 網路優化
- 設置適當的超時參數
- 實現指數退避重試策略
- 使用 HTTPS 確保傳輸可靠性

### 10.3 資源管理
- 限制緩衝區大小防止記憶體溢出
- 定期清理上傳緩衝區
- 監控上傳成功率

## 總結

SondeHub HTTPS PUT 請求封包包含：

1. **HTTP 標頭**: 包含軟體識別、內容類型和壓縮資訊
2. **JSON 主體**: 包含完整的探空儀遙測數據
3. **gzip 壓縮**: 減少 40% 的傳輸量
4. **TLS 加密**: 確保數據傳輸安全
5. **批量處理**: 提高上傳效率
6. **錯誤處理**: 實現可靠的重試機制

整個封包設計確保了數據的完整性、安全性和傳輸效率，為全球探空儀追蹤提供了可靠的數據上傳機制。
