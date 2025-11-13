#!/usr/bin/env python3
"""
Test VPN access to C2 admin interface
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path

def test_vpn_access():
    """Test if we can access admin interface through VPN"""
    
    print("[+] Testing VPN access to C2 admin interface")
    print("")
    
    # Check if VPN interface exists
    try:
        result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
        if '10.8.0.1' in result.stdout:
            print("[✓] VPN interface 10.8.0.1 found")
        else:
            print("[!] VPN interface 10.8.0.1 NOT found")
            return False
    except:
        print("[!] Cannot check VPN interface")
        return False
    
    # Start a simple test server
    print("[+] Starting test server on 10.8.0.1:8080...")
    try:
        server_process = subprocess.Popen([
            sys.executable, '-m', 'http.server', '8080', '--bind', '10.8.0.1'
        ], cwd='/mnt/okcomputer/output', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(2)
        
        # Test connection
        print("[+] Testing connection to 10.8.0.1:8080...")
        try:
            response = requests.get('http://10.8.0.1:8080', timeout=5)
            print(f"[✓] Connection successful! Status: {response.status_code}")
            print("[✓] VPN access is working!")
            server_process.terminate()
            return True
        except requests.exceptions.ConnectionError:
            print("[!] Connection failed - VPN may not be working")
        except requests.exceptions.Timeout:
            print("[!] Connection timeout")
        except Exception as e:
            print(f"[!] Connection error: {e}")
        
        server_process.terminate()
        
    except Exception as e:
        print(f"[!] Failed to start test server: {e}")
    
    return False

if __name__ == '__main__':
    test_vpn_access()