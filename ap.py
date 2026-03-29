# Jonayed Lab System Info - PROFESSIONAL EDITION v2.0
# Advanced System Diagnostic & Information Tool

import subprocess
import webbrowser
import platform
import socket
import uuid
import datetime
import os
import sys
import json

# ================== DEPENDENCY CHECK ==================

def check_dependencies():
    """Check if required packages are installed"""
    missing_packages = []

    try:
        import psutil
    except ImportError:
        missing_packages.append("psutil")

    return missing_packages

def show_dependency_error():
    """Show error message and guide to batch file"""
    print("\n" + "=" * 70)
    print("  JONAYED LAB SYSTEM INFO - DEPENDENCY ERROR")
    print("=" * 70)
    print("\n  [!] Required Python packages are not installed!")
    print("\n  Missing packages: psutil")
    print("\n  You have TWO options:")
    print("\n  OPTION 1: Install the required package")
    print("  -------------------------------------------")
    print("  Run this command in your terminal/command prompt:")
    print("\n      pip install psutil")
    print("\n  Then run this script again.")
    print("\n  OPTION 2: Use the Batch Version (NO PYTHON NEEDED)")
    print("  -------------------------------------------")
    print("  Run the batch file instead - it works without Python!")
    print("\n      jonayedlabinfo.bat")
    print("\n  The batch file provides similar system information")
    print("  and generates a professional HTML report.")
    print("\n" + "=" * 70)

    # Ask user what they want to do
    print("\n  What would you like to do?")
    print("  [1] Try to install psutil automatically")
    print("  [2] Open the batch file location")
    print("  [3] Exit")

    try:
        choice = input("\n  Enter your choice (1/2/3): ").strip()

        if choice == "1":
            print("\n  [*] Attempting to install psutil...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
                print("\n  [+] psutil installed successfully!")
                print("  [*] Please run this script again.")
            except Exception as e:
                print(f"\n  [!] Failed to install: {e}")
                print("  [*] Please install manually using: pip install psutil")
                print("  [*] Or use the batch file: jonayedlabinfo.bat")

        elif choice == "2":
            batch_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jonayedlabinfo.bat")
            if os.path.exists(batch_file):
                print(f"\n  [*] Opening folder containing batch file...")
                os.startfile(os.path.dirname(batch_file))
                print(f"\n  [+] Look for: jonayedlabinfo.bat")
                print("  [*] Double-click it to run!")
            else:
                print(f"\n  [!] Batch file not found at: {batch_file}")
                print("  [*] Please make sure jonayedlabinfo.bat is in the same folder.")

        elif choice == "3":
            print("\n  Goodbye!")

        else:
            print("\n  [!] Invalid choice. Exiting...")

    except KeyboardInterrupt:
        print("\n\n  Cancelled by user.")

    input("\n  Press Enter to exit...")
    sys.exit(1)

# Check dependencies before proceeding
missing = check_dependencies()
if missing:
    show_dependency_error()

# Import psutil after dependency check passes
import psutil

def run(cmd):
    """Execute command and return output"""
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode(errors="ignore")
        return result.strip() if result.strip() else "N/A"
    except:
        return "N/A"

def get_size(bytes_val):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024

def get_uptime():
    """Get system uptime"""
    try:
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        now = datetime.datetime.now()
        uptime = now - boot_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m", boot_time.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "N/A", "N/A"

# ================== SYSTEM COLLECTION ==================

print("🔍 Collecting System Information...")

# Basic System Info
system_info = {
    "hostname": socket.gethostname(),
    "username": os.getlogin(),
    "platform": platform.system(),
    "platform_release": platform.release(),
    "platform_version": platform.version(),
    "architecture": platform.machine(),
    "processor": platform.processor(),
    "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
}

uptime_str, boot_time = get_uptime()

# OS Information
print("📋 Getting OS Information...")
os_info = run("wmic os get Caption,Version,InstallDate,BuildNumber,OSArchitecture /format:list")

# CPU Information
print("🖥️ Getting CPU Information...")
cpu_info = run("wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed,CurrentClockSpeed,L2CacheSize,L3CacheSize /format:list")
cpu_usage = psutil.cpu_percent(interval=1)
cpu_freq = psutil.cpu_freq()
cpu_count = psutil.cpu_count()
cpu_count_physical = psutil.cpu_count(logical=False)

# RAM Information
print("💾 Getting Memory Information...")
ram_info = run("wmic memorychip get Manufacturer,Capacity,Speed,DeviceLocator,PartNumber /format:list")
virtual_mem = psutil.virtual_memory()

# Motherboard Information
print("🔧 Getting Motherboard Information...")
board_info = run("wmic baseboard get Manufacturer,Product,Version,SerialNumber /format:list")

# BIOS Information
print("⚙️ Getting BIOS Information...")
bios_info = run("wmic bios get Manufacturer,Name,Version,ReleaseDate,SerialNumber /format:list")

# Storage Information
print("💿 Getting Storage Information...")
disk_info = run("wmic diskdrive get Model,Size,SerialNumber,InterfaceType,Status /format:list")
partitions = psutil.disk_partitions()
disk_usage_data = []
for partition in partitions:
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage_data.append({
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "fstype": partition.fstype,
            "total": get_size(usage.total),
            "used": get_size(usage.used),
            "free": get_size(usage.free),
            "percent": usage.percent
        })
    except:
        pass

# GPU Information
print("🎮 Getting GPU Information...")
gpu_info = run("wmic path win32_videocontroller get Name,DriverVersion,AdapterRAM,CurrentRefreshRate,VideoModeDescription,DriverDate /format:list")

# Display Information
print("🖥️ Getting Display Information...")
display_info = run("wmic desktopmonitor get Name,ScreenHeight,ScreenWidth,PixelsPerXLogicalInch /format:list")

# Network Information
print("🌐 Getting Network Information...")
network_info = run("wmic nic where NetEnabled=true get Name,MACAddress,Speed,Manufacturer /format:list")
ip_config = run("ipconfig /all")

# Get network stats
net_io = psutil.net_io_counters()

# Battery Information
print("🔋 Getting Battery Information...")
battery = psutil.sensors_battery()
battery_status = None
if battery:
    battery_status = {
        "percent": battery.percent,
        "plugged": "Charging" if battery.power_plugged else "On Battery",
        "time_left": str(datetime.timedelta(seconds=battery.secsleft)) if battery.secsleft > 0 else "Calculating..." if battery.secsleft == -2 else "Unlimited (Plugged)"
    }

# Running Processes
print("📊 Getting Running Processes...")
processes = []
for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
    try:
        processes.append(proc.info)
    except:
        pass
top_processes = sorted(processes, key=lambda x: x.get('memory_percent', 0) or 0, reverse=True)[:15]

# Startup Programs
print("🚀 Getting Startup Programs...")
startup_programs = run("wmic startup get Caption,Command,Location /format:list")

# Installed Software (Top 30)
print("📦 Getting Installed Software...")
installed_software = run("wmic product get Name,Version,Vendor /format:list")

# Audio Devices
print("🔊 Getting Audio Devices...")
audio_devices = run("wmic sounddev get Name,Manufacturer,Status /format:list")

# USB Devices
print("🔌 Getting USB Devices...")
usb_devices = run("wmic path Win32_USBControllerDevice get Dependent /format:list")
usb_info = run("wmic path Win32_PnPEntity where \"PNPClass='USB'\" get Name,Manufacturer,Status /format:list")

# Printers
print("🖨️ Getting Printer Information...")
printers = run("wmic printer get Name,Default,DriverName,PortName,PrinterStatus /format:list")

# Antivirus Status
print("🛡️ Getting Security Information...")
antivirus = run("wmic /namespace:\\\\root\\SecurityCenter2 path AntivirusProduct get displayName,productState /format:list")

# Windows Services (Running)
print("⚡ Getting Services...")
running_services = run("wmic service where state='Running' get Name,DisplayName,StartMode /format:list")

# Environment Variables
print("🔐 Getting Environment Info...")
env_vars = {
    "TEMP": os.environ.get("TEMP", "N/A"),
    "PATH_COUNT": len(os.environ.get("PATH", "").split(";")),
    "COMPUTERNAME": os.environ.get("COMPUTERNAME", "N/A"),
    "USERPROFILE": os.environ.get("USERPROFILE", "N/A"),
    "PROCESSOR_ARCHITECTURE": os.environ.get("PROCESSOR_ARCHITECTURE", "N/A")
}

# Current Date/Time
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("🎨 Generating Professional Report...")

# ================== HTML GENERATION ==================

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jonayed Lab - System Information Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a25;
            --bg-card-hover: #22222f;
            --accent-primary: #6366f1;
            --accent-secondary: #8b5cf6;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-danger: #ef4444;
            --accent-info: #06b6d4;
            --text-primary: #ffffff;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --border-color: #27272a;
            --gradient-1: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            --gradient-2: linear-gradient(135deg, #06b6d4 0%, #10b981 100%);
            --gradient-3: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}

        /* Animated Background */
        .bg-animation {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }}

        .bg-animation::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(6, 182, 212, 0.05) 0%, transparent 40%);
            animation: backgroundMove 20s ease-in-out infinite;
        }}

        @keyframes backgroundMove {{
            0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
            25% {{ transform: translate(-5%, 5%) rotate(1deg); }}
            50% {{ transform: translate(5%, -5%) rotate(-1deg); }}
            75% {{ transform: translate(-3%, -3%) rotate(0.5deg); }}
        }}

        /* Header */
        .header {{
            background: linear-gradient(180deg, var(--bg-secondary) 0%, transparent 100%);
            padding: 30px 40px;
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(20px);
        }}

        .header-content {{
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .logo-icon {{
            width: 50px;
            height: 50px;
            background: var(--gradient-1);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3);
        }}

        .logo-text h1 {{
            font-size: 24px;
            font-weight: 700;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .logo-text span {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        .header-info {{
            display: flex;
            gap: 30px;
            align-items: center;
        }}

        .header-stat {{
            text-align: right;
        }}

        .header-stat label {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .header-stat value {{
            display: block;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
        }}

        /* Main Container */
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 30px 40px;
        }}

        /* Quick Stats */
        .quick-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: var(--gradient-1);
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-primary);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
        }}

        .stat-card.cpu::before {{ background: var(--gradient-1); }}
        .stat-card.memory::before {{ background: var(--gradient-2); }}
        .stat-card.disk::before {{ background: var(--gradient-3); }}
        .stat-card.network::before {{ background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%); }}

        .stat-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}

        .stat-icon {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}

        .stat-card.cpu .stat-icon {{ background: rgba(99, 102, 241, 0.2); color: #6366f1; }}
        .stat-card.memory .stat-icon {{ background: rgba(16, 185, 129, 0.2); color: #10b981; }}
        .stat-card.disk .stat-icon {{ background: rgba(245, 158, 11, 0.2); color: #f59e0b; }}
        .stat-card.network .stat-icon {{ background: rgba(236, 72, 153, 0.2); color: #ec4899; }}
        .stat-card.battery .stat-icon {{ background: rgba(6, 182, 212, 0.2); color: #06b6d4; }}

        .stat-card.battery::before {{ background: linear-gradient(135deg, #06b6d4 0%, #10b981 100%); }}

        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        .stat-bar {{
            width: 100%;
            height: 6px;
            background: var(--bg-secondary);
            border-radius: 3px;
            margin-top: 15px;
            overflow: hidden;
        }}

        .stat-bar-fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 1s ease;
        }}

        .stat-card.cpu .stat-bar-fill {{ background: var(--gradient-1); }}
        .stat-card.memory .stat-bar-fill {{ background: var(--gradient-2); }}
        .stat-card.disk .stat-bar-fill {{ background: var(--gradient-3); }}
        .stat-card.network .stat-bar-fill {{ background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%); }}
        .stat-card.battery .stat-bar-fill {{ background: linear-gradient(135deg, #06b6d4 0%, #10b981 100%); }}

        /* Navigation Tabs */
        .nav-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            background: var(--bg-card);
            padding: 10px;
            border-radius: 16px;
            border: 1px solid var(--border-color);
        }}

        .nav-tab {{
            padding: 12px 24px;
            border-radius: 10px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .nav-tab:hover {{
            background: var(--bg-secondary);
            color: var(--text-primary);
        }}

        .nav-tab.active {{
            background: var(--gradient-1);
            color: white;
            box-shadow: 0 5px 20px rgba(99, 102, 241, 0.3);
        }}

        /* Content Sections */
        .section {{
            display: none;
            animation: fadeIn 0.5s ease;
        }}

        .section.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Info Cards */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
        }}

        .info-card {{
            background: var(--bg-card);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .info-card:hover {{
            border-color: var(--accent-primary);
            box-shadow: 0 10px 40px rgba(99, 102, 241, 0.1);
        }}

        .info-card-header {{
            padding: 20px 24px;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .info-card-header i {{
            font-size: 20px;
            color: var(--accent-primary);
        }}

        .info-card-header h3 {{
            font-size: 16px;
            font-weight: 600;
        }}

        .info-card-body {{
            padding: 24px;
        }}

        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid var(--border-color);
        }}

        .info-row:last-child {{
            border-bottom: none;
        }}

        .info-row label {{
            color: var(--text-muted);
            font-size: 13px;
        }}

        .info-row value {{
            color: var(--text-primary);
            font-weight: 500;
            font-size: 13px;
            text-align: right;
            max-width: 60%;
            word-break: break-all;
        }}

        /* Process Table */
        .process-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .process-table th,
        .process-table td {{
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}

        .process-table th {{
            background: var(--bg-secondary);
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
        }}

        .process-table td {{
            font-size: 13px;
        }}

        .process-table tr:hover td {{
            background: var(--bg-card-hover);
        }}

        .process-badge {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
        }}

        .process-badge.high {{
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }}

        .process-badge.medium {{
            background: rgba(245, 158, 11, 0.2);
            color: #f59e0b;
        }}

        .process-badge.low {{
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
        }}

        /* Code Block */
        .code-block {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 12px;
            line-height: 1.8;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-all;
            color: var(--text-secondary);
            max-height: 400px;
            overflow-y: auto;
        }}

        .code-block::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        .code-block::-webkit-scrollbar-track {{
            background: var(--bg-card);
            border-radius: 4px;
        }}

        .code-block::-webkit-scrollbar-thumb {{
            background: var(--border-color);
            border-radius: 4px;
        }}

        /* Disk Card */
        .disk-card {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }}

        .disk-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .disk-name {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .disk-name i {{
            color: var(--accent-primary);
        }}

        .disk-progress {{
            width: 100%;
            height: 8px;
            background: var(--bg-card);
            border-radius: 4px;
            overflow: hidden;
        }}

        .disk-progress-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 1s ease;
        }}

        .disk-info {{
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 13px;
            border-top: 1px solid var(--border-color);
            margin-top: 40px;
        }}

        .footer a {{
            color: var(--accent-primary);
            text-decoration: none;
        }}

        /* Utility Button */
        .btn {{
            padding: 12px 24px;
            border-radius: 10px;
            border: none;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}

        .btn-primary {{
            background: var(--gradient-1);
            color: white;
            box-shadow: 0 5px 20px rgba(99, 102, 241, 0.3);
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        }}

        .btn-secondary {{
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }}

        .btn-secondary:hover {{
            background: var(--bg-card-hover);
            border-color: var(--accent-primary);
        }}

        /* Action Buttons */
        .action-buttons {{
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}

        /* Status Badge */
        .status {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }}

        .status.online {{
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
        }}

        .status.offline {{
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }}

        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        .status.online .status-dot {{
            background: #10b981;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .header-content {{
                flex-direction: column;
                gap: 20px;
                text-align: center;
            }}
            .header-info {{
                justify-content: center;
            }}
            .info-grid {{
                grid-template-columns: 1fr;
            }}
            .container {{
                padding: 20px;
            }}
            .nav-tabs {{
                justify-content: center;
            }}
        }}

        /* Print Styles */
        @media print {{
            .bg-animation, .nav-tabs, .action-buttons {{ display: none; }}
            .section {{ display: block !important; page-break-inside: avoid; }}
            body {{ background: white; color: black; }}
            .info-card {{ border: 1px solid #ddd; }}
        }}
    </style>
</head>
<body>
    <div class="bg-animation"></div>

    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <div class="logo">
                <div class="logo-icon">
                    <i class="fas fa-microchip"></i>
                </div>
                <div class="logo-text">
                    <h1>Jonayed Lab</h1>
                    <span>System Information Pro</span>
                </div>
            </div>
            <div class="header-info">
                <div class="header-stat">
                    <label>Hostname</label>
                    <value>{system_info['hostname']}</value>
                </div>
                <div class="header-stat">
                    <label>User</label>
                    <value>{system_info['username']}</value>
                </div>
                <div class="header-stat">
                    <label>Report Generated</label>
                    <value>{current_time}</value>
                </div>
                <span class="status online">
                    <span class="status-dot"></span>
                    System Online
                </span>
            </div>
        </div>
    </header>

    <div class="container">
        <!-- Quick Stats -->
        <div class="quick-stats">
            <div class="stat-card cpu">
                <div class="stat-header">
                    <div>
                        <div class="stat-value">{cpu_usage}%</div>
                        <div class="stat-label">CPU Usage</div>
                    </div>
                    <div class="stat-icon">
                        <i class="fas fa-microchip"></i>
                    </div>
                </div>
                <div class="stat-bar">
                    <div class="stat-bar-fill" style="width: {cpu_usage}%"></div>
                </div>
            </div>

            <div class="stat-card memory">
                <div class="stat-header">
                    <div>
                        <div class="stat-value">{virtual_mem.percent}%</div>
                        <div class="stat-label">Memory ({get_size(virtual_mem.used)} / {get_size(virtual_mem.total)})</div>
                    </div>
                    <div class="stat-icon">
                        <i class="fas fa-memory"></i>
                    </div>
                </div>
                <div class="stat-bar">
                    <div class="stat-bar-fill" style="width: {virtual_mem.percent}%"></div>
                </div>
            </div>

            <div class="stat-card disk">
                <div class="stat-header">
                    <div>
                        <div class="stat-value">{disk_usage_data[0]['percent'] if disk_usage_data else 0}%</div>
                        <div class="stat-label">Disk ({disk_usage_data[0]['used'] if disk_usage_data else 'N/A'} / {disk_usage_data[0]['total'] if disk_usage_data else 'N/A'})</div>
                    </div>
                    <div class="stat-icon">
                        <i class="fas fa-hdd"></i>
                    </div>
                </div>
                <div class="stat-bar">
                    <div class="stat-bar-fill" style="width: {disk_usage_data[0]['percent'] if disk_usage_data else 0}%"></div>
                </div>
            </div>

            <div class="stat-card network">
                <div class="stat-header">
                    <div>
                        <div class="stat-value">{get_size(net_io.bytes_sent)}</div>
                        <div class="stat-label">Total Sent / {get_size(net_io.bytes_recv)} Received</div>
                    </div>
                    <div class="stat-icon">
                        <i class="fas fa-network-wired"></i>
                    </div>
                </div>
                <div class="stat-bar">
                    <div class="stat-bar-fill" style="width: 70%"></div>
                </div>
            </div>

            {'<div class="stat-card battery"><div class="stat-header"><div><div class="stat-value">' + str(battery_status["percent"]) + '%</div><div class="stat-label">' + battery_status["plugged"] + ' - ' + battery_status["time_left"] + '</div></div><div class="stat-icon"><i class="fas fa-battery-three-quarters"></i></div></div><div class="stat-bar"><div class="stat-bar-fill" style="width: ' + str(battery_status["percent"]) + '%"></div></div></div>' if battery_status else ''}
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
            <button class="btn btn-primary" onclick="window.print()">
                <i class="fas fa-print"></i> Print Report
            </button>
            <button class="btn btn-secondary" onclick="exportJson()">
                <i class="fas fa-download"></i> Export JSON
            </button>
            <button class="btn btn-secondary" onclick="location.reload()">
                <i class="fas fa-sync"></i> Refresh
            </button>
        </div>

        <!-- Navigation -->
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showSection('overview')">
                <i class="fas fa-home"></i> Overview
            </button>
            <button class="nav-tab" onclick="showSection('hardware')">
                <i class="fas fa-server"></i> Hardware
            </button>
            <button class="nav-tab" onclick="showSection('storage')">
                <i class="fas fa-database"></i> Storage
            </button>
            <button class="nav-tab" onclick="showSection('network')">
                <i class="fas fa-wifi"></i> Network
            </button>
            <button class="nav-tab" onclick="showSection('processes')">
                <i class="fas fa-tasks"></i> Processes
            </button>
            <button class="nav-tab" onclick="showSection('software')">
                <i class="fas fa-box"></i> Software
            </button>
            <button class="nav-tab" onclick="showSection('security')">
                <i class="fas fa-shield-alt"></i> Security
            </button>
            <button class="nav-tab" onclick="showSection('advanced')">
                <i class="fas fa-cogs"></i> Advanced
            </button>
        </div>

        <!-- Overview Section -->
        <div class="section active" id="overview">
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fab fa-windows"></i>
                        <h3>Operating System</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="info-row">
                            <label>Platform</label>
                            <value>{system_info['platform']} {system_info['platform_release']}</value>
                        </div>
                        <div class="info-row">
                            <label>Version</label>
                            <value>{system_info['platform_version']}</value>
                        </div>
                        <div class="info-row">
                            <label>Architecture</label>
                            <value>{system_info['architecture']}</value>
                        </div>
                        <div class="info-row">
                            <label>Hostname</label>
                            <value>{system_info['hostname']}</value>
                        </div>
                        <div class="info-row">
                            <label>Username</label>
                            <value>{system_info['username']}</value>
                        </div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-clock"></i>
                        <h3>System Uptime</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="info-row">
                            <label>Uptime</label>
                            <value>{uptime_str}</value>
                        </div>
                        <div class="info-row">
                            <label>Last Boot</label>
                            <value>{boot_time}</value>
                        </div>
                        <div class="info-row">
                            <label>Current Time</label>
                            <value>{current_time}</value>
                        </div>
                        <div class="info-row">
                            <label>Processor Type</label>
                            <value>{env_vars['PROCESSOR_ARCHITECTURE']}</value>
                        </div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-microchip"></i>
                        <h3>CPU Summary</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="info-row">
                            <label>Processor</label>
                            <value>{system_info['processor']}</value>
                        </div>
                        <div class="info-row">
                            <label>Physical Cores</label>
                            <value>{cpu_count_physical}</value>
                        </div>
                        <div class="info-row">
                            <label>Logical Cores</label>
                            <value>{cpu_count}</value>
                        </div>
                        <div class="info-row">
                            <label>Current Frequency</label>
                            <value>{f"{cpu_freq.current:.0f} MHz" if cpu_freq else "N/A"}</value>
                        </div>
                        <div class="info-row">
                            <label>Current Usage</label>
                            <value>{cpu_usage}%</value>
                        </div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-memory"></i>
                        <h3>Memory Summary</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="info-row">
                            <label>Total RAM</label>
                            <value>{get_size(virtual_mem.total)}</value>
                        </div>
                        <div class="info-row">
                            <label>Used RAM</label>
                            <value>{get_size(virtual_mem.used)}</value>
                        </div>
                        <div class="info-row">
                            <label>Available RAM</label>
                            <value>{get_size(virtual_mem.available)}</value>
                        </div>
                        <div class="info-row">
                            <label>Usage</label>
                            <value>{virtual_mem.percent}%</value>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Hardware Section -->
        <div class="section" id="hardware">
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-microchip"></i>
                        <h3>CPU Details</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{cpu_info}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-memory"></i>
                        <h3>RAM Details</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{ram_info}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-desktop"></i>
                        <h3>Motherboard</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{board_info}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-cog"></i>
                        <h3>BIOS Information</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{bios_info}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-gamepad"></i>
                        <h3>Graphics Card (GPU)</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{gpu_info}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-tv"></i>
                        <h3>Display</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{display_info}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-volume-up"></i>
                        <h3>Audio Devices</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{audio_devices}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-usb"></i>
                        <h3>USB Devices</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{usb_info}</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Storage Section -->
        <div class="section" id="storage">
            <div class="info-grid">
                <div class="info-card" style="grid-column: 1 / -1;">
                    <div class="info-card-header">
                        <i class="fas fa-hdd"></i>
                        <h3>Disk Partitions</h3>
                    </div>
                    <div class="info-card-body">
                        {"".join([f'''
                        <div class="disk-card">
                            <div class="disk-header">
                                <div class="disk-name">
                                    <i class="fas fa-hdd"></i>
                                    <strong>{d['device']}</strong> ({d['fstype']})
                                </div>
                                <span>{d['percent']}% used</span>
                            </div>
                            <div class="disk-progress">
                                <div class="disk-progress-fill" style="width: {d['percent']}%; background: {'var(--accent-danger)' if d['percent'] > 90 else 'var(--accent-warning)' if d['percent'] > 70 else 'var(--gradient-2)'}"></div>
                            </div>
                            <div class="disk-info">
                                <span>Used: {d['used']}</span>
                                <span>Free: {d['free']}</span>
                                <span>Total: {d['total']}</span>
                            </div>
                        </div>
                        ''' for d in disk_usage_data])}
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-database"></i>
                        <h3>Physical Drives</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{disk_info}</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Network Section -->
        <div class="section" id="network">
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-network-wired"></i>
                        <h3>Network Adapters</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{network_info}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-exchange-alt"></i>
                        <h3>Network Statistics</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="info-row">
                            <label>Total Bytes Sent</label>
                            <value>{get_size(net_io.bytes_sent)}</value>
                        </div>
                        <div class="info-row">
                            <label>Total Bytes Received</label>
                            <value>{get_size(net_io.bytes_recv)}</value>
                        </div>
                        <div class="info-row">
                            <label>Packets Sent</label>
                            <value>{net_io.packets_sent:,}</value>
                        </div>
                        <div class="info-row">
                            <label>Packets Received</label>
                            <value>{net_io.packets_recv:,}</value>
                        </div>
                        <div class="info-row">
                            <label>Errors In</label>
                            <value>{net_io.errin}</value>
                        </div>
                        <div class="info-row">
                            <label>Errors Out</label>
                            <value>{net_io.errout}</value>
                        </div>
                        <div class="info-row">
                            <label>MAC Address</label>
                            <value>{system_info['mac_address']}</value>
                        </div>
                    </div>
                </div>

                <div class="info-card" style="grid-column: 1 / -1;">
                    <div class="info-card-header">
                        <i class="fas fa-globe"></i>
                        <h3>IP Configuration</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{ip_config}</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Processes Section -->
        <div class="section" id="processes">
            <div class="info-card" style="margin-bottom: 20px;">
                <div class="info-card-header">
                    <i class="fas fa-tasks"></i>
                    <h3>Top Processes by Memory Usage</h3>
                </div>
                <div class="info-card-body" style="padding: 0;">
                    <table class="process-table">
                        <thead>
                            <tr>
                                <th>PID</th>
                                <th>Process Name</th>
                                <th>Memory %</th>
                                <th>CPU %</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {"".join([f'''
                            <tr>
                                <td>{p.get('pid', 'N/A')}</td>
                                <td>{p.get('name', 'N/A')}</td>
                                <td>{p.get('memory_percent', 0):.2f}%</td>
                                <td>{p.get('cpu_percent', 0):.1f}%</td>
                                <td><span class="process-badge {'high' if (p.get('memory_percent') or 0) > 5 else 'medium' if (p.get('memory_percent') or 0) > 2 else 'low'}">{'High' if (p.get('memory_percent') or 0) > 5 else 'Medium' if (p.get('memory_percent') or 0) > 2 else 'Low'}</span></td>
                            </tr>
                            ''' for p in top_processes])}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Software Section -->
        <div class="section" id="software">
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-rocket"></i>
                        <h3>Startup Programs</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{startup_programs}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-print"></i>
                        <h3>Printers</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{printers}</div>
                    </div>
                </div>

                <div class="info-card" style="grid-column: 1 / -1;">
                    <div class="info-card-header">
                        <i class="fas fa-box-open"></i>
                        <h3>Installed Software</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block" style="max-height: 500px;">{installed_software}</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Security Section -->
        <div class="section" id="security">
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-shield-alt"></i>
                        <h3>Antivirus Status</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{antivirus}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-folder"></i>
                        <h3>Environment Info</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="info-row">
                            <label>Computer Name</label>
                            <value>{env_vars['COMPUTERNAME']}</value>
                        </div>
                        <div class="info-row">
                            <label>User Profile</label>
                            <value>{env_vars['USERPROFILE']}</value>
                        </div>
                        <div class="info-row">
                            <label>TEMP Folder</label>
                            <value>{env_vars['TEMP']}</value>
                        </div>
                        <div class="info-row">
                            <label>PATH Entries</label>
                            <value>{env_vars['PATH_COUNT']} entries</value>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Advanced Section -->
        <div class="section" id="advanced">
            <div class="info-grid">
                <div class="info-card" style="grid-column: 1 / -1;">
                    <div class="info-card-header">
                        <i class="fas fa-cogs"></i>
                        <h3>Running Services</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block" style="max-height: 500px;">{running_services}</div>
                    </div>
                </div>

                <div class="info-card">
                    <div class="info-card-header">
                        <i class="fas fa-info-circle"></i>
                        <h3>OS Details</h3>
                    </div>
                    <div class="info-card-body">
                        <div class="code-block">{os_info}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <p><strong>Jonayed Lab System Info Pro</strong> - Professional Edition v2.0</p>
        <p>Generated on {current_time} | Powered by Python & psutil</p>
        <p style="margin-top: 10px; opacity: 0.7;">Made with ❤️ for System Administrators & Power Users</p>
    </footer>

    <script>
        // Tab Navigation
        function showSection(sectionId) {{
            // Hide all sections
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            // Remove active from all tabs
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            // Show selected section
            document.getElementById(sectionId).classList.add('active');
            // Add active to clicked tab
            event.target.closest('.nav-tab').classList.add('active');
        }}

        // Export JSON
        function exportJson() {{
            const data = {{
                system: {json.dumps(system_info)},
                uptime: "{uptime_str}",
                boot_time: "{boot_time}",
                cpu_usage: {cpu_usage},
                memory: {{
                    total: "{get_size(virtual_mem.total)}",
                    used: "{get_size(virtual_mem.used)}",
                    percent: {virtual_mem.percent}
                }},
                network: {{
                    bytes_sent: "{get_size(net_io.bytes_sent)}",
                    bytes_recv: "{get_size(net_io.bytes_recv)}"
                }},
                generated: "{current_time}"
            }};

            const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'system_info_' + new Date().toISOString().slice(0,10) + '.json';
            a.click();
            URL.revokeObjectURL(url);
        }}

        // Smooth scroll for long content
        document.querySelectorAll('.code-block').forEach(block => {{
            block.style.scrollBehavior = 'smooth';
        }});
    </script>
</body>
</html>
"""

# Save HTML Report
output_file = "Jonayed_System_Info_Pro.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ Professional System Report Generated: {output_file}")
print("🌐 Opening in browser...")

webbrowser.open(output_file)
