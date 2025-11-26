import requests
import concurrent.futures
import time
from colorama import Fore, Style, init
import sys

# Initialize colorama for cross-platform color support
init(autoreset=True)

ASCII_ART = f"""
{Fore.CYAN}
   ██████╗████████╗██████╗ ██╗██╗  ██╗ █████╗ 
  ██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔══██╗
  ╚█████╗    ██║   ██████╔╝██║█████╔╝ ███████║
   ╚═══██╗   ██║   ██╔══██╗██║██╔═██╗ ██╔══██║
  ██████╔╝   ██║   ██║  ██║██║██║  ██╗██║  ██║
  ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
{Fore.MAGENTA}  ╔═══════════════════════════════════════════╗
  ║   Proxy Checker & Grabber Tool v1.0      ║
  ║   Fast • Reliable • Powerful              ║
  ╚═══════════════════════════════════════════╝
{Style.RESET_ALL}
"""

class ProxyChecker:
    def __init__(self):
        self.working_proxies = []
        self.dead_proxies = []
        self.test_url = "http://httpbin.org/ip"
        self.timeout = 5
        self.proxy_type = "http"
    
    def print_banner(self):
        """Display the ASCII art banner"""
        print(ASCII_ART)
    
    def grab_proxies_from_api(self):
        """Grab free proxies from public APIs"""
        print(f"\n{Fore.YELLOW}[*] Grabbing {self.proxy_type} proxies from public sources...")
        proxies = []
        
        sources = [
            # Primary API sources with protocol support
            f"https://api.proxyscrape.com/v2/?request=get&protocol={self.proxy_type}&timeout=5000&country=all&ssl=all&anonymity=all",
            f"https://www.proxy-list.download/api/v1/get?type={self.proxy_type.upper()}",
        
            # Github raw lists (frequently updated)
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        
            # Free proxy aggregator
            "https://www.freeproxylists.net/",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        
            # Updated lists
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
        
            # Additional sources
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://raw.githubusercontent.com/hendrikbakker/PublicProxyList/master/proxies.csv",
        ]

        for source in sources:
            try:
                print(f"{Fore.CYAN}[+] Fetching from: {source[:60]}...")
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    proxy_list = response.text.strip().split('\n')
                    proxies.extend([p.strip() for p in proxy_list if p.strip()])
                    print(f"{Fore.GREEN}[✓] Got {len(proxy_list)} proxies")
            except Exception as e:
                print(f"{Fore.RED}[✗] Failed to fetch from source: {str(e)[:40]}")
        
        proxies = list(set(proxies))
        print(f"\n{Fore.GREEN}[✓] Total unique proxies grabbed: {len(proxies)}")
        return proxies
    
    def check_proxy(self, proxy):
        """Check if a single proxy is working"""
        scheme = "http"
        if self.proxy_type in ("socks4", "socks5"):
            scheme = self.proxy_type
        
        proxy_dict = {
            "http": f"{scheme}://{proxy}",
            "https": f"{scheme}://{proxy}"
        }
        
        if self.proxy_type.startswith("socks"):
            try:
                import socks
            except Exception:
                print(f"{Fore.YELLOW}[!] Using socks proxies requires PySocks (pip install requests[socks])")
        
        try:
            start_time = time.time()
            response = requests.get(
                self.test_url,
                proxies=proxy_dict,
                timeout=self.timeout
            )
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if response.status_code == 200:
                return {
                    'proxy': proxy,
                    'status': 'working',
                    'response_time': response_time
                }
        except:
            pass
        
        return {
            'proxy': proxy,
            'status': 'dead',
            'response_time': None
        }
    
    def check_proxies(self, proxies, max_workers=50):
        """Check multiple proxies concurrently"""
        print(f"\n{Fore.YELLOW}[*] Starting proxy check with {max_workers} threads...")
        print(f"{Fore.CYAN}[*] Testing {len(proxies)} proxies...\n")
        
        total = len(proxies)
        checked = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.check_proxy, proxy): proxy for proxy in proxies}
            
            for future in concurrent.futures.as_completed(futures):
                checked += 1
                result = future.result()
                
                if result['status'] == 'working':
                    self.working_proxies.append(result)
                    print(f"{Fore.GREEN}[✓] {result['proxy']} - {result['response_time']}ms - [{checked}/{total}]")
                else:
                    self.dead_proxies.append(result['proxy'])
                    print(f"{Fore.RED}[✗] {result['proxy']} - DEAD - [{checked}/{total}]")
    
    def save_working_proxies(self, filename="working_proxies.txt"):
        """Save working proxies to file"""
        if not self.working_proxies:
            print(f"\n{Fore.YELLOW}[!] No working proxies to save")
            return
        
        try:
            with open(filename, 'w') as f:
                for proxy_info in sorted(self.working_proxies, key=lambda x: x['response_time']):
                    f.write(f"{proxy_info['proxy']}\n")
            
            print(f"\n{Fore.GREEN}[✓] Saved {len(self.working_proxies)} working proxies to {filename}")
        except Exception as e:
            print(f"\n{Fore.RED}[✗] Failed to save proxies: {str(e)}")
    
    def print_statistics(self):
        """Print checking statistics"""
        total = len(self.working_proxies) + len(self.dead_proxies)
        
        print(f"\n{Fore.MAGENTA}{'='*50}")
        print(f"{Fore.CYAN}STATISTICS")
        print(f"{Fore.MAGENTA}{'='*50}")
        print(f"{Fore.WHITE}Total Checked:    {Fore.YELLOW}{total}")
        print(f"{Fore.WHITE}Working Proxies:  {Fore.GREEN}{len(self.working_proxies)}")
        print(f"{Fore.WHITE}Dead Proxies:     {Fore.RED}{len(self.dead_proxies)}")
        
        if total > 0:
            success_rate = (len(self.working_proxies) / total) * 100
            print(f"{Fore.WHITE}Success Rate:     {Fore.CYAN}{success_rate:.2f}%")
        
        if self.working_proxies:
            avg_time = sum(p['response_time'] for p in self.working_proxies) / len(self.working_proxies)
            print(f"{Fore.WHITE}Avg Response:     {Fore.GREEN}{avg_time:.2f}ms")
        
        print(f"{Fore.MAGENTA}{'='*50}\n")
    
    def load_proxies_from_file(self, filename):
        """Load proxies from a text file"""
        try:
            with open(filename, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            print(f"{Fore.GREEN}[✓] Loaded {len(proxies)} proxies from {filename}")
            return proxies
        except FileNotFoundError:
            print(f"{Fore.RED}[✗] File not found: {filename}")
            return []
        except Exception as e:
            print(f"{Fore.RED}[✗] Error loading file: {str(e)}")
            return []
    
    def choose_proxy_type(self):
        """Prompt the user to select a proxy type"""
        print(f"\n{Fore.CYAN}Choose proxy type:")
        print("1. http")
        print("2. https")
        print("3. socks4")
        print("4. socks5")
        choice = input(f"{Fore.GREEN}[>] Select type (1-4) or enter name: {Style.RESET_ALL}").strip().lower()
        mapping = {"1": "http", "2": "https", "3": "socks4", "4": "socks5"}
        selected = mapping.get(choice, choice or self.proxy_type)
        if selected not in ("http", "https", "socks4", "socks5"):
            print(f"{Fore.RED}[✗] Invalid type '{selected}', defaulting to {self.proxy_type}")
            return self.proxy_type
        self.proxy_type = selected
        print(f"{Fore.GREEN}[✓] Proxy type set to: {self.proxy_type}")
        return self.proxy_type


def main_menu():
    """Display main menu"""
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.YELLOW}MAIN MENU")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.WHITE}1. Grab proxies from public sources")
    print(f"{Fore.WHITE}2. Load proxies from file")
    print(f"{Fore.WHITE}3. Enter proxies manually")
    print(f"{Fore.WHITE}4. Exit")
    print(f"{Fore.CYAN}{'='*50}")

