#!/usr/bin/env python3
"""
Security Hardening Script for Shadow C2 Toolkit
Implements advanced security measures and anti-forensics
"""

import os
import sys
import hashlib
import secrets
import subprocess
import shutil
import json
import time
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SecurityHardening:
    """Advanced security hardening for C2 operations"""
    
    def __init__(self, config_dir="/mnt/okcomputer/output/config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.security_config = self.config_dir / "security.json"
        self.encryption_key = None
        self.load_or_generate_config()
    
    def load_or_generate_config(self):
        """Load existing security config or generate new one"""
        if self.security_config.exists():
            with open(self.security_config, 'r') as f:
                config = json.load(f)
                self.encryption_key = base64.urlsafe_b64decode(config['encryption_key'])
        else:
            self.generate_security_config()
    
    def generate_security_config(self):
        """Generate comprehensive security configuration"""
        print("[+] Generating security configuration...")
        
        # Generate master encryption key
        password = secrets.token_bytes(32)
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.encryption_key = key
        
        config = {
            "encryption_key": key.decode(),
            "salt": base64.b64encode(salt).decode(),
            "security_policies": {
                "max_failed_logins": 5,
                "session_timeout": 3600,
                "password_complexity": {
                    "min_length": 12,
                    "require_uppercase": True,
                    "require_lowercase": True,
                    "require_numbers": True,
                    "require_symbols": True
                },
                "communication_security": {
                    "enable_tls": True,
                    "certificate_validation": True,
                    "perfect_forward_secrecy": True,
                    "anti_replay_protection": True
                },
                "data_protection": {
                    "encrypt_at_rest": True,
                    "encrypt_in_transit": True,
                    "memory_protection": True,
                    "secure_deletion": True
                }
            },
            "anti_forensics": {
                "memory_encryption": True,
                "process_masquerading": True,
                "anti_debugging": True,
                "sandbox_detection": True,
                "vm_detection": True,
                "self_destruct": True,
                "log_sanitization": True
            },
            "operational_security": {
                "domain_fronting": True,
                "traffic_morphing": True,
                "timing_jitter": True,
                "connection_proxy": True,
                "failover_endpoints": True
            }
        }
        
        # Encrypt and save config
        encrypted_config = self.encrypt_data(json.dumps(config))
        with open(self.security_config, 'wb') as f:
            f.write(encrypted_config)
        
        print(f"[+] Security config saved to {self.security_config}")
        return config
    
    def encrypt_data(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        f = Fernet(self.encryption_key)
        return f.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data"""
        f = Fernet(self.encryption_key)
        return f.decrypt(encrypted_data).decode()
    
    def generate_tls_certificates(self):
        """Generate self-signed TLS certificates"""
        print("[+] Generating TLS certificates...")
        
        cert_dir = self.config_dir / "certs"
        cert_dir.mkdir(exist_ok=True)
        
        # Generate private key
        key_file = cert_dir / "server.key"
        cert_file = cert_dir / "server.crt"
        
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:4096",
            "-keyout", str(key_file), "-out", str(cert_file),
            "-days", "365", "-nodes", "-subj",
            "/C=US/ST=State/L=City/O=Organization/CN=shadow-c2.local"
        ], check=True, capture_output=True)
        
        # Set restrictive permissions
        os.chmod(key_file, 0o600)
        os.chmod(cert_file, 0o644)
        
        print(f"[+] TLS certificates generated in {cert_dir}")
        return cert_file, key_file
    
    def setup_secure_directories(self):
        """Setup secure directory structure"""
        print("[+] Setting up secure directories...")
        
        secure_dirs = [
            "logs",
            "uploads",
            "downloads", 
            "backups",
            "temp",
            "audit"
        ]
        
        for dir_name in secure_dirs:
            dir_path = self.config_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            
            # Set restrictive permissions
            os.chmod(dir_path, 0o700)
            
            # Create .gitignore to prevent accidental commits
            gitignore = dir_path / ".gitignore"
            gitignore.write_text("*\n!.gitignore\n")
        
        print("[+] Secure directories configured")
    
    def generate_secure_passwords(self):
        """Generate secure passwords for various services"""
        print("[+] Generating secure passwords...")
        
        passwords = {
            "database": secrets.token_urlsafe(32),
            "api_key": secrets.token_urlsafe(32),
            "jwt_secret": secrets.token_urlsafe(32),
            "admin_password": secrets.token_urlsafe(16),
            "encryption_password": secrets.token_urlsafe(32)
        }
        
        passwords_file = self.config_dir / "passwords.enc"
        encrypted_passwords = self.encrypt_data(json.dumps(passwords))
        
        with open(passwords_file, 'wb') as f:
            f.write(encrypted_passwords)
        
        os.chmod(passwords_file, 0o600)
        
        print(f"[+] Secure passwords generated and saved")
        return passwords
    
    def create_hardening_script(self):
        """Create system hardening script"""
        print("[+] Creating system hardening script...")
        
        hardening_script = """#!/bin/bash
# Shadow C2 System Hardening Script

set -e

echo "[+] Starting system hardening..."

# Disable core dumps
echo "* soft core 0" >> /etc/security/limits.conf
echo "* hard core 0" >> /etc/security/limits.conf

# Enable ASLR
echo 2 > /proc/sys/kernel/randomize_va_space

# Disable IP forwarding
echo 0 > /proc/sys/net/ipv4/ip_forward

# Enable SYN cookies
echo 1 > /proc/sys/net/ipv4/tcp_syncookies

# Disable ICMP redirects
echo 0 > /proc/sys/net/ipv4/conf/all/accept_redirects
echo 0 > /proc/sys/net/ipv4/conf/default/accept_redirects

# Set strict file permissions
find /mnt/okcomputer/output -type f -name "*.py" -exec chmod 600 {} \;
find /mnt/okcomputer/output -type f -name "*.cpp" -exec chmod 600 {} \;
find /mnt/okcomputer/output -type f -name "*.h" -exec chmod 600 {} \;

# Secure log files
chmod 600 /mnt/okcomputer/output/logs/* 2>/dev/null || true
chmod 600 /mnt/okcomputer/output/audit/* 2>/dev/null || true

# Set secure umask
umask 077

echo "[+] System hardening completed"
"""
        
        script_path = self.config_dir / "hardening.sh"
        script_path.write_text(hardening_script)
        script_path.chmod(0o755)
        
        print(f"[+] Hardening script created: {script_path}")
    
    def create_firewall_rules(self):
        """Create firewall rules for enhanced security"""
        print("[+] Creating firewall rules...")
        
        firewall_rules = """#!/bin/bash
# Shadow C2 Firewall Rules

set -e

echo "[+] Configuring firewall..."

# Reset rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow C2 server port (adjust as needed)
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 8080 -j ACCEPT

# Allow HTTPS for beacon callbacks
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --sport 443 -j ACCEPT

# Rate limiting
iptables -A INPUT -p tcp --dport 8080 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "C2_DROPPED: " --log-level 4

# Save rules
iptables-save > /etc/iptables/rules.v4 2>/dev/null || true

echo "[+] Firewall rules configured"
"""
        
        firewall_script = self.config_dir / "firewall.sh"
        firewall_script.write_text(firewall_rules)
        firewall_script.chmod(0o755)
        
        print(f"[+] Firewall rules created: {firewall_script}")
    
    def create_monitoring_script(self):
        """Create security monitoring script"""
        print("[+] Creating monitoring script...")
        
        monitoring_script = """#!/usr/bin/env python3
# Shadow C2 Security Monitoring

import os
import time
import psutil
import logging
from datetime import datetime

class SecurityMonitor:
    def __init__(self):
        self.setup_logging()
        self.suspicious_patterns = [
            'gdb', 'strace', 'ltrace', 'tcpdump', 'wireshark',
            'netstat', 'lsof', 'ps', 'top', 'htop'
        ]
    
    def setup_logging(self):
        logging.basicConfig(
            filename='/mnt/okcomputer/output/logs/security.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def monitor_processes(self):
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                for pattern in self.suspicious_patterns:
                    if pattern in cmdline.lower():
                        self.logger.warning(f"Suspicious process detected: {cmdline}")
                        self.alert_admin(f"Security Alert: Analysis tool detected - {cmdline}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    
    def monitor_network_connections(self):
        connections = psutil.net_connections()
        for conn in connections:
            if conn.status == 'LISTEN' and conn.laddr.port not in [8080, 22, 80, 443]:
                self.logger.info(f"Unexpected listening port: {conn.laddr.port}")
    
    def monitor_file_changes(self):
        critical_files = [
            '/mnt/okcomputer/output/server/shadow_server.py',
            '/mnt/okcomputer/output/advanced_stager',
            '/mnt/okcomputer/output/config/security.json'
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                self.logger.info(f"File check: {file_path} - {stat.st_mtime}")
    
    def alert_admin(self, message):
        # Simple alert mechanism - could be enhanced
        with open('/mnt/okcomputer/output/logs/alerts.log', 'a') as f:
            f.write(f"{datetime.now()}: {message}\\n")
    
    def run(self):
        self.logger.info("Security monitoring started")
        while True:
            try:
                self.monitor_processes()
                self.monitor_network_connections()
                self.monitor_file_changes()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")

if __name__ == "__main__":
    monitor = SecurityMonitor()
    monitor.run()
"""
        
        monitor_path = self.config_dir / "monitor.py"
        monitor_path.write_text(monitoring_script)
        monitor_path.chmod(0o755)
        
        print(f"[+] Monitoring script created: {monitor_path}")
    
    def create_incident_response_plan(self):
        """Create incident response plan"""
        print("[+] Creating incident response plan...")
        
        incident_plan = """# Shadow C2 Incident Response Plan

## Immediate Response (0-5 minutes)
1. **Isolate the system**
   - Disconnect from network if compromise suspected
   - Preserve current state for forensics

2. **Assess the threat**
   - Check security logs for anomalies
   - Identify affected systems
   - Determine scope of compromise

3. **Activate response team**
   - Notify security personnel
   - Document all actions taken
   - Preserve evidence

## Short-term Response (5-30 minutes)
1. **Containment**
   - Stop C2 server if necessary
   - Revoke compromised credentials
   - Block suspicious IP addresses

2. **Evidence collection**
   - Save log files
   - Capture network traffic
   - Document timeline

3. **Communication**
   - Notify stakeholders
   - Prepare external communications
   - Coordinate with legal if needed

## Long-term Response (30+ minutes)
1. **Eradication**
   - Remove malicious artifacts
   - Patch vulnerabilities
   - Update security measures

2. **Recovery**
   - Restore from clean backups
   - Rebuild compromised systems
   - Verify integrity

3. **Lessons learned**
   - Conduct post-incident review
   - Update security policies
   - Improve detection capabilities

## Emergency Contacts
- Security Team: security@company.com
- System Admin: admin@company.com
- Legal: legal@company.com

## Critical Files Backup
- Configuration: /mnt/okcomputer/output/config/
- Logs: /mnt/okcomputer/output/logs/
- Certificates: /mnt/okcomputer/output/config/certs/
"""
        
        incident_file = self.config_dir / "incident_response.md"
        incident_file.write_text(incident_plan)
        
        print(f"[+] Incident response plan created: {incident_file}")
    
    def apply_all_hardening(self):
        """Apply all security hardening measures"""
        print("=" * 60)
        print("SHADOW C2 SECURITY HARDENING")
        print("=" * 60)
        
        try:
            # Generate all security components
            self.setup_secure_directories()
            self.generate_tls_certificates()
            self.generate_secure_passwords()
            self.create_hardening_script()
            self.create_firewall_rules()
            self.create_monitoring_script()
            self.create_incident_response_plan()
            
            print("\n" + "=" * 60)
            print("SECURITY HARDENING COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print("\nNext steps:")
            print("1. Review security configuration in config/security.json")
            print("2. Run system hardening: sudo ./config/hardening.sh")
            print("3. Configure firewall: sudo ./config/firewall.sh")
            print("4. Start monitoring: python3 ./config/monitor.py &")
            print("5. Update default credentials immediately")
            print("\nSecurity is now enhanced with:")
            print("- Encrypted configuration storage")
            print("- TLS certificate generation")
            print("- Secure password management")
            print("- System hardening scripts")
            print("- Firewall rules")
            print("- Security monitoring")
            print("- Incident response plan")
            
        except Exception as e:
            print(f"[!] Error during hardening: {e}")
            sys.exit(1)

def main():
    """Main security hardening function"""
    if os.geteuid() != 0:
        print("[!] Warning: Some hardening features require root privileges")
        print("    Run with sudo for full hardening capabilities")
    
    hardening = SecurityHardening()
    hardening.apply_all_hardening()

if __name__ == "__main__":
    main()