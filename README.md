\# 🛡️ Grae-X Magic Eye Shield



\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

\[!\[Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

\[!\[Windows](https://img.shields.io/badge/platform-Windows-blue)](https://github.com)



\*\*Real-time file type detector\*\* that protects you from disguised malware. When a file's extension doesn't match its true content (magic bytes), you get an instant futuristic popup warning.



!\[Demo Screenshot](docs/screenshot.png) \*(Add a screenshot later)\*



\## ✨ Features



\- 🔍 \*\*Real-time monitoring\*\* of Downloads and Desktop folders

\- ⚡ \*\*Magic byte detection\*\* – sees through file renaming tricks

\- 🚨 \*\*Futuristic popup alerts\*\* when suspicious files are detected

\- 🖥️ \*\*System tray icon\*\* for easy access

\- 🧠 \*\*Smart detection\*\* – flags EXE files disguised as PDFs, JPGs, etc.

\- 🎯 \*\*Zero configuration\*\* – works right out of the box



\## 📦 Installation



\### Option 1: Run from Source (for developers)



1\. \*\*Clone the repository\*\*

&nbsp;  ```bash

&nbsp;  git clone https://github.com/graexlabs/Grae-X-Magic-Eye-Shield.git

&nbsp;  cd Grae-X-Magic-Eye-Shield

Install Python 3.8+ (if not already installed)



Install dependencies



bash

pip install -r requirements.txt

Run the application



bash

python src/main.py

Option 2: Download Executable (for end users)

Download the latest Grae-X-Magic-Eye-Shield.exe from the Releases page.



Just double-click and run – no Python installation needed!



🚀 How to Use

Launch the application (system tray icon appears)



Download any file – the tool automatically monitors your Downloads folder



If a file is suspicious, a popup appears immediately:



https://docs/alert.png



Right-click the tray icon to open Downloads or exit



🧪 Testing the Tool

Create a test file to see it in action:



bash

\# Copy any EXE file (like notepad.exe) to your Downloads folder

copy C:\\Windows\\System32\\notepad.exe %USERPROFILE%\\Downloads\\innocent.pdf

Within seconds, you'll see the warning popup!



🛠️ Building Your Own Executable

To create a standalone .exe:



bash

\# Install Nuitka

pip install nuitka



\# Build with Nuitka (recommended for fewer false positives)

python -m nuitka --onefile --windows-disable-console --windows-icon-from-ico=icon.ico --output-dir=dist src/main.py



\# Or with PyInstaller

pip install pyinstaller

python -m PyInstaller --onefile --windowed --name "Grae-X Magic Eye Shield" --icon=icon.ico src/main.py

The executable will be in the dist folder.



⚠️ Antivirus False Positives

Some antivirus software may flag the executable because it contains an embedded Python interpreter. This is a false positive. To fix:



Add an exception in your antivirus



Or run from source (Option 1 above)



We're working on code signing to eliminate this



📋 Requirements

Windows 10/11 (64-bit)



Python 3.8+ (only for source version)



🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.



Fork the repository



Create your feature branch (git checkout -b feature/AmazingFeature)



Commit your changes (git commit -m 'Add some AmazingFeature')



Push to the branch (git push origin feature/AmazingFeature)



Open a Pull Request



📄 License

Distributed under the MIT License. See LICENSE for more information.



📧 Contact

Grae-X Labs - @graexlabs - security@graexlabs.com



Project Link: https://github.com/graexlabs/Grae-X-Magic-Eye-Shield



🙏 Acknowledgments

python-magic for file type detection



customtkinter for the beautiful UI



watchdog for file system monitoring



text



---



\### `requirements.txt`



```txt

watchdog>=4.0.0

python-magic-bin>=0.4.14

customtkinter>=5.2.0

pystray>=0.19.0

pillow>=10.0.0

