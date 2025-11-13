#!/usr/bin/env python3
"""
Shadow C2 Quick Start - Complete System Launch
Automated deployment and testing script
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
from pathlib import Path
import signal

class QuickStart:
    def __init__(self):
        self.output_dir = Path("/mnt/okcomputer/output")
        self.server_process = None
        self.beacon_process = None
        self.running = True
        
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n[!] Shutting down Shadow C2 system...")
        self.cleanup()
        sys.exit(0)
        
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        SHADOW C2 QUICK START                                ║
║                    Complete System Deployment                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def check_system(self):
        """Check system readiness"""
        print("[+] Checking system readiness...")
        
        # Check Python
        if not (sys.version_info.major >= 3 and sys.version_info.minor >= 7):
            print("[!] Python 3.7+ required")
            return False
            
        # Check files
        required_files = [
            "server/simple_server.py",
            "advanced_stager",
            "start_c2.sh"
        ]
        
        for file in required_files:
            if not (self.output_dir / file).exists():
                print(f"[!] Required file not found: {file}")
                return False
                
        print("[✓] System ready for deployment")
        return True
        
    def start_server(self):
        """Start C2 server"""
        print("[+] Starting C2 server...")
        
        try:
            self.server_process = subprocess.Popen([
                sys.executable, "server/simple_server.py",
                "--port", "8080"
            ], cwd=self.output_dir)
            
            # Wait for server to start
            time.sleep(3)
            
            if self.server_process.poll() is None:
                print(f"[✓] C2 server started (PID: {self.server_process.pid})")
                return True
            else:
                print("[!] Server failed to start")
                return False
                
        except Exception as e:
            print(f"[!] Error starting server: {e}")
            return False
            
    def start_beacon(self):
        """Start beacon in background"""
        print("[+] Starting beacon...")
        
        try:
            # Make beacon executable
            beacon_path = self.output_dir / "advanced_stager"
            beacon_path.chmod(0o755)
            
            self.beacon_process = subprocess.Popen([
                "./advanced_stager"
            ], cwd=self.output_dir)
            
            print(f"[✓] Beacon started (PID: {self.beacon_process.pid})")
            return True
            
        except Exception as e:
            print(f"[!] Error starting beacon: {e}")
            return False
            
    def open_dashboard(self):
        """Open web dashboard"""
        print("[+] Opening dashboard...")
        time.sleep(2)  # Wait for server to be ready
        webbrowser.open('http://localhost:8080/dashboard')
        print("[✓] Dashboard opened in browser")
        
    def monitor_system(self):
        """Monitor system status"""
        print("\\n" + "="*60)
        print("SYSTEM MONITORING")
        print("="*60)
        
        try:
            while self.running:
                # Check server status
                if self.server_process and self.server_process.poll() is not None:
                    print("[!] Server process died")
                    break
                    
                # Check beacon status  
                if self.beacon_process and self.beacon_process.poll() is not None:
                    print("[!] Beacon process died")
                    
                print(f"[+] System running - {time.strftime('%H:%M:%S')}", end='\\r')
                time.sleep(10)
                
        except KeyboardInterrupt:
            pass
            
    def cleanup(self):
        """Clean up processes"""
        print("\\n[+] Cleaning up...")
        
        if self.server_process:
            print("[+] Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
            
        if self.beacon_process:
            print("[+] Stopping beacon...")
            self.beacon_process.terminate()
            self.beacon_process.wait()
            
        print("[✓] Cleanup completed")
        
    def run(self):
        """Run complete quick start"""
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.print_banner()
        
        # Check system
        if not self.check_system():
            return False
            
        # Start components
        if not self.start_server():
            return False
            
        if not self.start_beacon():
            print("[!] Warning: Beacon failed to start")
            
        # Open dashboard
        self.open_dashboard()
        
        # Monitor system
        print("\\n" + "=" * 60)
        print("SHADOW C2 SYSTEM DEPLOYED SUCCESSFULLY!")
        print("=" * 60)
        print("")
        print("🎯 What you can do now:")
        print("   • View beacons in the dashboard")
        print("   • Send commands to connected beacons")
        print("   • Monitor system activity")
        print("   • Access all C2 features")
        print("")
        print("🌐 Dashboard: http://localhost:8080/dashboard")
        print("📡 Beacons: http://localhost:8080/beacons")
        print("")
        print("⚡ Press Ctrl+C to shut down the system")
        print("")
        
        # Start monitoring
        self.monitor_system()
        
        return True

def main():
    """Main function"""
    quick_start = QuickStart()
    
    try:
        success = quick_start.run()
        
        if success:
            print("\\n" + "="*60)
            print("✅ SHADOW C2 DEPLOYMENT COMPLETED SUCCESSFULLY!")
            print("="*60)
        else:
            print("\\n" + "="*60) 
            print("❌ DEPLOYMENT FAILED")
            print("="*60)
            
    except Exception as e:
        print(f"\\n[!] Unexpected error: {e}")
        quick_start.cleanup()
        
if __name__ == '__main__':
    main()
