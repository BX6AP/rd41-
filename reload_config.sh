#!/bin/bash
#
# Reload Auto-RX Configuration Script
# This script reloads the configuration without restarting the service
#

echo "Reloading Auto-RX configuration..."

# Method 1: Send SIGHUP signal to auto_rx process
if pgrep -f "auto_rx.py" > /dev/null; then
    PID=$(pgrep -f "auto_rx.py")
    echo "Sending SIGHUP signal to auto_rx process (PID: $PID)"
    kill -HUP $PID
    echo "Configuration reload signal sent successfully"
else
    echo "Auto-RX process not found"
    exit 1
fi

# Wait a moment and check if the reload was successful
sleep 2

# Check if the process is still running
if pgrep -f "auto_rx.py" > /dev/null; then
    echo "✅ Auto-RX service is running - configuration reloaded"
else
    echo "❌ Auto-RX service is not running - check logs for errors"
    exit 1
fi
