Automated Nmap Scanner with GUI
A professional, user-friendly desktop application that provides a graphical interface for Nmap port scanning. This tool allows users to scan IP addresses for open ports and services, displaying results in a clean GUI and saving them to text files.
<img width="691" height="626" alt="Screenshot 2026-03-12 112302" src="https://github.com/user-attachments/assets/4dc8d9cd-acce-45a8-925f-da077774b1b4" />


Main application interface with input fields for target IP and port range

📸 Screenshots
Main Application Window
<img width="691" height="626" alt="Screenshot 2026-03-12 112302" src="https://github.com/user-attachments/assets/b208ec96-09a9-419f-a0e7-255fad97a3bb" />

Clean and intuitive interface with target IP input, port range selection, and control buttons

Scan Results Display
<img width="699" height="629" alt="Screenshot 2026-03-12 112317" src="https://github.com/user-attachments/assets/4c1f965f-7dc3-4391-a6bc-d3377aca59bd" />

Results showing scan time and port status with color-coded output

Detailed Output
<img width="485" height="529" alt="Screenshot 2026-03-12 112417" src="https://github.com/user-attachments/assets/39d2f605-7803-498e-9359-dd9ff56ae00f" />

Formatted scan results with clear port status information

✨ Features
Graphical User Interface: Built with Tkinter for easy, intuitive interaction

Port Scanning: Scan any IP address for open ports within a specified range

Service Detection: Automatically identifies services running on open ports

Real-time Results: Displays scan results in a scrollable, color-coded text area

🟢 Green: Open ports

🔴 Red: Closed ports

🔵 Blue: Header information

Save Functionality: Export scan results to text files with automatic naming

Input Validation: Comprehensive error checking for IP addresses and port ranges

Non-blocking Operations: Scanning runs in separate threads to prevent GUI freezing

Status Updates: Real-time status bar showing "Ready", "Scanning...", "Scan Completed"

Cross-platform: Works on Windows, macOS, and Linux

🛠️ Prerequisites
Before running this application, ensure you have the following installed:

Python 3.6 or higher

Nmap (Network Mapper) - Download here

python-nmap library

📦 Installation
Step 1: Install Nmap
Download and install Nmap from the official website:

Windows: Download installer from https://nmap.org/download.html

Important: During installation, check "Add Nmap to the system PATH"

macOS: brew install nmap

Linux:

Ubuntu/Debian: sudo apt-get install nmap

CentOS/RHEL: sudo yum install nmap

Verify Nmap installation:

bash
nmap --version
Step 2: Clone the Repository
bash
git clone https://github.com/yourusername/automated-nmap-scanner.git
cd automated-nmap-scanner
Step 3: Install Python Dependencies
bash
pip install -r requirements.txt
🚀 Usage
Run the application:

bash
python main.py
Enter scan parameters:

Target IP Address: Enter the IP you want to scan (e.g., 192.168.1.1 or scanme.nmap.org)

Port Range: Specify the ports to scan (e.g., 1-1000 or 22,80,443)

Click "Start Scan" to begin scanning

View results in the scrollable text area with color-coded output

Click "Save Results" to export the scan to a text file

Click "Clear Output" to reset the display

📁 Project Structure
text
automated-nmap-scanner/
│
├── main.py              # GUI application and user interface
├── scanner.py           # Nmap scanning logic
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── screenshots/        # Application screenshots
    ├── main_window.png
    ├── scan_results.png
    └── detailed_output.png
💻 Code Example
python
# Example: Quick scan of common ports
from scanner import NmapScanner

scanner = NmapScanner()
results = scanner.quick_scan("192.168.1.1")
for port in results['ports']:
    print(f"Port {port['port']} - {port['state']} - {port['service']}")
⚙️ How It Works
GUI Layer (main.py): Provides the user interface, handles input validation, and displays results

Scanner Layer (scanner.py): Interfaces with Nmap through python-nmap library

Threading: Scanning runs in separate threads to keep the interface responsive

Data Flow: User inputs → Validation → Nmap scan → Result formatting → Display/Save

🎯 Features in Detail
Input Validation
Validates IPv4 address format

Checks port range validity (1-65535)

Ensures proper format (e.g., "1-1000" or "80")

Prevents empty field submissions

Scan Results
Displays target IP and scan duration

Lists all scanned ports with their status

Shows service names and versions when available

Color-coded for easy identification

Save Functionality
Automatic filename generation: scan_results_<IP>.txt

File dialog for custom save locations

Preserves formatting in saved files

🐛 Troubleshooting
"Nmap not found" error
Ensure Nmap is installed

Add Nmap to your system PATH

Restart the application after installation

Verify with nmap --version in command prompt

Permission errors (Windows)
Run Command Prompt as Administrator

Or scan ports above 1024 (non-privileged ports)

Slow scans
Reduce the port range (e.g., 1-100 instead of 1-1000)

Check network connectivity

Some networks may have firewall restrictions

No open ports found
Try scanme.nmap.org (Nmap's test server)

Ensure the target is reachable (try pinging it)

Check if firewall is blocking the scan

🤝 Contributing
Contributions are welcome! Here are some ways you can contribute:

🐛 Report bugs

💡 Suggest new features

📝 Improve documentation

🔧 Submit pull requests

Feature Ideas
Export to CSV/JSON formats

Network discovery feature

Save scan profiles

Dark mode theme

Real-time scan progress bar

Multiple scan types (SYN, UDP, etc.)

📜 License
This project is open source and available under the MIT License.

⚠️ Disclaimer
This tool is intended for:

✅ Educational purposes

✅ Security testing on your own networks

✅ Networks you have permission to scan

Unauthorized scanning of networks may be:

❌ Illegal

❌ Against terms of service

❌ Considered hostile activity

Always obtain proper written authorization before scanning any network or system you do not own.

🙏 Acknowledgments
Nmap - The industry standard for network discovery

python-nmap - Python wrapper for Nmap

Python's Tkinter team for the GUI framework
