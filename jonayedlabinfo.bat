@echo off
title Jonayed Lab System Info - Professional Edition v2.0
color 0A

echo.
echo  ============================================================================
echo  ^|         JONAYED LAB SYSTEM INFO - PROFESSIONAL EDITION v2.0              ^|
echo  ^|              Advanced System Diagnostic Tool                             ^|
echo  ============================================================================
echo.
echo  [*] Starting system scan...
echo.

:: Run the PowerShell script
powershell -ExecutionPolicy Bypass -File "%~dp0jonayedlabinfo.ps1"

echo.
echo  Press any key to exit...
pause >nul
