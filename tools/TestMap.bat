@echo off && cd..
mode con: cols=80 lines=8
title Debugging 
cd scripts && python test_map.py
echo Invalid Map Name
pause >nul
exit
