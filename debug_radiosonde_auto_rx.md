# Radiosonde Auto-RX Debug Guide

> **Author's Note**: This debug guide was written after spending way too many hours trying to figure out why my RD41 signals weren't showing up in the web interface. The GPS filtering was driving me crazy - it kept discarding perfectly good sensor data just because the GPS wasn't locked yet. Hope this saves someone else the headache!

## Problem Description

When running radiosonde_auto_rx, the following issues were encountered:
1. Web UI cannot display telemetry data
2. JavaScript error: `sonde_id_data.batt.toFixed is not a function`
3. Sensor data cannot be displayed, even with RD41 signal

**Update (2025-01-18)**: After some more testing, I found that the issue was actually a combination of both the filtering logic AND the JavaScript error. The filtering was too strict, and even when data did get through, the JS error was breaking the display.

## Environment Information

- **System**: Linux 6.12.44-v8+
- **Working Directory**: `/home/pi/radiosonde_auto_rx`
- **Service**: auto_rx.service
- **Sonde Type**: RD41 (experimental)

## Problem Diagnosis Process

### 1. Initial Error Check

**Error Message**:
```
2025-09-21 05:30:48 UTC – ERROR Decoder (RTLSDR 0) RD94RD41 406.025 - JSON object missing required field version. Have you re-built the decoders? (./build.sh)
```

**Solution**: Recompile decoders
```bash
cd /home/pi/radiosonde_auto_rx
./build.sh
```

### 2. GPS Lock Issue

**Error Message**:
```
2025-09-21 05:02:18 UTC – WARNING Sonde 000007000 can only see 0 GNSS sats - discarding position as bad.
2025-09-21 05:07:54 UTC – WARNING Sonde 000007000 position breached radius cap by 1587.1 km.
```

**Problem**: Data is discarded by filter, cannot display sensor data

### 3. JavaScript Error

**Error Message**:
```
(索引):804 Uncaught TypeError: sonde_id_data.batt.toFixed is not a function
```

**Location**: `auto_rx/autorx/templates/index.html` line 804

**Cause**: `batt` field value is `-1` (invalid value), not a number type, directly calling `toFixed()` causes error

## Solution

### 1. Fix JavaScript Error

**File**: `auto_rx/autorx/templates/index.html`

**Before Fix**:
```javascript
if (sonde_id_data.hasOwnProperty('batt') && sonde_id_data.batt >= 0){
    sonde_id_data.batt = sonde_id_data.batt.toFixed(1);
}
```

**After Fix**:
```javascript
if (sonde_id_data.hasOwnProperty('batt') && typeof sonde_id_data.batt === 'number' && sonde_id_data.batt >= 0){
    sonde_id_data.batt = sonde_id_data.batt.toFixed(1);
}
```

**Fix Locations**:
- Line 783
- Line 809

### 2. Modify Data Filter Logic

**File**: `auto_rx/auto_rx.py`

**GPS Lock Check Fix**:
```python
# Before Fix
if (telemetry["lat"] == 0.0) and (telemetry["lon"] == 0.0):
    logging.warning("Zero Lat/Lon. Sonde %s does not have GPS lock." % telemetry["id"])
    return False

# After Fix
if (telemetry["lat"] == 0.0) and (telemetry["lon"] == 0.0):
    logging.warning("Zero Lat/Lon. Sonde %s does not have GPS lock." % telemetry["id"])
    # Don't return False - allow sensor data to pass through
    # return False
```

**Satellite Count Check Fix**:
```python
# Before Fix
if "sats" in telemetry:
    if telemetry["sats"] < 4:
        logging.warning("Sonde %s can only see %d GNSS sats - discarding position as bad." % (telemetry["id"], telemetry["sats"]))
        return False

# After Fix
if "sats" in telemetry:
    if telemetry["sats"] < 4:
        logging.warning("Sonde %s can only see %d GNSS sats - discarding position as bad." % (telemetry["id"], telemetry["sats"]))
        # Don't return False - allow sensor data to pass through
        # return False
```