def main():
    checker = ProxyChecker()
    checker.print_banner()
    
    while True:
        main_menu()
        choice = input(f"\n{Fore.GREEN}[>] Select option: {Style.RESET_ALL}")
        
        if choice == '1':
            checker.choose_proxy_type()
            proxies = checker.grab_proxies_from_api()
            if proxies:
                checker.check_proxies(proxies)
                checker.print_statistics()
                checker.save_working_proxies()
            
        elif choice == '2':
            checker.choose_proxy_type()
            filename = input(f"{Fore.GREEN}[>] Enter filename: {Style.RESET_ALL}")
            proxies = checker.load_proxies_from_file(filename)
            if proxies:
                checker.check_proxies(proxies)
                checker.print_statistics()
                checker.save_working_proxies()
        
        elif choice == '3':
            checker.choose_proxy_type()
            print(f"{Fore.YELLOW}[*] Enter proxies (IP:PORT format, one per line)")
            print(f"{Fore.YELLOW}[*] Press Enter twice when done")
            proxies = []
            while True:
                proxy = input(f"{Fore.GREEN}[>] {Style.RESET_ALL}")
                if not proxy:
                    break
                proxies.append(proxy.strip())
            
            if proxies:
                checker.check_proxies(proxies)
                checker.print_statistics()
                checker.save_working_proxies()
        
        elif choice == '4':
            print(f"\n{Fore.CYAN}[*] Thanks for using Strika Proxy Checker!")
            print(f"{Fore.MAGENTA}[*] Stay sharp! 🎯\n")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}[✗] Invalid option!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Interrupted by user")
        print(f"{Fore.CYAN}[*] Goodbye! 👋\n")
        sys.exit(0)