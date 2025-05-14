import tkinter as tk
from tkinter import colorchooser
import matplotlib.pyplot as plt
import numpy as np
import re

class BarChartApp:
    def __init__(self, root):
        self.root = root

        # Изначальный язык – украинский ("uk") 
        self.current_language = "uk"
        self.translations = {
            "uk": {
                "title": "Барна діаграма",
                "num_bars_label": "Кількість колонок:",
                "create_button": "Створити",
                "preview_label": "Попередній перегляд:",
                "save_button": "Зберегти JPG",
                "bar_name": "Назва:",
                "bar_value": "Значення:",
                "color_button": "Колір",
                "lang_button": "English"
            },
            "en": {
                "title": "Bar Chart",
                "num_bars_label": "Number of Bars:",
                "create_button": "Create",
                "preview_label": "Preview:",
                "save_button": "Save JPG",
                "bar_name": "Name:",
                "bar_value": "Value:",
                "color_button": "Color",
                "lang_button": "Українська"
            }
        }

        self.root.title(self.translations[self.current_language]["title"])
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")

        # Верхняя панель
        top_frame = tk.Frame(root, bg="#f0f0f0")
        top_frame.pack(pady=10)
        
        self.num_bars_label = tk.Label(top_frame, 
                                       text=self.translations[self.current_language]["num_bars_label"],
                                       font=("Arial", 12),
                                       bg="#f0f0f0")
        self.num_bars_label.pack(side=tk.LEFT, padx=5)
        
        self.num_bars_entry = tk.Entry(top_frame, font=("Arial", 12), width=5)
        self.num_bars_entry.pack(side=tk.LEFT, padx=5)
        
        self.create_bars_button = tk.Button(top_frame, 
                                            text=self.translations[self.current_language]["create_button"],
                                            font=("Arial", 12),
                                            command=self.create_bars)
        self.create_bars_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопка переключения языка
        self.lang_button = tk.Button(top_frame,
                                     text=self.translations[self.current_language]["lang_button"],
                                     font=("Arial", 12),
                                     command=self.toggle_language)
        self.lang_button.pack(side=tk.RIGHT, padx=10)
        
        # Фрейм для ввода данных по каждому столбцу
        self.bars_frame = tk.Frame(root, bg="#f0f0f0")
        self.bars_frame.pack(pady=10)
        
        # Фрейм для предварительного просмотра диаграммы
        preview_frame = tk.Frame(root, bg="#f0f0f0")
        preview_frame.pack(pady=10)
        
        self.preview_label = tk.Label(preview_frame, 
                                      text=self.translations[self.current_language]["preview_label"],
                                      font=("Arial", 12),
                                      bg="#f0f0f0")
        self.preview_label.pack()
        
        self.preview_canvas = tk.Canvas(preview_frame, width=500, height=350, bg="white", bd=2, relief="sunken")
        self.preview_canvas.pack(pady=5)
        
        # Кнопка сохранения диаграммы
        self.save_button = tk.Button(root,
                                     text=self.translations[self.current_language]["save_button"],
                                     font=("Arial", 12),
                                     command=self.save_chart)
        self.save_button.pack(pady=10)
        
        # Инициализация списков для динамически создаваемых элементов
        self.bar_entries = []
        self.value_entries = []
        self.color_buttons = []
        self.bar_colors = []  # Значения по умолчанию
        
        # Добавляем watermark
        self.watermark_label = tk.Label(root,
                                        text="© BeaverV000 team",
                                        font=("Arial", 10),
                                        fg="gray",
                                        bg="#f0f0f0")
        self.watermark_label.place(relx=0.98, rely=0.98, anchor="se")
    
    def toggle_language(self):
        # Переключаем язык между украинским и английским
        self.current_language = "en" if self.current_language == "uk" else "uk"
        self.update_language()
        
    def update_language(self):
        # Обновляем тексты на всех основных виджетах
        self.root.title(self.translations[self.current_language]["title"])
        self.num_bars_label.config(text=self.translations[self.current_language]["num_bars_label"])
        self.create_bars_button.config(text=self.translations[self.current_language]["create_button"])
        self.preview_label.config(text=self.translations[self.current_language]["preview_label"])
        self.save_button.config(text=self.translations[self.current_language]["save_button"])
        self.lang_button.config(text=self.translations[self.current_language]["lang_button"])
        
        # Если уже созданы настройки для столбцов, обновляем заголовки
        for widget in self.bars_frame.winfo_children():
            widget.destroy()
        # Если пользователь уже ввёл число столбцов, можно пересоздать
        if self.num_bars_entry.get().isdigit():
            self.create_bars()
    
    def create_bars(self):
        # Очищаем фрейм для настроек
        for widget in self.bars_frame.winfo_children():
            widget.destroy()
        
        try:
            num_bars = int(self.num_bars_entry.get())
        except ValueError:
            num_bars = 0
        
        self.bar_entries = []
        self.value_entries = []
        self.color_buttons = []
        self.bar_colors = [ "#3498db" ] * num_bars
        
        # Заголовки
        header_name = tk.Label(self.bars_frame, 
                               text=self.translations[self.current_language]["bar_name"],
                               font=("Arial", 12), bg="#f0f0f0")
        header_name.grid(row=0, column=0, padx=5, pady=5)
        header_value = tk.Label(self.bars_frame, 
                                text=self.translations[self.current_language]["bar_value"],
                                font=("Arial", 12), bg="#f0f0f0")
        header_value.grid(row=0, column=1, padx=5, pady=5)
        header_color = tk.Label(self.bars_frame, 
                                text=self.translations[self.current_language]["color_button"],
                                font=("Arial", 12), bg="#f0f0f0")
        header_color.grid(row=0, column=2, padx=5, pady=5)
        
        # Создаем строки для каждого столбца
        for i in range(num_bars):
            # Поле для ввода имени
            label = tk.Label(self.bars_frame,
                             text=f"{self.translations[self.current_language]['bar_name']} {i+1}:",
                             font=("Arial", 10),
                             bg="#f0f0f0")
            label.grid(row=i+1, column=0, padx=5, pady=3, sticky="e")
            bar_entry = tk.Entry(self.bars_frame, font=("Arial", 10))
            bar_entry.grid(row=i+1, column=0, padx=5, pady=3, sticky="w")
            self.bar_entries.append(bar_entry)
            
            # Поле для ввода значения
            value_entry = tk.Entry(self.bars_frame, font=("Arial", 10), width=8)
            value_entry.grid(row=i+1, column=1, padx=5, pady=3)
            self.value_entries.append(value_entry)
            
            # Кнопка для выбора цвета
            color_button = tk.Button(self.bars_frame,
                                     text=self.translations[self.current_language]["color_button"],
                                     font=("Arial", 10),
                                     command=lambda i=i: self.choose_color(i))
            color_button.grid(row=i+1, column=2, padx=5, pady=3)
            self.color_buttons.append(color_button)
        
        self.update_chart()
    
    def choose_color(self, i):
        color = colorchooser.askcolor()[1]
        if color:
            self.bar_colors[i] = color
        self.update_chart()
    
    def update_chart(self):
        self.preview_canvas.delete("all")
        labels = [entry.get() for entry in self.bar_entries]
        values = []
        for entry in self.value_entries:
            try:
                value = float(entry.get())
            except ValueError:
                value = 0
            values.append(value)
        
        max_value = max(values, default=100)
        bar_width = 40
        spacing = 60
        
        for i, (label, value, color) in enumerate(zip(labels, values, self.bar_colors)):
            x = i * spacing + 50
            y = 280 - (value / max_value * 250) if max_value != 0 else 280
            self.preview_canvas.create_rectangle(x, y, x + bar_width, 280, fill=color, outline=color)
            self.preview_canvas.create_text(x + bar_width / 2, y - 10, text=str(value), font=("Arial", 10))
            self.preview_canvas.create_text(x + bar_width / 2, 290, text=label, font=("Arial", 10))
        
        for y in range(280, 20, -50):
            self.preview_canvas.create_line(30, y, 400, y, dash=(4, 2), fill="gray")
            self.preview_canvas.create_text(15, y, text=str(int((280 - y) / 250 * max_value)), font=("Arial", 10))
    
    def save_chart(self):
        labels = [entry.get() for entry in self.bar_entries]
        try:
            values = [float(entry.get()) for entry in self.value_entries]
        except ValueError:
            values = [0] * len(self.value_entries)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(labels, values, color=self.bar_colors)
        ax.set_ylabel("Кількість", fontsize=12)
        ax.set_title(self.translations[self.current_language]["title"], fontsize=14)
        ax.grid(axis='y', linestyle='--', linewidth=0.7)
        if values:
            ax.set_yticks(np.arange(0, max(values) + 20, 20))
        
        plt.savefig("barchart.jpg")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BarChartApp(root)
    root.mainloop()