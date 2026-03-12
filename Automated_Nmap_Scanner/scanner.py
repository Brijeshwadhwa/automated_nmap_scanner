"""
scanner.py - Nmap Scanning Logic
This module handles all Nmap scanning operations using python-nmap library.
"""

import nmap
import socket
from datetime import datetime

class NmapScanner:
    """Handles Nmap scanning operations"""
    
    def __init__(self):
        """Initialize the Nmap scanner"""
        self.nm = nmap.PortScanner()
        
    def check_nmap_installed(self):
        """
        Check if Nmap is installed and accessible
        
        Returns:
            bool: True if Nmap is installed, False otherwise
        """
        try:
            # Try to get Nmap version
            self.nm.nmap_version()
            return True
        except Exception:
            return False
    
    def scan_target(self, ip_address, port_range):
        """
        Perform an Nmap scan on the target IP address
        
        Args:
            ip_address: Target IP address to scan
            port_range: Port range to scan (e.g., "1-1000")
        
        Returns:
            dict: Dictionary containing scan results
        """
        try:
            # Validate IP address
            socket.inet_aton(ip_address)
            
            # Record scan start time
            start_time = datetime.now()
            
            # Perform the scan
            # Arguments: -sS (SYN scan), -sV (version detection)
            self.nm.scan(hosts=ip_address, ports=port_range, arguments='-sS -sV')
            
            # Calculate scan time
            scan_time = datetime.now() - start_time
            time_str = str(scan_time).split('.')[0]  # Remove microseconds
            
            # Prepare results
            results = {
                'target': ip_address,
                'scan_time': time_str,
                'ports': []
            }
            
            # Process scan results
            if ip_address in self.nm.all_hosts():
                host = self.nm[ip_address]
                
                # Check if host is up
                if host.state() == 'up':
                    # Get TCP ports
                    if 'tcp' in host:
                        for port, port_info in host['tcp'].items():
                            port_result = {
                                'port': port,
                                'state': port_info['state'],
                                'service': port_info.get('name', 'unknown'),
                                'product': port_info.get('product', ''),
                                'version': port_info.get('version', ''),
                                'extrainfo': port_info.get('extrainfo', '')
                            }
                            
                            # Add version info if available
                            if port_result['product']:
                                port_result['service'] += f" ({port_result['product']}"
                                if port_result['version']:
                                    port_result['service'] += f" {port_result['version']}"
                                port_result['service'] += ")"
                            
                            results['ports'].append(port_result)
            
            # Sort ports numerically
            results['ports'].sort(key=lambda x: x['port'])
            
            return results
            
        except socket.error:
            return {'error': f"Invalid IP address: {ip_address}"}
        except nmap.PortScannerError as e:
            return {'error': f"Nmap scanner error: {str(e)}"}
        except Exception as e:
            return {'error': f"Unexpected error: {str(e)}"}
    
    def scan_specific_ports(self, ip_address, ports):
        """
        Scan specific ports on a target
        
        Args:
            ip_address: Target IP address
            ports: List of specific ports to scan (e.g., [22, 80, 443])
        
        Returns:
            dict: Scan results
        """
        port_range = ','.join(map(str, ports))
        return self.scan_target(ip_address, port_range)
    
    def quick_scan(self, ip_address):
        """
        Perform a quick scan of common ports
        
        Args:
            ip_address: Target IP address
        
        Returns:
            dict: Scan results
        """
        # Common ports: HTTP(80), HTTPS(443), SSH(22), FTP(21), SMTP(25), DNS(53)
        common_ports = "21,22,25,53,80,443,3306,5432,8080"
        return self.scan_target(ip_address, common_ports)
    
    def get_open_ports(self, ip_address, port_range):
        """
        Get only open ports from a scan
        
        Args:
            ip_address: Target IP address
            port_range: Port range to scan
        
        Returns:
            list: List of dictionaries containing only open ports
        """
        results = self.scan_target(ip_address, port_range)
        
        if 'error' in results:
            return results
        
        # Filter only open ports
        open_ports = [port for port in results['ports'] 
                     if port['state'].lower() == 'open']
        
        return {
            'target': results['target'],
            'scan_time': results['scan_time'],
            'ports': open_ports
        }