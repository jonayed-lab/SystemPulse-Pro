<p align="center">
  <img src="https://img.icons8.com/fluency/96/processor.png" alt="SystemPulse Logo" width="100"/>
</p>

<h1 align="center">SystemPulse Pro</h1>

<p align="center">
  <strong>Advanced System Diagnostic & Information Tool</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0-blue.svg" alt="Version"/>
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey.svg" alt="Platform"/>
  <img src="https://img.shields.io/badge/python-3.6+-green.svg" alt="Python"/>
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License"/>
  <img src="https://img.shields.io/github/stars/jonayed-lab/SystemPulse-Pro?style=social" alt="Stars"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Love%20by%20JONAYED-red.svg" alt="Made with Love"/>
</p>

---

## Overview

**SystemPulse Pro** is a powerful, professional-grade system information and diagnostic tool for Windows. It generates beautiful, interactive HTML reports containing comprehensive details about your computer's hardware, software, network, and security configuration.

> **Two Versions Available:**
> - **Python Version** (`ap.py`) - Full-featured with real-time monitoring
> - **Batch Version** (`jonayedlabinfo.bat`) - Works without Python installation

---

## Features

### Core Features

| Feature | Description |
|---------|-------------|
| **System Overview** | Complete system information including OS, uptime, and boot time |
| **CPU Analysis** | Processor details, cores, frequency, and real-time usage |
| **Memory Monitoring** | RAM specifications, usage statistics, and available memory |
| **Storage Information** | Physical drives, partitions, and disk space analysis |
| **GPU Details** | Graphics card specifications and driver information |
| **Network Analysis** | Adapters, IP configuration, and network statistics |
| **Process Monitor** | Top processes by memory/CPU usage |
| **Security Status** | Antivirus detection and user privileges |
| **Battery Status** | Battery health and charge information (laptops) |

### UI/UX Features

- **Modern Dark Theme** - Easy on the eyes with gradient backgrounds
- **Interactive Tabs** - Organized navigation between sections
- **Animated Elements** - Smooth transitions and hover effects
- **Responsive Design** - Works on all screen sizes
- **Print Support** - Print-optimized layouts
- **Export Options** - JSON export (Python version)

---

## Requirements

### Python Version (`ap.py`)

| Requirement | Version |
|-------------|---------|
| Python | 3.6 or higher |
| psutil | Latest |

### Batch Version (`jonayedlabinfo.bat`)

| Requirement | Version |
|-------------|---------|
| Windows | 7/8/10/11 |
| PowerShell | 5.0 or higher (pre-installed) |

> **Note:** The Batch version requires NO additional installations!

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/jonayed-lab/SystemPulse-Pro.git
```

Or download the ZIP file and extract it.

### Step 2: Navigate to the Project Directory

```bash
cd SystemPulse-Pro
```

### Step 3: Install Dependencies (Python Version Only)

```bash
pip install psutil
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

---

## Usage

### Option 1: Python Version (Recommended)

The Python version provides more detailed information and real-time monitoring.

#### Run via Command Line:

```bash
python ap.py
```

#### Run by Double-Click:

Simply double-click `ap.py` if Python is set as the default handler.

#### What Happens:

1. Script checks for required dependencies
2. If `psutil` is missing, you'll see installation options
3. System information is collected (takes 10-30 seconds)
4. HTML report is generated and opens in your browser

---

### Option 2: Batch Version (No Python Needed)

Perfect for systems without Python installed.

#### Run via Double-Click:

Double-click `jonayedlabinfo.bat`

#### Run via Command Line:

```cmd
jonayedlabinfo.bat
```

#### Alternative - Run PowerShell Script Directly:

```powershell
powershell -ExecutionPolicy Bypass -File jonayedlabinfo.ps1
```

#### What Happens:

1. PowerShell collects system information (takes 1-2 minutes)
2. Professional HTML report is generated
3. Report is saved to `JonayedLab_Reports` folder
4. Report automatically opens in your browser

---

## Output

### Report Location

| Version | Output Location |
|---------|-----------------|
| Python | `Jonayed_System_Info_Pro.html` (same directory) |
| Batch | `JonayedLab_Reports/SystemReport_[timestamp].html` |

### Report Sections

| Section | Information Included |
|---------|---------------------|
| **System** | Full systeminfo output, OS details, uptime |
| **Hardware** | CPU, RAM, Motherboard, BIOS, GPU, Display, Audio, Battery |
| **Storage** | Physical drives, Partitions with usage statistics |
| **Network** | Network adapters, IP configuration, Statistics |
| **Processes** | Top processes sorted by memory usage |
| **Software** | Startup programs, Running services |
| **Security** | Antivirus status, User account information |

---

## Screenshots

