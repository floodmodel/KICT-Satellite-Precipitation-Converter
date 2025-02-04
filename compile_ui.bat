@echo off
call "C:\Program Files\QGIS 3.34.8\bin\o4w_env.bat"

@echo on
pyuic5 Kict_Satellite_Precipitation_Converter/GPM.ui > Kict_Satellite_Precipitation_Converter/GPM_ui.py