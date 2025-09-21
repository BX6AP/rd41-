# SondeHub Uploader

This is a web application for decoding Base64 encoded gzip data and uploading to SondeHub.

> **Real-world Usage**: I've been using this tool for uploading RD41 dropsonde data to SondeHub for the past few months. The compression works great - typically reduces data size by 40-60%. The main challenge was handling the different data formats from various decoders, but the current version handles most cases well.

## Known Issues

- **Browser Compatibility**: Some older browsers don't support the DecompressionStream API
- **Large Files**: Files over 10MB might cause memory issues in the frontend version
- **Network Timeouts**: The backend sometimes times out on slow connections (working on this)

## Recent Updates

- **2025-01-20**: Fixed compression ratio display bug
- **2025-01-19**: Added better error messages for invalid data
- **2025-01-18**: Improved batch upload handling

## Features

- 🔍 **Base64 Decoding**: Decode Base64 encoded gzip data
- 📦 **gzip Decompression**: Automatically decompress gzip format data
- 📋 **JSON Preview**: Display decoded JSON data
- 🚀 **SondeHub Upload**: Direct upload to SondeHub API
- 📊 **Statistics**: Display data size, compression ratio and other statistics
- 🌐 **Web Interface**: User-friendly web interface

## File Description

### 1. Frontend Only Version
- `simple_sondehub_uploader.html` - Pure HTML/JavaScript version
- Requires modern browser support (Chrome 80+, Firefox 65+)
- Uses browser built-in DecompressionStream API

### 2. Backend Service Version
- `sondehub_uploader_server.py` - Flask backend service
- `start_uploader.sh` - Startup script
- Supports all browsers
- Provides RESTful API

## Usage

### Method 1: Frontend Only Version

1. Open `simple_sondehub_uploader.html` directly in browser
2. Paste Base64 encoded gzip data
3. Click "Decode and Display" to view data
4. Click "Upload to SondeHub" to upload data

### Method 2: Backend Service Version

1. Start service:
```bash
cd /home/pi/radiosonde_auto_rx
./start_uploader.sh
```

2. Open `http://localhost:5001` in browser

3. Usage steps same as frontend only version

## API Endpoints

### POST /api/decode
Decode Base64 encoded gzip data

**Request Body:**
```json
{
  "base64_data": "H4sIAJwfzGgC/4WST4/TMBDFv0qVc2v5T5zEvcFlT0gVXQFitbKmzWTXUuIE2+myQnx3PC4rijiQXOLnn9+8yfjhRxXnIb1AQOthwmq/qQL0bo6z79HCmmYbvlfbzR/sgiG62RMpWMfk7oQJGkLWZZyhx2DPMI7RPRXm/Zfm3cHeg1vQWfUXtszRpavVg9SM1w3vuu1GSMG0aLWstxv+eHsAfELvgWzJKLkJbcAzugv2JEou9Y6bnejuhd5zua81M6b5SvAEfh3gnNaAgdhP4CKMUHxel9L4x2MtSqsYHIykfBZaCsFNUdfTLbg73h1I7iEhBflf/RFSRqRiouFckVAaF5IzoZu8hpEAbZiSKndeDeE6D6HKMuG0kEHDZF49r5PrXXrNCmc8C0vAGHNvdIBzw2qyPEEiT1WICClSgfx5wdFe8vcup1H51ebtedt9JpI1Whptct5Wa14bqov5cvgnqtIYpjveKtF2vJNN6WkI+G1Ff6ZcNZd5pC1V9vTHpSzJB3tGn0rQTGSgodGXDQxhJvJNWZappFctxQqxFnYC508zhP46hg+1rKt/9uzwcp2G5uVentYQk6UhFXetVfHD4fYGVneHY/Vbvp0pyT8ffwHitlDeKAMAAA=="
}
```

**Response:**
```json
{
  "success": true,
  "data": [...],
  "decompressed_size": 808,
  "packet_count": 1
}
```

### POST /api/upload
Upload data to SondeHub

**Request Body:**
```json
{
  "data": [...]
}
```

**Response:**
```json
{
  "success": true,
  "status_code": 200,
  "upload_size": 475,
  "packet_count": 1
}
```

### GET /api/health
Health check

**Response:**
```json
{
  "status": "healthy",
  "service": "SondeHub Uploader",
  "version": "1.0.0"
}
```

## Example Usage

### Using curl commands

1. **Decode data:**
```bash
curl -X POST http://localhost:5001/api/decode \
  -H "Content-Type: application/json" \
  -d '{"base64_data": "H4sIAJwfzGgC/4WST4/TMBDFv0qVc2v5T5zEvcFlT0gVXQFitbKmzWTXUuIE2+myQnx3PC4rijiQXOLnn9+8yfjhRxXnIb1AQOthwmq/qQL0bo6z79HCmmYbvlfbzR/sgiG62RMpWMfk7oQJGkLWZZyhx2DPMI7RPRXm/Zfm3cHeg1vQWfUXtszRpavVg9SM1w3vuu1GSMG0aLWstxv+eHsAfELvgWzJKLkJbcAzugv2JEou9Y6bnejuhd5zua81M6b5SvAEfh3gnNaAgdhP4CKMUHxel9L4x2MtSqsYHIykfBZaCsFNUdfTLbg73h1I7iEhBflf/RFSRqRiouFckVAaF5IzoZu8hpEAbZiSKndeDeE6D6HKMuG0kEHDZF49r5PrXXrNCmc8C0vAGHNvdIBzw2qyPEEiT1WICClSgfx5wdFe8vcup1H51ebtedt9JpI1Whptct5Wa14bqov5cvgnqtIYpjveKtF2vJNN6WkI+G1Ff6ZcNZd5pC1V9vTHpSzJB3tGn0rQTGSgodGXDQxhJvJNWZappFctxQqxFnYC508zhP46hg+1rKt/9uzwcp2G5uVentYQk6UhFXetVfHD4fYGVneHY/Vbvp0pyT8ffwHitlDeKAMAAA=="}'
```

2. **Upload data:**
```bash
curl -X POST http://localhost:5001/api/upload \
  -H "Content-Type: application/json" \
  -d '{"data": [{"software_name": "radiosonde_auto_rx", "type": "RS41", "serial": "W1521109", ...}]}'
```

## System Requirements

### Frontend Only Version
- Modern browser (Chrome 80+, Firefox 65+, Safari 16+)
- Support for DecompressionStream API

### Backend Service Version
- Python 3.6+
- Flask
- requests
- flask-cors

## Install Dependencies

```bash
pip3 install flask requests flask-cors
```

## Troubleshooting

### 1. Decode Failure
- Check if Base64 data is complete
- Confirm data is valid gzip format
- Check if JSON format is correct

### 2. Upload Failure
- Check network connection
- Confirm SondeHub API is accessible
- Check if data format meets SondeHub requirements

### 3. Browser Compatibility
- Frontend only version requires browser with DecompressionStream support
- Recommend using backend service version for better compatibility

## Technical Details

### Data Flow
1. Base64 decode → Binary data
2. gzip decompress → JSON string
3. JSON parse → Object array
4. Recompress → gzip format
5. HTTPS PUT → SondeHub API

### Compression Effect
- Original JSON: ~800 bytes
- After gzip compression: ~475 bytes
- Compression ratio: ~60%

### Security Considerations
- Use HTTPS transmission
- Validate input data format
- Error handling and logging

## License

This project uses MIT license.

## Support

For questions or suggestions, please contact the development team.
