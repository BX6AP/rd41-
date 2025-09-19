# Radiosonde Auto RX - Custom Build

這是一個基於 [projecthorus/radiosonde_auto_rx](https://github.com/projecthorus/radiosonde_auto_rx) 的自定義版本，專門用於氣象探空儀信號接收和解碼。

## 主要功能

- 自動掃描和解碼多種氣象探空儀信號
- 支持 RS41, RS92, DFM, iMet, M10, M20 等多種探空儀類型
- 實時數據上傳到 SondeHub
- Web界面監控和配置
- 支持多個 SDR 設備同時工作

## 自定義修改

- 修復了 `sdr_wrappers.py` 中的模組導入問題
- 添加了 SondeHub 集成功能
- 優化了系統資源使用
- 移除了不必要的 UHD/GNU Radio 依賴

## 系統要求

- Raspberry Pi (推薦 Pi 4)
- RTL-SDR 或其他兼容的 SDR 設備
- Python 3.11+
- 至少 2GB 可用磁盤空間

## 安裝

1. 克隆此 repository:
```bash
git clone https://github.com/YOUR_USERNAME/radiosonde_auto_rx.git
cd radiosonde_auto_rx
```

2. 安裝依賴:
```bash
sudo apt update
sudo apt install python3-flask python3-flask-socketio python3-requests python3-semver python3-dateutil
pip3 install --user simple-websocket --break-system-packages
```

3. 編譯解碼器:
```bash
make
```

## 使用方法

1. 配置 `station.cfg` 文件
2. 運行主程序:
```bash
python3 auto_rx/auto_rx.py
```

3. 訪問 Web 界面: http://localhost:8080

## 文件結構

- `auto_rx/` - 主要程序代碼
- `demod/` - 解碼器源代碼
- `scan/` - 掃描器代碼
- `utils/` - 工具程序
- `log/` - 日誌文件

## 授權

基於原項目 GNU GPL v3 授權

## 原始項目

此項目基於 [projecthorus/radiosonde_auto_rx](https://github.com/projecthorus/radiosonde_auto_rx) 開發