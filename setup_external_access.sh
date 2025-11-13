#!/bin/bash
# Shadow C2 External Access Setup Script
# Configures firewall and network for external C2 access

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    SHADOW C2 EXTERNAL ACCESS SETUP                          ║"
echo ║                    Настройка внешнего доступа                               ║
"echo "╚══════════════════════════════════════════════════════════════════════════════╝"

echo ""
echo "[+] Проверка системы..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "[!] Этот скрипт требует root прав для настройки firewall"
    echo "[!] Запустите с sudo"
    exit 1
fi

# Check if ufw is available
if ! command -v ufw &> /dev/null; then
    echo "[!] UFW (Uncomplicated Firewall) не найден"
    echo "[!] Установите: sudo apt install ufw"
    exit 1
fi

# Function to get local IP
get_local_ip() {
    hostname -I | awk '{print $1}'
}

# Function to get external IP
get_external_ip() {
    curl -s https://api.ipify.org || echo "Не определен"
}

# Function to check if port is open
check_port() {
    local port=$1
    if nc -z localhost $port 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to setup firewall
setup_firewall() {
    local port=$1
    local ip_whitelist=$2
    
    echo ""
    echo "[+] Настройка firewall..."
    
    # Reset ufw to defaults
    echo "y" | ufw reset
    
    # Default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH (important!)
    ufw allow ssh
    
    # Allow C2 port
    if [ -n "$ip_whitelist" ]; then
        echo "[+] Настройка доступа только для whitelist IP..."
        for ip in $ip_whitelist; do
            ufw allow from $ip to any port $port
            echo "    ✅ Разрешен доступ с $ip на порт $port"
        done
    else
        echo "[+] Разрешен доступ на порт $port со всех IP (НЕБЕЗОПАСНО!)"
        ufw allow $port/tcp
    fi
    
    # Enable firewall
    echo "y" | ufw enable
    
    echo "[✓] Firewall настроен"
}

# Function to test external access
test_external_access() {
    local port=$1
    local external_ip=$2
    
    echo ""
    echo "[+] Тестирование внешнего доступа..."
    
    if [ "$external_ip" != "Не определен" ]; then
        echo "[+] Внешний IP: $external_ip"
        echo "[+] Проверка порта $port..."
        
        # Test if port is accessible from outside
        if nc -z $external_ip $port 2>/dev/null; then
            echo "[✓] Порт $port доступен извне"
        else
            echo "[!] Порт $port НЕ доступен извне"
            echo "[!] Проверьте роутер/NAT настройки"
        fi
    else
        echo "[!] Не удалось определить внешний IP"
        echo "[!] Проверьте интернет соединение"
    fi
}

# Function to show security recommendations
show_security_tips() {
    echo ""
    echo "🔒 РЕКОМЕНДАЦИИ ПО БЕЗОПАСНОСТИ:"
    echo "================================="
    echo ""
    echo "1. ИСПОЛЬЗУЙТЕ IP WHITELIST:"
    echo "   ./setup_external_access.sh --port 8080 --whitelist 1.2.3.4,5.6.7.8"
    echo ""
    echo "2. НАСТРОЙТЕ HTTPS:"
    echo "   - Получите SSL сертификат"
    echo "   - Используйте reverse proxy (nginx)"
    echo ""
    echo "3. МОНИТОРИНГ:"
    echo "   - Проверяйте логи регулярно"
    echo "   - Настройте alerts на подозрительную активность"
    echo ""
    echo "4. РЕГУЛЯРНОЕ ОБНОВЛЕНИЕ:"
    echo "   - Обновляйте систему"
    echo "   - Меняйте пароли"
    echo ""
}

# Main function
main() {
    local port=8080
    local ip_whitelist=""
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --port)
                port="$2"
                shift 2
                ;;
            --whitelist)
                ip_whitelist="$2"
                shift 2
                ;;
            -h|--help)
                echo "Использование: $0 [--port PORT] [--whitelist IP1,IP2,...]"
                echo ""
                echo "Примеры:"
                echo "  $0 --port 8080                          # Открыть порт для всех (НЕБЕЗОПАСНО)"
                echo "  $0 --port 8080 --whitelist 1.2.3.4     # Только для указанного IP"
                echo "  $0 --port 8080 --whitelist 1.2.3.4,5.6.7.8 # Несколько IP"
                exit 0
                ;;
            *)
                echo "[!] Неизвестный параметр: $1"
                echo "Используйте --help для справки"
                exit 1
                ;;
        esac
    done
    
    # Get network information
    local local_ip=$(get_local_ip)
    local external_ip=$(get_external_ip)
    
    echo ""
    echo "[+] Сетевая информация:"
    echo "    Локальный IP: $local_ip"
    echo "    Внешний IP: $external_ip"
    echo "    Порт: $port"
    echo ""
    
    # Setup firewall
    setup_firewall $port "$ip_whitelist"
    
    # Show current firewall status
    echo ""
    echo "[+] Текущий статус firewall:"
    ufw status numbered
    
    # Test external access
    test_external_access $port $external_ip
    
    # Show security tips
    show_security_tips
    
    echo ""
    echo "🎯 ДЛЯ ЗАПУСКА СЕРВЕРА:"
    echo "======================"
    echo ""
    echo "1. Запустите C2 сервер:"
    if [ -n "$ip_whitelist" ]; then
        echo "   python3 server/external_server.py --port $port --whitelist $ip_whitelist"
    else
        echo "   python3 server/external_server.py --port $port"
    fi
    echo ""
    echo "2. Доступ к веб-интерфейсу:"
    echo "   Локально: http://localhost:$port/dashboard"
    echo "   В сети: http://$local_ip:$port/dashboard"
    if [ "$external_ip" != "Не определен" ]; then
        echo "   Извне: http://$external_ip:$port/dashboard"
    fi
    echo ""
    echo "3. Администратор: admin / shadowc2"
    echo ""
    echo "✅ Настройка внешнего доступа завершена!"
}

# Run main function
main "$@"