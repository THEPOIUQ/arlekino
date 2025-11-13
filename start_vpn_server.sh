#!/bin/bash
# Start C2 server with VPN support

echo "Starting Shadow C2 server with VPN interface..."

# Change to correct directory
cd $(dirname "$0")

# Check if VPN interface exists
if ! ip addr show | grep -q "10.8.0.1"; then
    echo "[!] VPN interface 10.8.0.1 not found!"
    echo "[!] Please start your VPN first"
    exit 1
fi

echo "[✓] VPN interface found"

# Start with VPN interface
echo "[+] Starting server on VPN interface..."
python3 run_split_servers.py --admin-host 10.8.0.1 --admin-port 8080 > /dev/null 2>&1 &
SERVER_PID=$!

sleep 3

# Check if server started
if netstat -tulpn 2>/dev/null | grep -q ":8080" || ss -tulpn 2>/dev/null | grep -q ":8080"; then
    echo "[✓] Server started successfully!"
    echo ""
    echo "🎯 Доступ к админке:"
    echo "   • Через VPN: http://10.8.0.1:8080/dashboard"
    echo "   • С localhost: http://localhost:8080/dashboard"
    echo ""
    echo "🔑 Логин: admin / shadowc2"
    echo ""
    echo "PID: $SERVER_PID"
    echo ""
    echo "Для остановки: kill $SERVER_PID"
else
    echo "[!] Failed to start server"
    echo "[!] Check logs for errors"
fi