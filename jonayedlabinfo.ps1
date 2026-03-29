# Jonayed Lab System Info - Professional Edition v2.0
# PowerShell Script for System Information Report

$ErrorActionPreference = 'SilentlyContinue'

# Create output directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputDir = Join-Path $scriptPath "JonayedLab_Reports"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Generate filename with timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportFile = Join-Path $outputDir "SystemReport_$timestamp.html"
$dateStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host ""
Write-Host "  [*] Collecting System Information..." -ForegroundColor Cyan
Write-Host ""

# Collect all system information
Write-Host "  [1/15] System Info..." -ForegroundColor Yellow
$sysInfo = systeminfo 2>$null | Out-String

Write-Host "  [2/15] OS Details..." -ForegroundColor Yellow
$osInfo = Get-CimInstance Win32_OperatingSystem | Format-List Caption,Version,BuildNumber,OSArchitecture,InstallDate,SerialNumber | Out-String

Write-Host "  [3/15] CPU Info..." -ForegroundColor Yellow
$cpuInfo = Get-CimInstance Win32_Processor | Format-List Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed,Manufacturer,ProcessorId | Out-String

Write-Host "  [4/15] Memory Info..." -ForegroundColor Yellow
$ramInfo = Get-CimInstance Win32_PhysicalMemory | Format-List Manufacturer,Capacity,Speed,DeviceLocator,PartNumber | Out-String
$ramUsage = Get-CimInstance Win32_OperatingSystem | Select-Object @{N='Total Memory (GB)';E={[math]::Round($_.TotalVisibleMemorySize/1MB,2)}},@{N='Free Memory (GB)';E={[math]::Round($_.FreePhysicalMemory/1MB,2)}},@{N='Used Memory (GB)';E={[math]::Round(($_.TotalVisibleMemorySize - $_.FreePhysicalMemory)/1MB,2)}} | Format-List | Out-String

Write-Host "  [5/15] Motherboard Info..." -ForegroundColor Yellow
$boardInfo = Get-CimInstance Win32_BaseBoard | Format-List Manufacturer,Product,Version,SerialNumber | Out-String

Write-Host "  [6/15] BIOS Info..." -ForegroundColor Yellow
$biosInfo = Get-CimInstance Win32_BIOS | Format-List Manufacturer,Name,Version,ReleaseDate,SerialNumber,SMBIOSBIOSVersion | Out-String

Write-Host "  [7/15] GPU Info..." -ForegroundColor Yellow
$gpuInfo = Get-CimInstance Win32_VideoController | Format-List Name,DriverVersion,AdapterRAM,VideoModeDescription,CurrentRefreshRate,DriverDate | Out-String

Write-Host "  [8/15] Storage Info..." -ForegroundColor Yellow
$diskInfo = Get-CimInstance Win32_DiskDrive | Format-List Model,Size,SerialNumber,InterfaceType,Status,MediaType | Out-String
$partInfo = Get-CimInstance Win32_LogicalDisk | Where-Object {$_.DriveType -eq 3} | Select-Object DeviceID,VolumeName,FileSystem,@{N='Size(GB)';E={[math]::Round($_.Size/1GB,2)}},@{N='Free(GB)';E={[math]::Round($_.FreeSpace/1GB,2)}},@{N='Used(GB)';E={[math]::Round(($_.Size - $_.FreeSpace)/1GB,2)}},@{N='Used%';E={[math]::Round((($_.Size - $_.FreeSpace)/$_.Size)*100,1)}} | Format-Table -AutoSize | Out-String

Write-Host "  [9/15] Network Info..." -ForegroundColor Yellow
$netAdapter = Get-CimInstance Win32_NetworkAdapter -Filter "NetEnabled=true" | Format-List Name,MACAddress,Speed,Manufacturer,AdapterType | Out-String
$ipConfig = ipconfig /all 2>$null | Out-String
$netStats = netstat -e 2>$null | Out-String

