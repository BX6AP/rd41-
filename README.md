# RD41 解碼專案

這是一個基於 `radiosonde_auto_rx` 的 RD41 dropsonde（投落式探空儀）解碼系統，專門用於接收、解碼和追蹤 Vaisala RD41 探空儀的遙測數據。

## 專案特色

- 🎯 **專門針對 RD41**: 優化的 RD41 dropsonde 解碼支援
- 📡 **自動信號檢測**: 在 400-406 MHz 頻段自動掃描和檢測 RD41 信號
- 🔄 **實時解碼**: 使用 `rd94rd41drop` 解碼器進行實時數據解碼
- 🌐 **SondeHub 整合**: 自動上傳數據到全球 SondeHub 追蹤平台
- 📊 **Web 介面**: 提供即時的地圖顯示和數據監控
- 🔧 **易於配置**: 簡單的配置文件和自動化腳本

## 支援的探空儀類型

### Vaisala RD41
- **頻率範圍**: 400-406 MHz
- **調變方式**: FSK 4800 baud
- **編碼**: Manchester, 8N1
- **資料率**: 240 bytes/sec
- **位置更新**: 2 Hz
- **速度更新**: 4 Hz

## 系統需求

- **硬體**: Raspberry Pi 3B+ 或更高版本
- **SDR**: RTLSDR 或 AirSpy
- **作業系統**: Raspberry Pi OS (64-bit)
- **Python**: 3.8+
- **記憶體**: 最少 2GB RAM

## 快速開始

### 1. 安裝依賴

```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝必要套件
sudo apt install -y git build-essential cmake libusb-1.0-0-dev \
    rtl-sdr librtlsdr-dev sox libsox-fmt-all python3-pip \
    python3-numpy python3-scipy python3-matplotlib

# 安裝 Python 套件
pip3 install -r auto_rx/requirements.txt
```

### 2. 編譯解碼器

```bash
# 編譯 dropsonde 解碼器
cd demod/dropsonde/
make clean all

# 複製解碼器到 auto_rx 目錄
cd ../../auto_rx/
cp ../dropsonde/rd94rd41drop .
```

### 3. 配置系統

```bash
# 複製配置範例
cp station.cfg.example station.cfg

# 編輯配置文件
nano station.cfg
```

### 4. 啟動系統

```bash
# 啟動 RD41 解碼系統
python3 auto_rx.py --config station.cfg
```

## 配置說明

### 基本配置 (station.cfg)

```ini
[location]
# 接收站位置
station_lat = 25.046088
station_lon = 121.517524
station_alt = 0

[sondehub]
# SondeHub 上傳設定
sondehub_enabled = True
sondehub_upload_rate = 15
sondehub_contact_email = your@email.com

[habitat]
# 站台資訊
uploader_callsign = YOUR_CALLSIGN
uploader_antenna = "RD41 專用天線"
```

### 頻率配置

RD41 dropsonde 通常在以下頻率操作：
- 401.000 MHz
- 401.100 MHz
- 401.400 MHz
- 401.500 MHz
- 401.740 MHz
- 401.800 MHz
- 402.000 MHz
- 402.200 MHz
- 402.300 MHz
- 402.520 MHz
- 402.800 MHz
- 403.000 MHz
- 403.200 MHz
- 403.400 MHz
- 403.600 MHz
- 404.000 MHz
- 404.200 MHz
- 404.400 MHz
- 404.600 MHz
- 405.000 MHz
- 405.200 MHz
- 405.400 MHz
- 405.600 MHz
- 405.800 MHz
- 406.000 MHz

## 數據格式

解碼器輸出符合標準的 JSON 格式：

```json
{
  "type": "RD41",
  "frame": 123,
  "id": "123456789",
  "datetime": "2025-01-17T12:34:56.789Z",
  "lat": 52.12345,
  "lon": 13.67890,
  "alt": 5000.0,
  "temp": -20.5,
  "humidity": 45.2,
  "pressure": 500.0,
  "vel_h": 25.3,
  "vel_v": -5.2,
  "heading": 180.0,
  "sats": 8,
  "freq": 401.400
}
```

## 功能特色

### 1. 自動信號檢測
- 在 400-406 MHz 頻段自動掃描
- 檢測 RD41 信號特徵（同步頭 0x1ACFFC1D）
- 自動切換到解碼模式

### 2. 實時解碼
- 使用 `rd94rd41drop` 解碼器
- 支援位置、溫度、濕度、氣壓數據
- 實時錯誤檢查和數據驗證

### 3. 數據上傳
- **SondeHub**: 全球追蹤平台
- **APRS-IS**: 業餘無線電網路
- **本地記錄**: CSV 檔案存儲

### 4. Web 介面
- 即時地圖顯示
- 遙測數據表格
- 系統狀態監控

## 使用場景

### 颶風研究
- 從氣象飛機投下的 RD41 探空儀
- 提供高精度的垂直大氣剖面數據
- 支援颶風強度和路徑預測

### 風暴追蹤
- 實時追蹤風暴系統
- 收集關鍵氣象數據
- 支援氣象預報模型

## 技術細節

### 信號處理流程
```
RD41 探空儀 → RTLSDR → FM 解調 → rd94rd41drop → JSON 數據 → SondeHub
```

### 解碼參數
- **採樣率**: 48 kHz
- **濾波器**: 高通 20Hz, 低通 2600Hz
- **幀長**: 120 bytes
- **錯誤檢查**: CRC16 校驗

## 故障排除

### 常見問題

1. **無法檢測到信號**
   - 檢查天線連接
   - 確認頻率設定正確
   - 檢查 SDR 硬體狀態

2. **解碼失敗**
   - 檢查信號品質
   - 確認解碼器編譯正確
   - 檢查音頻處理鏈

3. **上傳失敗**
   - 檢查網路連接
   - 確認 SondeHub 設定
   - 檢查數據格式

### 日誌監控

```bash
# 查看系統日誌
journalctl -u auto_rx -f

# 查看解碼日誌
tail -f auto_rx/log/system.log
```

## 相關連結

- [原始 radiosonde_auto_rx 專案](https://github.com/projecthorus/radiosonde_auto_rx)
- [SondeHub 全球追蹤平台](https://sondehub.org/)
- [RD41 dropsonde 解碼專案](https://github.com/byte-me404/rd41-dropsonde-decode)

## 授權

本專案基於 GNU GPL v3 授權條款。

## 貢獻

歡迎提交 Issue 和 Pull Request 來改善這個專案。

## 聯絡資訊

如有問題或建議，請透過 GitHub Issues 聯繫。

---

**注意**: 本專案僅供教育和研究用途。使用前請確保遵守當地法規和頻譜使用規定。