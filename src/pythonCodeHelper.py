import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import subprocess
import sys
import requests
import threading

# Глобальные переменные для языка и переводов
current_language = "ru"
translations = {
    "ru": {
        "title": "Python Editor",
        "open_file": "Открыть файл",
        "save_file": "Сохранить файл",
        "run_code": "Запустить код",
        "install_library": "Установить библиотеку",
        "bg_color_label": "Цвет фона:",
        "choose_bg": "Выбрать фон",
        "btn_color_label": "Цвет кнопок:",
        "choose_btn": "Выбрать кнопки",
        "scale_label": "Масштаб окна (px):",
        "apply": "Применить настройки",
        "toggle_language": "English"
    },
    "en": {
        "title": "Python Editor",
        "open_file": "Open File",
        "save_file": "Save File",
        "run_code": "Run Code",
        "install_library": "Install Library",
        "bg_color_label": "Background Color:",
        "choose_bg": "Choose Background",
        "btn_color_label": "Button Color:",
        "choose_btn": "Choose Buttons",
        "scale_label": "Window Scale (px):",
        "apply": "Apply Settings",
        "toggle_language": "Русский"
    }
}

# --------------------- Функции работы с файлом --------------------- #
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text_area.delete("1.0", tk.END)
                text_area.insert(tk.END, f.read())
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                             filetypes=[("Python Files", "*.py")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

# --------------------- Функции установки библиотек --------------------- #
def install_library():
    lib_name = lib_entry.get().strip()
    if lib_name:
        try:
            response = requests.get(f"https://pypi.org/pypi/{lib_name}/json", timeout=5)
            if response.status_code == 200:
                threading.Thread(
                    target=lambda: subprocess.run([sys.executable, "-m", "pip", "install", lib_name])
                ).start()
                messagebox.showinfo("Установка", f"Библиотека '{lib_name}' устанавливается...")
            else:
                messagebox.showerror("Ошибка", f"Библиотека '{lib_name}' не найдена!")
        except requests.exceptions.RequestException:
            messagebox.showerror("Ошибка", "Не удалось подключиться к PyPI. Проверьте интернет.")

def install_pip():
    try:
        subprocess.run([sys.executable, "-m", "ensurepip"], check=True)
        messagebox.showinfo("Установка pip", "pip успешно установлен!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Ошибка", "Не удалось установить pip!")

def open_library_window():
    libs_window = ctk.CTkToplevel(app)
    libs_window.title("Установка библиотек")
    libs_window.geometry("400x200")
    
    lbl = ctk.CTkLabel(libs_window, text="Введите название библиотеки:")
    lbl.pack(pady=5)
    
    global lib_entry
    lib_entry = ctk.CTkEntry(libs_window, width=250)
    lib_entry.pack(pady=5)
    
    btn_install = ctk.CTkButton(libs_window, text="Установить", command=install_library)
    btn_install.pack(pady=5)
    
    btn_install_pip = ctk.CTkButton(libs_window, text="Установить pip", command=install_pip)
    btn_install_pip.pack(pady=5)

# --------------------- Функция запуска кода --------------------- #
def run_code():
    code = text_area.get("1.0", tk.END).strip()
    if code:
        with open("temp_script.py", "w", encoding="utf-8") as f:
            f.write(code)
        try:
            threading.Thread(
                target=lambda: subprocess.run(["start", "cmd", "/K", "python temp_script.py"], shell=True)
            ).start()
        except Exception as e:
            messagebox.showerror("Ошибка выполнения", f"Ошибка: {e}")

# --------------------- Функции настроек (выбор цвета через спектр) --------------------- #
def choose_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        global_bg_color.set(color)
        bg_color_label.configure(text=f"{translations[current_language]['bg_color_label']} {color}")

def choose_btn_color():
    color = colorchooser.askcolor()[1]
    if color:
        global_btn_color.set(color)
        btn_color_label.configure(text=f"{translations[current_language]['btn_color_label']} {color}")

def apply_settings():
    app.configure(bg_color=global_bg_color.get())
    btn_run.configure(fg_color=global_btn_color.get())
    btn_open.configure(fg_color=global_btn_color.get())
    btn_save.configure(fg_color=global_btn_color.get())
    btn_lib_window.configure(fg_color=global_btn_color.get())
    try:
        size = int(scale_size.get())
        app.geometry(f"{size}x{size}")
    except ValueError:
        messagebox.showerror("Ошибка", "Масштаб должен быть числом!")

# --------------------- Функция смены языка --------------------- #
def toggle_language():
    global current_language
    current_language = "en" if current_language == "ru" else "ru"
    update_language()

def update_language():
    # Обновляем тексты на виджетах:
    app.title(translations[current_language]["title"])
    btn_open.configure(text=translations[current_language]["open_file"])
    btn_save.configure(text=translations[current_language]["save_file"])
    btn_run.configure(text=translations[current_language]["run_code"])
    btn_lib_window.configure(text=translations[current_language]["install_library"])
    bg_color_label.configure(text=f"{translations[current_language]['bg_color_label']} {global_bg_color.get()}")
    btn_choose_bg.configure(text=translations[current_language]["choose_bg"])
    btn_color_label.configure(text=f"{translations[current_language]['btn_color_label']} {global_btn_color.get()}")
    btn_choose_btn.configure(text=translations[current_language]["choose_btn"])
    scale_label.configure(text=translations[current_language]["scale_label"])
    btn_apply_settings.configure(text=translations[current_language]["apply"])
    btn_toggle_lang.configure(text=translations[current_language]["toggle_language"])

# --------------------- Создание основного окна --------------------- #
app = ctk.CTk()
app.title(translations[current_language]["title"])
app.geometry("600x500")

global_bg_color = tk.StringVar(app, value="#2C2C2C")
global_btn_color = tk.StringVar(app, value="#008CBA")

# --------------------- Поле для редактирования кода --------------------- #
text_area = ctk.CTkTextbox(app, wrap="word", width=550, height=250)
text_area.pack(expand=True, fill="both", padx=10, pady=10)

# --------------------- Кнопки для работы с файлом и запуска кода --------------------- #
btn_open = ctk.CTkButton(app, text=translations[current_language]["open_file"], command=open_file)
btn_open.pack(pady=5)
btn_save = ctk.CTkButton(app, text=translations[current_language]["save_file"], command=save_file)
btn_save.pack(pady=5)
btn_run = ctk.CTkButton(app, text=translations[current_language]["run_code"], command=run_code)
btn_run.pack(pady=5)
btn_lib_window = ctk.CTkButton(app, text=translations[current_language]["install_library"], command=open_library_window)
btn_lib_window.pack(pady=5)

# Добавляем кнопку переключения языка
btn_toggle_lang = ctk.CTkButton(app, text=translations[current_language]["toggle_language"], command=toggle_language)
btn_toggle_lang.pack(pady=5)

# --------------------- Блок настроек интерфейса --------------------- #
settings_frame = ctk.CTkFrame(app)
settings_frame.pack(pady=10)

bg_color_label = ctk.CTkLabel(settings_frame, text=f"{translations[current_language]['bg_color_label']} {global_bg_color.get()}")
bg_color_label.grid(row=0, column=0, padx=5, pady=5)
btn_choose_bg = ctk.CTkButton(settings_frame, text=translations[current_language]["choose_bg"], command=choose_bg_color)
btn_choose_bg.grid(row=0, column=1, padx=5, pady=5)

btn_color_label = ctk.CTkLabel(settings_frame, text=f"{translations[current_language]['btn_color_label']} {global_btn_color.get()}")
btn_color_label.grid(row=1, column=0, padx=5, pady=5)
btn_choose_btn = ctk.CTkButton(settings_frame, text=translations[current_language]["choose_btn"], command=choose_btn_color)
btn_choose_btn.grid(row=1, column=1, padx=5, pady=5)

scale_label = ctk.CTkLabel(settings_frame, text=translations[current_language]["scale_label"])
scale_label.grid(row=2, column=0, padx=5, pady=5)
scale_size = ctk.CTkEntry(settings_frame)
scale_size.insert(0, "600")
scale_size.grid(row=2, column=1, padx=5, pady=5)

btn_apply_settings = ctk.CTkButton(settings_frame, text=translations[current_language]["apply"], command=apply_settings)
btn_apply_settings.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# --------------------- Добавление watermark --------------------- #
watermark_label = ctk.CTkLabel(app,
                               text="© BeaverV000 team",
                               text_color="gray",
                               font=("Arial", 10))
watermark_label.place(relx=0.98, rely=0.98, anchor="se")

# --------------------- Запуск главного цикла приложения --------------------- #
app.mainloop()