Write-Host "  [10/15] Battery Info..." -ForegroundColor Yellow
$batteryInfo = Get-CimInstance Win32_Battery | Format-List EstimatedChargeRemaining,BatteryStatus,DesignCapacity,FullChargeCapacity | Out-String
if ([string]::IsNullOrWhiteSpace($batteryInfo)) {
    $batteryInfo = "No battery detected (Desktop PC or battery not available)"
}

Write-Host "  [11/15] Process Info..." -ForegroundColor Yellow
$processes = Get-Process | Sort-Object -Property WorkingSet64 -Descending | Select-Object -First 25 Name,Id,@{N='Memory(MB)';E={[math]::Round($_.WorkingSet64/1MB,2)}},@{N='CPU(s)';E={[math]::Round($_.CPU,2)}} | Format-Table -AutoSize | Out-String

Write-Host "  [12/15] Startup Programs..." -ForegroundColor Yellow
$startup = Get-CimInstance Win32_StartupCommand | Select-Object Caption,Command,Location,User | Format-List | Out-String

Write-Host "  [13/15] Services..." -ForegroundColor Yellow
$services = Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object Name,DisplayName,Status | Format-Table -AutoSize | Out-String

Write-Host "  [14/15] Security Info..." -ForegroundColor Yellow
$avInfo = Get-CimInstance -Namespace "root/SecurityCenter2" -ClassName AntivirusProduct 2>$null | Format-List displayName,productState | Out-String
if ([string]::IsNullOrWhiteSpace($avInfo)) {
    $avInfo = "Unable to retrieve antivirus information (may require elevated privileges)"
}
$userInfo = whoami /all 2>$null | Out-String

Write-Host "  [15/15] Audio & Display..." -ForegroundColor Yellow
$audioInfo = Get-CimInstance Win32_SoundDevice | Format-List Name,Manufacturer,Status | Out-String
$displayInfo = Get-CimInstance Win32_DesktopMonitor | Format-List Name,ScreenHeight,ScreenWidth,MonitorType | Out-String

Write-Host ""
Write-Host "  [*] Generating HTML Report..." -ForegroundColor Green
Write-Host ""

# Get system info
$hostname = $env:COMPUTERNAME
$username = $env:USERNAME

# Function to escape HTML
function EscapeHtml($text) {
    if ([string]::IsNullOrEmpty($text)) { return "N/A" }
    $text = $text -replace '&', '&amp;'
    $text = $text -replace '<', '&lt;'
    $text = $text -replace '>', '&gt;'
    $text = $text -replace '"', '&quot;'
    return $text
}

