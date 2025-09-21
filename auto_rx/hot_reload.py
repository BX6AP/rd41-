#!/usr/bin/env python3
"""
Hot Reload Configuration for Radiosonde Auto-RX
This script allows reloading configuration without restarting the service
"""

import os
import signal
import sys
import time
import logging
from pathlib import Path

def send_reload_signal():
    """Send SIGHUP signal to auto_rx service to trigger configuration reload"""
    try:
        # Find the auto_rx process
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'auto_rx.py'], capture_output=True, text=True)
        
        if result.returncode == 0:
            pid = int(result.stdout.strip())
            os.kill(pid, signal.SIGHUP)
            print(f"Sent reload signal to auto_rx process (PID: {pid})")
            return True
        else:
            print("auto_rx process not found")
            return False
    except Exception as e:
        print(f"Error sending reload signal: {e}")
        return False

def monitor_config_file(config_file, callback):
    """Monitor configuration file for changes and trigger callback"""
    if not os.path.exists(config_file):
        print(f"Configuration file {config_file} not found")
        return
    
    last_modified = os.path.getmtime(config_file)
    print(f"Monitoring {config_file} for changes...")
    
    while True:
        try:
            current_modified = os.path.getmtime(config_file)
            if current_modified > last_modified:
                print(f"Configuration file changed at {time.ctime(current_modified)}")
                last_modified = current_modified
                callback()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping configuration monitor...")
            break
        except Exception as e:
            print(f"Error monitoring config file: {e}")
            time.sleep(5)

if __name__ == "__main__":
    config_file = "/home/pi/radiosonde_auto_rx/auto_rx/station.cfg"
    
    if len(sys.argv) > 1 and sys.argv[1] == "reload":
        # One-time reload
        send_reload_signal()
    else:
        # Continuous monitoring
        monitor_config_file(config_file, send_reload_signal)
