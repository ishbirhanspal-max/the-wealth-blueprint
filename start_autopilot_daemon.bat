@echo off
title The Wealth Blueprint - Infinite Autopilot Daemon
cd /d "%~dp0"
echo ========================================================
echo   THE WEALTH BLUEPRINT: INFINITE AUTOPILOT DAEMON
echo ========================================================
echo.
python autonomous_autopilot_engine.py --daemon
pause
