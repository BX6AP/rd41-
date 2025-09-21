# SondeHub HTTPS PUT Request Packet Details

## Overview

This document details the complete packet content when the `radiosonde_auto_rx` system sends HTTPS PUT requests to SondeHub, including HTTP headers, request body, compression processing and transmission details.

## 1. HTTP Request Basic Information

### 1.1 Request Method and URL
```
Method: PUT
URL: https://api.v2.sondehub.org/sondes/telemetry
Protocol: HTTPS (TLS 1.2/1.3)
Port: 443
```

### 1.2 Connection Parameters
```
Connection Timeout: 20 seconds
Read Timeout: 6.1 seconds
Retry Count: Maximum 5 times
Retry Strategy: Exponential backoff
```

## 2. HTTP Headers

### 2.1 Standard Headers
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

### 2.2 Header Description
| Header | Value | Description |
|--------|-------|-------------|
| `User-Agent` | `autorx-1.8.2-beta6` | Identify upload software and version |
| `Content-Type` | `application/json` | Specify content type as JSON |
| `Content-Encoding` | `gzip` | Specify content uses gzip compression |
| `Content-Length` | `438` | Compressed content length (bytes) |
| `Date` | `Mon, 18 Sep 2025 15:02:37 GMT` | Request send time (UTC) |

## 3. Request Body

### 3.1 JSON Data Structure
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

### 3.2 Field Description

#### 3.2.1 Software Information
| Field | Type | Description | Example Value |
|-------|------|-------------|---------------|
| `software_name` | string | Software name | "radiosonde_auto_rx" |
| `software_version` | string | Software version | "1.8.2-beta6" |
| `uploader_callsign` | string | Uploader callsign | "BX6AP_Taipei_3" |
| `uploader_position` | array | Uploader position [lat, lon, alt] | [25.046088, 121.517524, 0] |
| `uploader_antenna` | string | Antenna information | "" |
| `time_received` | string | Receive time (ISO 8601) | "2025-09-18T15:02:37.996Z" |

#### 3.2.2 Radiosonde Basic Information
| Field | Type | Description | Example Value |
|-------|------|-------------|---------------|
| `manufacturer` | string | Manufacturer | "Vaisala" |
| `type` | string | Radiosonde type | "RS41" |
| `serial` | string | Serial number | "W1521109" |
| `subtype` | string | Subtype | "RS41-SGP" |
| `datetime` | string | Data time (ISO 8601) | "2025-09-18T15:02:37.996Z" |
| `frame` | integer | Frame number | 1326 |

#### 3.2.3 Position Information
| Field | Type | Description | Example Value |
|-------|------|-------------|---------------|
| `lat` | float | Latitude (degrees) | 23.16017 |
| `lon` | float | Longitude (degrees) | 120.15602 |
| `alt` | float | Altitude (meters) | 89.58712 |

#### 3.2.4 Sensor Data
| Field | Type | Description | Example Value |
|-------|------|-------------|---------------|
| `temp` | float | Temperature (°C) | 26.3 |
| `humidity` | float | Humidity (%) | 0.0 |
| `pressure` | float | Pressure (hPa) | 1009.43 |
| `batt` | float | Battery voltage (V) | 3.0 |
| `sats` | integer | Satellite count | 6 |

#### 3.2.5 Motion Data
| Field | Type | Description | Example Value |
|-------|------|-------------|---------------|
| `vel_v` | float | Vertical velocity (m/s) | -8.000380000000002 |
| `vel_h` | float | Horizontal velocity (m/s) | 1.1119492662446442 |
| `heading` | float | Heading (degrees) | 180.0 |

#### 3.2.6 Technical Data
| Field | Type | Description | Example Value |
|-------|------|-------------|---------------|
| `frequency` | float | Frequency (MHz) | 402.047 |
| `snr` | float | Signal-to-noise ratio (dB) | 22.4 |
| `f_centre` | float | Frequency center (Hz) | 402047625.0 |
| `f_error` | float | Frequency error (Hz) | 625.0 |
| `ppm` | float | Frequency correction (PPM) | -5.125 |

#### 3.2.7 RS41 Specific Data
| Field | Type | Description | Example Value |
|-------|------|-------------|---------------|
| `rs41_mainboard` | string | Mainboard model | "RSM424" |
| `rs41_mainboard_fw` | string | Firmware version | "20506" |
| `burst_timer` | integer | Burst timer | 65535 |

#### 3.2.8 Reference Information
| Field | Type | Description | Example Value |
|-------|------|-------------|---------------|
| `ref_position` | string | Position reference | "GPS" |
| `ref_datetime` | string | Time reference | "GPS" |

## 4. Data Compression Processing

