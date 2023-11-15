import os
import sys
import json
import time
from pathlib import Path
import win32api
import ctypes
import psutil

# admin
if not ctypes.windll.shell32.IsUserAnAdmin():
    print('Запуск от имени администратора')
    win32api.ShellExecute(0, 'runas', sys.executable, __file__, None, 1)
    

# for proc in psutil.process_iter():
#     try:
#         print(proc.cwd())
#         print(proc.exe())
#     except psutil.AccessDenied:
#         continue
    
config_file = Path('config.json')

if not config_file.exists():
    print('Конфигурационный файл не найден')
    sys.exit(1)

with config_file.open() as f:
    config = json.load(f)

blacklisted_apps = config['blacklistedapps']

if not blacklisted_apps:
    print('Нет запрещенных приложений в конфиге')
    sys.exit(1)

while True:
    for process in blacklisted_apps:
        os.system(f'taskkill /f /im {os.path.basename(process)}')
        print(f'Процесс {os.path.basename(process)} завершен')

    time.sleep(5)