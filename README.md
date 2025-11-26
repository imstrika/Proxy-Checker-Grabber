# Strika Proxy Checker & Grabber

A fast, reliable, and powerful proxy checker and grabber tool written in Python. Automatically fetches proxies from multiple sources, validates them, and saves working proxies to a file.

## Features

✨ **Multi-Source Proxy Grabbing**
- Pulls from 20+ actively maintained proxy sources
- Supports HTTP, HTTPS, SOCKS4, and SOCKS5 proxies
- Automatic deduplication

🚀 **High-Performance Validation**
- Concurrent proxy checking (50 threads by default)
- Fast response time detection
- Detailed statistics and success rates

📊 **User-Friendly Interface**
- Clean, colorized CLI output
- Multiple input methods (grab, file, manual)
- Real-time progress tracking
- Sorted results by response time

💾 **Easy Export**
- Save working proxies to text file
- CSV support ready
- Organized by performance

## Installation

### Requirements
- Python 3.7+
- Windows/Linux/macOS

### Setup

1. Clone the repository:
```bash
git clone https://github.com/imstrika/strika-proxy-checker.git
cd strika-proxy-checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

For SOCKS proxy support, install PySocks:
```bash
pip install requests[socks]
```

## Usage

Run the tool:
```bash
python strikaproxytool.py
```

### Menu Options

**1. Grab proxies from public sources**
- Select proxy type (HTTP, HTTPS, SOCKS4, SOCKS5)
- Fetches from 20+ sources automatically
- Validates all proxies concurrently
- Saves working ones to `working_proxies.txt`

**2. Load proxies from file**
- Load a list of proxies from a text file
- One proxy per line (IP:PORT format)
- Validates against selected type
- Saves results

**3. Enter proxies manually**
- Input proxies one by one
- Format: `IP:PORT`
- Press Enter twice when done
- Validates and saves results

**4. Exit**
- Quit the application

## Example Output

```
[*] Grabbing http proxies from public sources...
[+] Fetching from: https://api.proxyscrape.com/v2/...
[✓] Got 150 proxies
[✓] Got 200 proxies

[*] Starting proxy check with 50 threads...
[✓] 192.168.1.1:8080 - 45.23ms - [1/350]
[✗] 10.0.0.1:3128 - DEAD - [2/350]

==================================================
STATISTICS
==================================================
Total Checked:    350
Working Proxies:  87
Dead Proxies:     263
Success Rate:     24.86%
Avg Response:     52.34ms
==================================================
```

## Supported Proxy Sources

The tool fetches from these maintained sources:

- ProxyScrape API
- TheSpeedX/PROXY-List
- monosans/proxy-list
- ShiftyTR/Proxy-List
- jetkai/proxy-list
- zevtyardt/proxy-list
- clarketm/proxy-list
- opsxcq/proxy-list
- sunny9577/proxy-scraper
- And more...

All sources are actively updated daily/hourly.

## Configuration

Edit default settings in the `ProxyChecker` class:

```python
self.test_url = "http://httpbin.org/ip"  # Test endpoint
self.timeout = 5                          # Timeout in seconds
self.proxy_type = "http"                  # Default proxy type
```

## Dependencies

```
requests>=2.28.0
colorama>=0.4.6
```

Install with:
```bash
pip install -r requirements.txt
```

## Performance Tips

- **Increase threads** for faster checking: Modify `max_workers=50` in `check_proxies()` (use 50-100)
- **Adjust timeout** for slower networks: Change `self.timeout = 5` to higher value
- **Use SOCKS proxies** for better anonymity and evasion
- **Run during off-peak hours** for better grab success rates

## Troubleshooting

**No proxies found?**
- Some sources may be temporarily down
- Try again in a few minutes
- Check your internet connection

**"PySocks not installed" error?**
- Install with: `pip install requests[socks]`

**Low success rate?**
- Free proxies have low reliability (20-30% is normal)
- Increase timeout value
- Try different proxy type

**Permission denied on save?**
- Run with admin privileges or check folder permissions

## Project Structure

```
strika-proxy-checker/
├── strikaproxytool.py    # Main application
├── requirements.txt       # Dependencies
├── README.md             # This file
├── working_proxies.txt   # Output file (generated)
└── .gitignore           # Git ignore rules
```

## Legal & Disclaimer

⚠️ **Use responsibly and legally**

This tool is for educational and authorized testing purposes only. Users are responsible for:
- Complying with local laws and regulations
- Obtaining proper authorization before testing
- Respecting target website terms of service
- Not using for malicious activities

The authors assume no liability for misuse.

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest new proxy sources
- Improve performance
- Add new features

Submit pull requests or open issues on GitHub.

## Roadmap

- [ ] GUI version with PyQt5
- [ ] Proxy filtering by country/speed/anonymity
- [ ] Schedule automated checks
- [ ] API endpoint for live proxy list
- [ ] Proxy rotation feature
- [ ] JSON/CSV export options
- [ ] Proxy geolocation detection

## License

MIT License - See LICENSE file for details

## Support

Found a bug or have a suggestion? Open an issue on GitHub!

---

Made with ❤️ by [ImStrika]
Star ⭐ if you found this useful!