### 4.1 Compression Flow
```python
# 1. Serialize JSON
_telem_json = json.dumps(telem_list).encode("utf-8")

# 2. gzip compression
_compressed_payload = gzip.compress(_telem_json)

# 3. Set Content-Encoding header
headers["Content-Encoding"] = "gzip"
```

### 4.2 Compression Effect
| Item | Size | Description |
|------|------|-------------|
| Original JSON | 730 bytes | Uncompressed JSON data |
| After gzip compression | 438 bytes | Compressed data |
| Compression ratio | 60% | Save 40% transmission volume |
| Compression time | < 1ms | Compression processing time |

## 5. TLS Encrypted Transmission

### 5.1 Encryption Parameters
```
Protocol: TLS 1.2 or TLS 1.3
Cipher Suite: AES-256-GCM or ChaCha20-Poly1305
Certificate Verification: Enabled
HSTS: Supported
```

### 5.2 Transport Layer Security
- **End-to-end encryption**: From client to SondeHub server
- **Certificate verification**: Verify server identity
- **Integrity check**: Prevent data tampering
- **Replay attack protection**: Timestamp verification

## 6. Actual Transmission Packet

### 6.1 Complete HTTP Request
```http
PUT /sondes/telemetry HTTP/1.1
Host: api.v2.sondehub.org
User-Agent: autorx-1.8.2-beta6
Content-Type: application/json
Content-Encoding: gzip
Content-Length: 438
Date: Mon, 18 Sep 2025 15:02:37 GMT
Connection: keep-alive

[gzip compressed JSON data - 438 bytes]
```

### 6.2 Transmission Statistics
```
Total packet size: ~500-600 bytes (including HTTP headers)
Valid data: 438 bytes (compressed)
HTTP headers: ~150 bytes
TLS overhead: ~50-100 bytes
```

## 7. Server Response

### 7.1 Success Response (HTTP 200)
```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 0
Date: Mon, 18 Sep 2025 15:02:38 GMT
Server: nginx/1.18.0
```

### 7.2 Error Response Example
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
Content-Length: 45
Date: Mon, 18 Sep 2025 15:02:38 GMT

{"error": "Invalid telemetry data format"}
```

### 7.3 Response Handling
| Status Code | Description | Handling Method |
|-------------|-------------|-----------------|
| 200 | Success | Clear buffer, continue upload |
| 400 | Request error | Log error, skip this batch |
| 500 | Server error | Retry upload |
| Other | Other errors | Decide retry or skip based on error type |

## 8. Upload Frequency and Batch Processing

### 8.1 Upload Strategy
```
Upload frequency: Every 15 seconds
Batch size: 1-50 packets
Buffer strategy: Time trigger + count trigger
```

### 8.2 Batch Upload Example
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

## 9. Monitoring and Debugging

### 9.1 Upload Logs
```
Sep 18 22:56:33 RS41 auto_rx[398560]: INFO:Sondehub Uploader - Uploaded 9 telemetry packets to Sondehub in 1.1 seconds.
Sep 18 22:56:49 RS41 auto_rx[398560]: INFO:Sondehub Uploader - Uploaded 16 telemetry packets to Sondehub in 1.2 seconds.
```

### 9.2 Compression Statistics Logs
```
Sep 18 22:56:33 RS41 auto_rx[398560]: DEBUG:Pre-compression: 730 bytes, post: 438 bytes. 60.0 % compression ratio, in 0.001 s
```

### 9.3 Error Logs
```
Sep 18 22:56:33 RS41 auto_rx[398560]: ERROR:Sondehub Uploader - Upload Failed: Connection timeout
Sep 18 22:56:33 RS41 auto_rx[398560]: ERROR:Sondehub Uploader - Upload failed with status 500
```

## 10. Performance Optimization

### 10.1 Compression Optimization
- Use gzip compression to reduce 40% transmission volume
- Batch upload to reduce HTTP request count
- Connection reuse to reduce TLS handshake overhead

### 10.2 Network Optimization
- Set appropriate timeout parameters
- Implement exponential backoff retry strategy
- Use HTTPS to ensure transmission reliability

### 10.3 Resource Management
- Limit buffer size to prevent memory overflow
- Regularly clean upload buffer
- Monitor upload success rate

## Summary

SondeHub HTTPS PUT request packet contains:

1. **HTTP Headers**: Include software identification, content type and compression information
2. **JSON Body**: Contains complete radiosonde telemetry data
3. **gzip Compression**: Reduces 40% transmission volume
4. **TLS Encryption**: Ensures data transmission security
5. **Batch Processing**: Improves upload efficiency
6. **Error Handling**: Implements reliable retry mechanism

The entire packet design ensures data integrity, security and transmission efficiency, providing a reliable data upload mechanism for global radiosonde tracking.
