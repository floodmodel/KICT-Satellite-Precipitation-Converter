@echo off
call "C:\Program Files\QGIS 3.34.8\bin\o4w_env.bat"

@echo on
%PYTHONHOME%/python.exe -m venv --system-site-packages .venv