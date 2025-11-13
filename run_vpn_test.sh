#!/bin/bash
# Test different configurations for VPN access

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    SHADOW C2 VPN TEST CONFIGURATIONS                        ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"

echo ""
echo "[+] Проверка доступных конфигураций..."

# Test 1: Standard localhost
echo ""
echo "=== Тест 1: Стандартная конфигурация (localhost) ==="
echo "Запускаем на localhost:8080..."
python3 run_split_servers.py --admin-port 8080 &
PID1=$!
sleep 3
if netstat -tulpn 2>/dev/null | grep -q ":8080" || ss -tulpn 2>/dev/null | grep -q ":8080"; then
    echo "[✓] Сервер запущен на localhost:8080"
    echo "    Доступ: http://localhost:8080/dashboard"
    kill $PID1 2>/dev/null
else
    echo "[!] Сервер НЕ запущен на localhost:8080"
fi

# Test 2: All interfaces
echo ""
echo "=== Тест 2: Все интерфейсы (0.0.0.0) ==="
echo "Запускаем на 0.0.0.0:8080..."
python3 run_split_servers.py --admin-host 0.0.0.0 --admin-port 8080 &
PID2=$!
sleep 3
if netstat -tulpn 2>/dev/null | grep -q "0.0.0.0:8080" || ss -tulpn 2>/dev/null | grep -q "0.0.0.0:8080"; then
    echo "[✓] Сервер запущен на 0.0.0.0:8080"
    echo "    Доступ: http://0.0.0.0:8080/dashboard"
    echo "    Через VPN: http://10.8.0.1:8080/dashboard"
    kill $PID2 2>/dev/null
else
    echo "[!] Сервер НЕ запущен на 0.0.0.0:8080"
fi

# Test 3: VPN interface only
echo ""
echo "=== Тест 3: Только VPN интерфейс ==="
echo "Запускаем на 10.8.0.1:8080..."
python3 run_split_servers.py --admin-host 10.8.0.1 --admin-port 8080 &
PID3=$!
sleep 3
if netstat -tulpn 2>/dev/null | grep -q "10.8.0.1:8080" || ss -tulpn 2>/dev/null | grep -q "10.8.0.1:8080"; then
    echo "[✓] Сервер запущен на 10.8.0.1:8080"
    echo "    Доступ: http://10.8.0.1:8080/dashboard"
    kill $PID3 2>/dev/null
else
    echo "[!] Сервер НЕ запущен на 10.8.0.1:8080"
fi

echo ""
echo "[+] Рекомендации:"
echo "    1. Используйте конфигурацию которая работает"
echo "    2. Проверьте доступ через браузер"
echo "    3. Убедитесь что VPN активен"
echo "    4. Проверьте firewall если есть"
echo ""
echo "Для постоянного запуска используйте:"
echo "nohup python3 run_split_servers.py --admin-host Р’Р°С€_Р’Р°СЂРёР°РЅС‚ --admin-port 8080 &"