# Build HTML
$html = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jonayed Lab - System Info Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0a0f;
            color: #ffffff;
            min-height: 100vh;
            line-height: 1.6;
        }

        .bg-glow {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background:
                radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.08) 0%, transparent 50%);
            animation: bgPulse 10s ease-in-out infinite;
        }

        @keyframes bgPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .header {
            background: rgba(18, 18, 26, 0.95);
            backdrop-filter: blur(20px);
            padding: 25px 40px;
            border-bottom: 1px solid rgba(99, 102, 241, 0.3);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1500px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo-icon {
            width: 55px;
            height: 55px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            box-shadow: 0 10px 40px rgba(99, 102, 241, 0.4);
            animation: iconFloat 3s ease-in-out infinite;
        }

        @keyframes iconFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }

        .logo h1 {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #6366f1, #a855f7, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .logo span {
            display: block;
            font-size: 11px;
            color: #71717a;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-top: 2px;
        }

        .batch-tag {
            display: inline-block;
            padding: 4px 12px;
            background: linear-gradient(135deg, #f59e0b, #ef4444);
            border-radius: 20px;
            font-size: 10px;
            font-weight: 700;
            color: white;
            margin-left: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: tagPulse 2s ease-in-out infinite;
        }

        @keyframes tagPulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
            50% { box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
        }

        .header-info {
            display: flex;
            gap: 35px;
            align-items: center;
            flex-wrap: wrap;
        }

        .header-stat {
            text-align: center;
            padding: 10px 20px;
            background: rgba(39, 39, 42, 0.5);
            border-radius: 12px;
            border: 1px solid rgba(63, 63, 70, 0.5);
        }

        .header-stat label {
            display: block;
            font-size: 10px;
            color: #71717a;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }

        .header-stat value {
            display: block;
            font-size: 14px;
            font-weight: 600;
            color: #e4e4e7;
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 30px;
            font-size: 13px;
            font-weight: 500;
            color: #10b981;
        }

        .status-dot {
            width: 10px;
            height: 10px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s infinite;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(0.9); }
        }

        .container {
            max-width: 1500px;
            margin: 0 auto;
            padding: 30px 40px;
        }

        .action-bar {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .btn {
            padding: 14px 30px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            border: none;
            text-decoration: none;
        }

        .btn-primary {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(99, 102, 241, 0.5);
        }

        .btn-secondary {
            background: rgba(39, 39, 42, 0.8);
            color: #e4e4e7;
            border: 1px solid rgba(63, 63, 70, 0.8);
        }

        .btn-secondary:hover {
            background: rgba(63, 63, 70, 0.8);
            border-color: rgba(99, 102, 241, 0.5);
            transform: translateY(-2px);
        }

        .nav-container {
            background: rgba(26, 26, 37, 0.8);
            border-radius: 16px;
            padding: 12px;
            margin-bottom: 30px;
            border: 1px solid rgba(39, 39, 42, 0.8);
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .nav-btn {
            padding: 14px 24px;
            background: transparent;
            border: none;
            color: #a1a1aa;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            border-radius: 12px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .nav-btn:hover {
            background: rgba(99, 102, 241, 0.15);
            color: #e4e4e7;
        }

        .nav-btn.active {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        }

        .nav-btn i {
            font-size: 16px;
        }

        .section {
            display: none;
            animation: fadeIn 0.5s ease;
        }

        .section.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 24px;
        }

        .card {
            background: rgba(26, 26, 37, 0.9);
            border-radius: 20px;
            border: 1px solid rgba(39, 39, 42, 0.8);
            overflow: hidden;
            transition: all 0.4s ease;
        }

        .card:hover {
            border-color: rgba(99, 102, 241, 0.5);
            box-shadow: 0 25px 60px rgba(99, 102, 241, 0.15);
            transform: translateY(-5px);
        }

        .card.full {
            grid-column: 1 / -1;
        }

        .card-header {
            padding: 22px 28px;
            background: linear-gradient(135deg, rgba(18, 18, 26, 0.9), rgba(26, 26, 37, 0.9));
            border-bottom: 1px solid rgba(39, 39, 42, 0.8);
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .card-header i {
            font-size: 22px;
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #8b5cf6;
        }

        .card-header h3 {
            font-size: 18px;
            font-weight: 600;
            color: #f4f4f5;
        }

        .card-body {
            padding: 28px;
        }

        .code-block {
            background: linear-gradient(135deg, rgba(10, 10, 15, 0.9), rgba(15, 15, 22, 0.9));
            border-radius: 14px;
            padding: 24px;
            font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
            font-size: 13px;
            line-height: 1.9;
            color: #a1a1aa;
            max-height: 500px;
            overflow: auto;
            white-space: pre-wrap;
            word-break: break-word;
            border: 1px solid rgba(39, 39, 42, 0.5);
        }

        .code-block::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        .code-block::-webkit-scrollbar-track {
            background: rgba(26, 26, 37, 0.5);
            border-radius: 5px;
        }

        .code-block::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-radius: 5px;
        }

        .code-block::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #8b5cf6, #a855f7);
        }

        .footer {
            text-align: center;
            padding: 50px 40px;
            margin-top: 50px;
            border-top: 1px solid rgba(39, 39, 42, 0.5);
            background: rgba(18, 18, 26, 0.5);
        }

        .footer p {
            color: #71717a;
            margin-bottom: 8px;
        }

        .footer strong {
            color: #a1a1aa;
            font-size: 18px;
        }

        .footer .hearts {
            color: #ef4444;
            animation: heartbeat 1.5s ease-in-out infinite;
        }

        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }

        @media (max-width: 900px) {
            .header-content { flex-direction: column; text-align: center; }
            .header-info { justify-content: center; }
            .grid { grid-template-columns: 1fr; }
            .container { padding: 20px; }
            .nav-container { justify-content: center; }
            .card { margin-bottom: 15px; }
        }

        @media print {
            .bg-glow, .nav-container, .action-bar { display: none; }
            .section { display: block !important; page-break-inside: avoid; margin-bottom: 20px; }
            body { background: white; color: black; }
            .card { border: 1px solid #ddd; box-shadow: none; transform: none !important; }
            .card-header { background: #f5f5f5; }
            .code-block { background: #f9f9f9; color: #333; max-height: none; }
            .header { position: relative; background: #f5f5f5; }
        }
    </style>
</head>
<body>
    <div class="bg-glow"></div>

    <header class="header">
        <div class="header-content">
            <div class="logo">
                <div class="logo-icon"><i class="fas fa-microchip"></i></div>
                <div>
                    <h1>Jonayed Lab <span class="batch-tag">Batch</span></h1>
                    <span>System Information Pro v2.0</span>
                </div>
            </div>
            <div class="header-info">
                <div class="header-stat">
                    <label>Hostname</label>
                    <value>$hostname</value>
                </div>
                <div class="header-stat">
                    <label>User</label>
                    <value>$username</value>
                </div>
                <div class="header-stat">
                    <label>Generated</label>
                    <value>$dateStr</value>
                </div>
                <div class="status-badge">
                    <span class="status-dot"></span>
                    System Online
                </div>
            </div>
        </div>
    </header>

    <div class="container">
        <div class="action-bar">
            <button class="btn btn-primary" onclick="window.print()">
                <i class="fas fa-print"></i> Print Report
            </button>
            <button class="btn btn-secondary" onclick="location.reload()">
                <i class="fas fa-sync"></i> Refresh
            </button>
        </div>

        <div class="nav-container">
            <button class="nav-btn active" onclick="showTab('system')">
                <i class="fas fa-info-circle"></i> System
            </button>
            <button class="nav-btn" onclick="showTab('hardware')">
                <i class="fas fa-server"></i> Hardware
            </button>
            <button class="nav-btn" onclick="showTab('storage')">
                <i class="fas fa-database"></i> Storage
            </button>
            <button class="nav-btn" onclick="showTab('network')">
                <i class="fas fa-wifi"></i> Network
            </button>
            <button class="nav-btn" onclick="showTab('processes')">
                <i class="fas fa-tasks"></i> Processes
            </button>
            <button class="nav-btn" onclick="showTab('software')">
                <i class="fas fa-box"></i> Software
            </button>
            <button class="nav-btn" onclick="showTab('security')">
                <i class="fas fa-shield-alt"></i> Security
            </button>
        </div>

        <!-- SYSTEM SECTION -->
        <div class="section active" id="system">
            <div class="grid">
                <div class="card full">
                    <div class="card-header">
                        <i class="fab fa-windows"></i>
                        <h3>Complete System Information</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $sysInfo)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-desktop"></i>
                        <h3>Operating System Details</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $osInfo)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- HARDWARE SECTION -->
        <div class="section" id="hardware">
            <div class="grid">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-microchip"></i>
                        <h3>CPU / Processor</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $cpuInfo)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-memory"></i>
                        <h3>Memory / RAM</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $ramInfo)

