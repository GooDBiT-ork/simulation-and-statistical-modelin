import datetime
import logging
import psutil
import os
import sys
import json
import time
from pathlib import Path
import signal
import win32api
import ctypes

if not ctypes.windll.shell32.IsUserAnAdmin():
    print('Запуск от имени администратора')
    win32api.ShellExecute(0, 'runas', sys.executable, __file__, None, 1)
    

logger = logging.getLogger('process_watcher')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('process_watcher.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
for process in psutil.process_iter():
  logger.info(f"{datetime.datetime.now()} - Process started: {process.name()} {process.exe()}")
  
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

if process.name() in blacklisted_apps:
  logger.info(f"Forbidden process detected: {process.name()}")
  
  try:
    process.terminate()
    logger.info(f"Process {process.name()} terminated successfully")
  except Exception as e:
    logger.error(f"Error terminating process {process.name()}: {e}")