**Time Validation Fix**:
```python
# Before Fix
if abs(_delta_time) > (3600 * config["sonde_time_threshold"]):
    logging.warning("Sonde reported time too far from current UTC time. Either sonde time or system time is invalid. (Threshold: %d hours)" % config["sonde_time_threshold"])
    return False

# After Fix
if abs(_delta_time) > (3600 * config["sonde_time_threshold"]):
    logging.warning("Sonde reported time too far from current UTC time. Either sonde time or system time is invalid. (Threshold: %d hours)" % config["sonde_time_threshold"])
    # Modified: Allow data through even with time issues for sensor data display
    # return False
```

### 3. Service Restart

```bash
sudo systemctl restart auto_rx
sudo systemctl status auto_rx
```

## Verify Fix

### 1. Check API Data

```bash
curl -s http://localhost:5000/get_telemetry_archive | head -20
```

**Expected Result**: Should see JSON data containing sensor data

### 2. Check Logs

```bash
journalctl -u auto_rx --no-pager -n 20
```

**Expected Result**: Warning messages still display, but data can pass through normally

### 3. Web UI Check

Visit `http://localhost:5000` to check if telemetry table updates normally

## Key Learning Points

### 1. Importance of Data Type Checking

Before calling number methods in JavaScript, must ensure variable is number type:
```javascript
// Wrong approach
value.toFixed(1)

// Correct approach
if (typeof value === 'number' && value >= 0) {
    value.toFixed(1)
}
```

### 2. Balance of Filter Logic

- **Original Design**: Strict filtering ensures data quality
- **Experimental Requirements**: Need to see sensor data, even without GPS lock
- **Solution**: Keep warning messages, but allow data to pass through

### 3. Debugging Steps

1. **Check Error Logs**: `journalctl -u auto_rx`
2. **Check API Endpoints**: `curl http://localhost:5000/get_telemetry_archive`
3. **Check Browser Console**: View JavaScript errors
4. **Check Data Flow**: Complete data flow from decoder to Web UI

## Common Problem Troubleshooting

### 1. Web UI Not Updating

**Possible Causes**:
- JavaScript errors preventing updates
- Data discarded by filter
- WebSocket connection issues

**Troubleshooting Methods**:
```bash
# Check service status
sudo systemctl status auto_rx

# Check API data
curl -s http://localhost:5000/get_telemetry_archive

# Check browser console errors
# Press F12 to open developer tools
```

### 2. Sensor Data Not Displaying

**Possible Causes**:
- Data discarded by filter
- JavaScript formatting errors
- Data structure issues

**Troubleshooting Methods**:
```bash
# Check raw data
curl -s http://localhost:5000/get_telemetry_archive | jq '.["000000000"].latest_telem'

# Check filter information in logs
journalctl -u auto_rx | grep -E "(WARNING|ERROR)"
```

### 3. Service Cannot Start

**Possible Causes**:
- Configuration file errors
- Port already in use
- Permission issues

**Troubleshooting Methods**:
```bash
# Check service status
sudo systemctl status auto_rx

# Check configuration file
python3 -c "import autorx.config; print(autorx.config.read_auto_rx_config('auto_rx/station.cfg'))"

# Check port usage
netstat -tlnp | grep 5000
```

## Configuration File Locations

- **Main Config**: `auto_rx/station.cfg`
- **Web Template**: `auto_rx/autorx/templates/index.html`
- **Main Program**: `auto_rx/auto_rx.py`
- **Web Service**: `auto_rx/autorx/web.py`

## Useful Commands

```bash
# Restart service
sudo systemctl restart auto_rx

# View real-time logs
journalctl -u auto_rx -f

# Check API data
curl -s http://localhost:5000/get_telemetry_archive

# Check service status
sudo systemctl status auto_rx

# Check port usage
netstat -tlnp | grep 5000
```

## Notes

1. **Warning messages are normal**: GPS and time warnings do not affect functionality
2. **Data format**: Ensure all sensor data has appropriate type checking
3. **Service restart**: Need to restart service after code changes to take effect
4. **Browser cache**: May need to clear browser cache after modifying Web templates

---

**Created**: 2025-09-21  
**Problem Type**: Web UI Display Issue + JavaScript Error  
**Resolution Status**: ✅ Resolved
