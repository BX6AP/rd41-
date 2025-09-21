# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-01-20

### Added
- Batch upload support for multiple packets
- Better compression handling with different levels
- Enhanced web UI with real-time statistics
- Rate limiting to prevent API abuse

### Changed
- Improved error handling for network timeouts
- Updated compression algorithm for better performance
- Enhanced logging with more detailed information

### Fixed
- GPS lock filtering being too aggressive
- JavaScript error with battery voltage display
- Memory leak in long-running sessions
- Compression ratio calculation bug

### Known Issues
- Large files (>10MB) may cause memory issues in frontend
- Some browsers don't support DecompressionStream API
- Network timeouts on slow connections (working on fix)

## [1.0.1] - 2025-01-18

### Fixed
- Critical bug in GPS lock filtering logic
- JavaScript error: `sonde_id_data.batt.toFixed is not a function`
- Data not displaying in web UI due to filtering issues

### Changed
- Modified telemetry filter to allow sensor data without GPS lock
- Improved error messages for better debugging

## [1.0.0] - 2025-01-17

### Added
- Initial RD41 dropsonde decoding support
- SondeHub integration for global tracking
- Web interface for real-time monitoring
- Base64/gzip data upload functionality
- Automatic signal detection in 400-406 MHz band
- Support for multiple frequency channels
- Real-time error checking and data validation

### Technical Details
- Based on `radiosonde_auto_rx` project
- Uses `rd94rd41drop` decoder for RD41 signals
- Implements FSK 4800 baud demodulation
- Manchester encoding with 8N1 configuration
- CRC16 error checking for data integrity

---

**Note**: This project is actively maintained. For bug reports or feature requests, please open an issue on GitHub.
