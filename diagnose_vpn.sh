#!/bin/bash
# VPN Diagnostic Script

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    SHADOW C2 VPN DIAGNOSTIC                               ║"
echo ║                    Диагностика VPN подключения                              ║
"echo "╚══════════════════════════════════════════════════════════════════════════════╝"

echo ""
echo "[+] Проверка VPN интерфейса..."

# Check if VPN interface exists
if netstat -rn | grep -q "10.8"; then
    echo "[✓] VPN маршрут найден"
else
    echo "[!] VPN маршрут НЕ найден"
fi

# Check if 10.8.0.1 is in routing table
if netstat -rn | grep -q "10.8.0.1"; then
    echo "[✓] VPN интерфейс 10.8.0.1 найден"
else
    echo "[!] VPN интерфейс 10.8.0.1 НЕ найден"
fi

echo ""
echo "[+] Проверка открытых портов..."
netstat -tulpn | grep LISTEN | head -20

echo ""
echo "[+] Проверка процессов C2..."
ps aux | grep -E "(beacon|admin|shadow)" | grep -v grep

echo ""
echo "[+] Попытка запуска тестового сервера на 10.8.0.1:8080..."
python3 -m http.server 8080 --bind 10.8.0.1 &
HTTP_PID=$!
sleep 2
if netstat -tulpn | grep -q ":8080"; then
    echo "[✓] Тестовый сервер запущен на 10.8.0.1:8080"
    echo "    Попробуйте открыть http://10.8.0.1:8080"
else
    echo "[!] Не удалось запустить сервер на 10.8.0.1:8080"
fi
sleep 5
kill $HTTP_PID 2>/dev/null

echo ""
echo "[+] Рекомендации:"
echo "    1. Убедитесь что VPN активен"
echo "    2. Проверьте маршруты: netstat -rn"
echo "    3. Попробуйте другой порт: --admin-port 8080"
echo "    4. Проверьте firewall если есть"
echo ""
echo "Для запуска с VPN используйте:"
echo "sudo ./run_split_servers.py --admin-host 10.8.0.1 --admin-port 8080"