### Main Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  🔲 Jonayed Lab                           [Hostname] [User] │
│  System Information Pro                    [Date] ● Online  │
├─────────────────────────────────────────────────────────────┤
│  [Print Report]  [Export JSON]  [Refresh]                   │
├─────────────────────────────────────────────────────────────┤
│  [System] [Hardware] [Storage] [Network] [Processes] ...    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ CPU Usage   │ │ Memory      │ │ Disk        │           │
│  │   25%       │ │   68%       │ │   45%       │           │
│  │ ████░░░░░░  │ │ ██████░░░░  │ │ ████░░░░░░  │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Operating System                                     │   │
│  │ Windows 10 Pro | Build 19045 | x64                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
SystemPulse-Pro/
│
├── ap.py                    # Python version (full-featured)
├── jonayedlabinfo.bat       # Batch launcher
├── jonayedlabinfo.ps1       # PowerShell script
├── README.md                # This file
├── LICENSE                  # MIT License
├── requirements.txt         # Python dependencies
│
└── JonayedLab_Reports/      # Generated reports (Batch version)
    └── SystemReport_*.html
```

---

## Comparison: Python vs Batch Version

| Feature | Python Version | Batch Version |
|---------|---------------|---------------|
| Real-time CPU/Memory % | ✅ Yes | ❌ No |
| Export to JSON | ✅ Yes | ❌ No |
| Progress Bars | ✅ Visual | ❌ Text only |
| Installation Required | Python + psutil | None |
| Execution Speed | Fast (~10s) | Medium (~1-2min) |
| Works Offline | ✅ Yes | ✅ Yes |
| Professional UI | ✅ Yes | ✅ Yes |
| Process Details | ✅ Memory + CPU | ✅ Memory only |

---

## Troubleshooting

### Python Version Issues

<details>
<summary><b>Error: "ModuleNotFoundError: No module named 'psutil'"</b></summary>

Install psutil using pip:
```bash
pip install psutil
```

Or use the batch version which doesn't require Python.
</details>

<details>
<summary><b>Error: "Python is not recognized"</b></summary>

1. Make sure Python is installed
2. Add Python to your system PATH
3. Or use the batch version instead
</details>

<details>
<summary><b>Script doesn't open the report</b></summary>

1. Check if the HTML file was created
2. Open the HTML file manually in your browser
3. Check for any error messages in the console
</details>

### Batch Version Issues

<details>
<summary><b>Error: "Running scripts is disabled on this system"</b></summary>

Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or run the batch file which bypasses this automatically.
</details>

<details>
<summary><b>Report shows "N/A" for some fields</b></summary>

Some information requires administrator privileges. Try:
1. Right-click `jonayedlabinfo.bat`
2. Select "Run as administrator"
</details>

<details>
<summary><b>Antivirus blocks the script</b></summary>

The scripts are safe. Add an exception in your antivirus for:
- `jonayedlabinfo.bat`
- `jonayedlabinfo.ps1`
</details>

---

## Advanced Usage

### Running with Administrator Privileges

For complete system information, run with elevated privileges:

```cmd
# Right-click Command Prompt -> Run as Administrator
cd path\to\SystemPulse-Pro
python ap.py
```

### Scheduling Reports

Create a scheduled task to generate reports automatically:

```cmd
# Using Task Scheduler
schtasks /create /tn "SystemPulse Report" /tr "python C:\path\to\ap.py" /sc daily /st 09:00
```

### Command Line Arguments (Future Feature)

```bash
# Coming soon
python ap.py --output custom_report.html
python ap.py --sections cpu,ram,disk
python ap.py --format json
```

---

## Contributing

Contributions are welcome! Here's how you can help:

### Step 1: Fork the Repository

Click the "Fork" button at the top of this page.

### Step 2: Clone Your Fork

```bash
git clone https://github.com/jonayed-lab/SystemPulse-Pro.git
```

### Step 3: Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### Step 4: Make Changes

Add your improvements or bug fixes.

### Step 5: Commit Changes

```bash
git add .
git commit -m "Add: Description of your changes"
```

### Step 6: Push to GitHub

```bash
git push origin feature/your-feature-name
```

### Step 7: Create Pull Request

Go to the original repository and click "New Pull Request".

---

## Roadmap

### Version 2.1 (Coming Soon)
- [ ] Temperature monitoring (CPU/GPU)
- [ ] Disk health status (S.M.A.R.T.)
- [ ] Network speed test
- [ ] Historical data comparison

### Version 2.2 (Planned)
- [ ] Linux support
- [ ] macOS support
- [ ] Command-line arguments
- [ ] Custom themes

### Version 3.0 (Future)
- [ ] GUI application
- [ ] Real-time monitoring dashboard
- [ ] Cloud sync for reports
- [ ] Mobile app companion

---

## Support

If you find this project helpful, please consider:

- Giving it a ⭐ on GitHub
- Sharing it with others
- [Reporting issues](https://github.com/jonayed-lab/SystemPulse-Pro/issues)
- Contributing to the code

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 JONAYED

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## Author

<p align="center">
  <img src="https://img.shields.io/badge/Created%20by-JONAYED-blue.svg?style=for-the-badge" alt="Author"/>
</p>

<p align="center">
  <a href="https://github.com/jonayed-lab">
    <img src="https://img.shields.io/badge/GitHub-jonayed--lab-181717?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
</p>

---

<p align="center">
  <strong>Made with ❤️ by JONAYED</strong>
</p>

<p align="center">
  <sub>For System Administrators & Power Users</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Thank%20You-For%20Using%20SystemPulse%20Pro-brightgreen.svg" alt="Thank You"/>
</p>
