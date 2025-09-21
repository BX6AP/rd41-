# RD41 Decoding Project

This is an RD41 dropsonde decoding system based on `radiosonde_auto_rx`, specifically designed for receiving, decoding and tracking Vaisala RD41 radiosonde telemetry data.

> **Personal Note**: I've been working on this project for several months now. The RD41 dropsonde signals are quite challenging to decode compared to regular radiosondes, but the data quality is excellent once you get it working. The main issue I encountered was the GPS lock filtering being too aggressive - had to modify the filter logic to allow sensor data through even without GPS lock.

## Version History

- **v1.0.0** (2025-01-17): Initial release
  - Basic RD41 decoding support
  - SondeHub integration
  - Web interface
  
- **v1.0.1** (2025-01-18): Bug fixes
  - Fixed GPS lock filtering issue
  - Improved error handling
  - Added better logging

- **v1.1.0** (2025-01-20): Feature updates
  - Added batch upload support
  - Improved compression handling
  - Enhanced web UI

## Project Features

- 🎯 **RD41 Specific**: Optimized RD41 dropsonde decoding support
- 📡 **Automatic Signal Detection**: Auto-scan and detect RD41 signals in 400-406 MHz band
- 🔄 **Real-time Decoding**: Use `rd94rd41drop` decoder for real-time data decoding
- 🌐 **SondeHub Integration**: Automatically upload data to global SondeHub tracking platform
- 📊 **Web Interface**: Provide real-time map display and data monitoring
- 🔧 **Easy Configuration**: Simple configuration files and automated scripts

## Supported Radiosonde Types

### Vaisala RD41
- **Frequency Range**: 400-406 MHz
- **Modulation**: FSK 4800 baud
- **Encoding**: Manchester, 8N1
- **Data Rate**: 240 bytes/sec
- **Position Update**: 2 Hz
- **Velocity Update**: 4 Hz

## System Requirements

- **Hardware**: Raspberry Pi 3B+ or higher
- **SDR**: RTLSDR or AirSpy
- **Operating System**: Raspberry Pi OS (64-bit)
- **Python**: 3.8+
- **Memory**: Minimum 2GB RAM

## Quick Start

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y git build-essential cmake libusb-1.0-0-dev \
    rtl-sdr librtlsdr-dev sox libsox-fmt-all python3-pip \
    python3-numpy python3-scipy python3-matplotlib

# Install Python packages
pip3 install -r auto_rx/requirements.txt
```

### 2. Compile Decoders

```bash
# Compile dropsonde decoder
cd demod/dropsonde/
make clean all

# Copy decoder to auto_rx directory
cd ../../auto_rx/
cp ../dropsonde/rd94rd41drop .
```

### 3. Configure System

```bash
# Copy configuration example
cp station.cfg.example station.cfg

# Edit configuration file
nano station.cfg
```

### 4. Start System

```bash
# Start RD41 decoding system
python3 auto_rx.py --config station.cfg
```

## Configuration

### Basic Configuration (station.cfg)

```ini
[location]
# Receiver station position
station_lat = 25.046088
station_lon = 121.517524
station_alt = 0

[sondehub]
# SondeHub upload settings
sondehub_enabled = True
sondehub_upload_rate = 15
sondehub_contact_email = your@email.com

[habitat]
# Station information
uploader_callsign = YOUR_CALLSIGN
uploader_antenna = "RD41 dedicated antenna"
```

### Frequency Configuration

RD41 dropsonde typically operates on the following frequencies:
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

## Data Format

Decoder outputs standard JSON format:

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

## Features

### 1. Automatic Signal Detection
- Auto-scan in 400-406 MHz band
- Detect RD41 signal characteristics (sync header 0x1ACFFC1D)
- Automatically switch to decoding mode

### 2. Real-time Decoding
- Use `rd94rd41drop` decoder
- Support position, temperature, humidity, pressure data
- Real-time error checking and data validation

### 3. Data Upload
- **SondeHub**: Global tracking platform
- **APRS-IS**: Amateur radio network
- **Local Recording**: CSV file storage

### 4. Web Interface
- Real-time map display
- Telemetry data table
- System status monitoring

## Use Cases

### Hurricane Research
- RD41 radiosondes dropped from weather aircraft
- Provide high-precision vertical atmospheric profile data
- Support hurricane intensity and path prediction

### Storm Tracking
- Real-time storm system tracking
- Collect critical meteorological data
- Support weather forecast models

## Technical Details

### Signal Processing Flow
```
RD41 Radiosonde → RTLSDR → FM Demodulation → rd94rd41drop → JSON Data → SondeHub
```

### Decoding Parameters
- **Sample Rate**: 48 kHz
- **Filter**: High-pass 20Hz, low-pass 2600Hz
- **Frame Length**: 120 bytes
- **Error Check**: CRC16 verification

## Troubleshooting

### Common Issues

1. **Cannot detect signal**
   - Check antenna connection
   - Confirm frequency settings are correct
   - Check SDR hardware status

2. **Decoding failure**
   - Check signal quality
   - Confirm decoder compilation is correct
   - Check audio processing chain

3. **Upload failure**
   - Check network connection
   - Confirm SondeHub settings
   - Check data format

### Log Monitoring

```bash
# View system logs
journalctl -u auto_rx -f

# View decode logs
tail -f auto_rx/log/system.log
```

## Related Links

- [Original radiosonde_auto_rx project](https://github.com/projecthorus/radiosonde_auto_rx)
- [SondeHub global tracking platform](https://sondehub.org/)
- [RD41 dropsonde decoding project](https://github.com/byte-me404/rd41-dropsonde-decode)

## License

This project is based on GNU GPL v3 license.

## Contributing

Welcome to submit Issues and Pull Requests to improve this project.

## Contact

For questions or suggestions, please contact via GitHub Issues.

---

**Note**: This project is for educational and research purposes only. Please ensure compliance with local regulations and spectrum usage rules before use.