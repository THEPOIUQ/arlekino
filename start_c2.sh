#!/bin/bash
# Shadow C2 Toolkit - Simple Startup Script
# Handles network dependency issues and provides fallback options

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                        SHADOW C2 TOOLKIT STARTUP                            ║"
echo "║                    Network-Friendly Version                                 ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"

echo ""
echo "[+] Checking system requirements..."

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "[!] Python not found. Please install Python 3.7+"
    exit 1
fi

echo "[✓] Python found: $PYTHON_CMD"

# Check if we're in the right directory
if [ ! -f "server/simple_server.py" ]; then
    echo "[!] Not in correct directory. Please cd to /mnt/okcomputer/output"
    exit 1
fi

echo "[✓] Correct directory confirmed"

# Function to check network connectivity
check_network() {
    if ping -c 1 8.8.8.8 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to install dependencies if network is available
install_dependencies() {
    if check_network; then
        echo "[+] Network available - checking for optional dependencies..."
        
        # Try to install aiohttp_jinja2 for enhanced features
        if $PYTHON_CMD -m pip install aiohttp_jinja2 &> /dev/null; then
            echo "[✓] Enhanced dependencies installed successfully"
            return 0
        else
            echo "[!] Could not install enhanced dependencies, using simple server"
            return 1
        fi
    else
        echo "[!] No network connectivity - using simple server"
        return 1
    fi
}

# Function to start the appropriate server
start_server() {
    echo ""
    echo "[+] Starting C2 Server..."
    
    # Try to install dependencies first
    if install_dependencies; then
        # Enhanced server available
        echo "[+] Starting enhanced server with full features..."
        if [ -f "server/enhanced_server.py" ]; then
            $PYTHON_CMD server/enhanced_server.py --port 8080
        else
            echo "[!] Enhanced server not found, falling back to simple server"
            $PYTHON_CMD server/simple_server.py --port 8080
        fi
    else
        # Use simple server
        echo "[+] Starting simple server (no external dependencies)..."
        $PYTHON_CMD server/simple_server.py --port 8080
    fi
}

# Function to show menu
show_menu() {
    echo ""
    echo "Choose an option:"
    echo "1. Start C2 Server"
    echo "2. Run Security Hardening"
    echo "3. Run Full Demo"
    echo "4. Start Beacon"
    echo "5. Show Documentation"
    echo "6. Exit"
    echo ""
}

# Main menu loop
while true; do
    show_menu
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            start_server
            ;;
        2)
            echo ""
            echo "[+] Running security hardening..."
            if $PYTHON_CMD security_hardening.py; then
                echo "[✓] Security hardening completed"
            else
                echo "[!] Security hardening failed"
            fi
            ;;
        3)
            echo ""
            echo "[+] Running full demonstration..."
            $PYTHON_CMD demo_usage.py
            ;;
        4)
            echo ""
            echo "[+] Starting beacon..."
            if [ -f "advanced_stager" ]; then
                chmod +x advanced_stager
                ./advanced_stager
            else
                echo "[!] Beacon binary not found. Please compile first."
            fi
            ;;
        5)
            echo ""
            echo "Available documentation:"
            echo "- DEPLOYMENT_GUIDE.md: Complete deployment guide"
            echo "- NEXT_STEPS.md: What to do after compilation"
            echo "- README.md: General information"
            echo ""
            read -p "Press Enter to continue..."
            ;;
        6)
            echo ""
            echo "[+] Exiting Shadow C2 Toolkit"
            exit 0
            ;;
        *)
            echo "[!] Invalid choice. Please enter 1-6"
            ;;
    esac
done