=== MEMORY USAGE ===
$(EscapeHtml $ramUsage)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-th-large"></i>
                        <h3>Motherboard</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $boardInfo)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-cog"></i>
                        <h3>BIOS Information</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $biosInfo)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-gamepad"></i>
                        <h3>Graphics Card / GPU</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $gpuInfo)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-tv"></i>
                        <h3>Display / Monitor</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $displayInfo)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-volume-up"></i>
                        <h3>Audio Devices</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $audioInfo)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-battery-three-quarters"></i>
                        <h3>Battery Status</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $batteryInfo)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- STORAGE SECTION -->
        <div class="section" id="storage">
            <div class="grid">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-hdd"></i>
                        <h3>Physical Drives</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $diskInfo)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-folder"></i>
                        <h3>Disk Partitions</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $partInfo)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- NETWORK SECTION -->
        <div class="section" id="network">
            <div class="grid">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-network-wired"></i>
                        <h3>Network Adapters</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $netAdapter)</div>
                    </div>
                </div>
                <div class="card full">
                    <div class="card-header">
                        <i class="fas fa-globe"></i>
                        <h3>IP Configuration</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $ipConfig)</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-exchange-alt"></i>
                        <h3>Network Statistics</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $netStats)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- PROCESSES SECTION -->
        <div class="section" id="processes">
            <div class="grid">
                <div class="card full">
                    <div class="card-header">
                        <i class="fas fa-tasks"></i>
                        <h3>Top 25 Processes by Memory Usage</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $processes)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SOFTWARE SECTION -->
        <div class="section" id="software">
            <div class="grid">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-rocket"></i>
                        <h3>Startup Programs</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $startup)</div>
                    </div>
                </div>
                <div class="card full">
                    <div class="card-header">
                        <i class="fas fa-cogs"></i>
                        <h3>Running Services</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $services)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SECURITY SECTION -->
        <div class="section" id="security">
            <div class="grid">
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-shield-alt"></i>
                        <h3>Antivirus Software</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $avInfo)</div>
                    </div>
                </div>
                <div class="card full">
                    <div class="card-header">
                        <i class="fas fa-user-shield"></i>
                        <h3>Current User Information</h3>
                    </div>
                    <div class="card-body">
                        <div class="code-block">$(EscapeHtml $userInfo)</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="footer">
        <p><strong>Jonayed Lab System Info Pro</strong></p>
        <p>Batch Edition v2.0</p>
        <p style="margin-top: 15px;">Report Generated: $dateStr</p>
        <p style="margin-top: 20px; opacity: 0.7;">
            Made with <span class="hearts">Love By JONAYED</span> for System Administrators & Power Users
        </p>
        <p style="opacity: 0.5; margin-top: 10px;">No Python Required - Works on any Windows System</p>
    </footer>

    <script>
        function showTab(tabId) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(function(section) {
                section.classList.remove('active');
            });

            // Remove active class from all nav buttons
            document.querySelectorAll('.nav-btn').forEach(function(btn) {
                btn.classList.remove('active');
            });

            // Show selected section
            document.getElementById(tabId).classList.add('active');

            // Add active class to clicked button
            event.target.closest('.nav-btn').classList.add('active');
        }
    </script>
</body>
</html>
"@

# Save HTML file
$html | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "  ============================================================================" -ForegroundColor Green
Write-Host "  |                    REPORT GENERATED SUCCESSFULLY!                        |" -ForegroundColor Green
Write-Host "  ============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  [+] Report saved to:" -ForegroundColor Yellow
Write-Host "      $reportFile" -ForegroundColor White
Write-Host ""
Write-Host "  [+] Reports folder:" -ForegroundColor Yellow
Write-Host "      $outputDir" -ForegroundColor White
Write-Host ""
Write-Host "  [*] Opening report in your default browser..." -ForegroundColor Cyan
Write-Host ""

# Open report in browser
Start-Process $reportFile
