import tkinter as tk
import re
from tkinter import colorchooser

class GridPlotter:
    def __init__(self, root):
        self.root = root

        # Язык по умолчанию — украинский ("uk")
        self.current_language = "uk"
        self.translations = {
            "uk": {
                "title": "Координатна сітка",
                "entry_label": "Введіть координати (x,y):",
                "button_add": "Додати точки",
                "button_draw": "Побудувати лінії",
                "button_clear_all": "Видалити все",
                "button_theme_dark": "Темний режим",
                "button_theme_light": "Світлий режим",
                "button_bg_color": "Колір фону",
                "button_line_color": "Колір ліній",
                "button_point_color": "Колір точок",
                "lang_button": "English"
            },
            "en": {
                "title": "Coordinate Grid",
                "entry_label": "Enter coordinates (x,y):",
                "button_add": "Add Points",
                "button_draw": "Draw Lines",
                "button_clear_all": "Clear All",
                "button_theme_dark": "Dark Mode",
                "button_theme_light": "Light Mode",
                "button_bg_color": "Background Color",
                "button_line_color": "Line Color",
                "button_point_color": "Point Color",
                "lang_button": "Українська"
            }
        }

        # Устанавливаем заголовок и размеры окна
        self.root.title(self.translations[self.current_language]["title"])
        self.grid_size = 28                # Фиксированный размер сетки (28x28)
        self.grid_spacing = 20             # Размер каждой клетки: 20 пикселей
        self.window_width = self.grid_size * self.grid_spacing
        self.window_height = self.grid_size * self.grid_spacing + 150  # место для кнопок
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        # Начальные настройки цветов и режима
        self.dark_mode = False
        self.bg_color = "white"
        self.grid_color = "gray"
        self.line_color = "blue"
        self.point_color = "red"

        # Canvas для рисования сетки и точек
        self.canvas = tk.Canvas(root, width=self.window_width, height=self.window_height - 150, bg=self.bg_color)
        self.canvas.pack()

        # Фрейм для кнопок и ввода
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        # Подсказка для ввода координат
        self.entry_label = tk.Label(self.button_frame,
                                    text=self.translations[self.current_language]["entry_label"])
        self.entry_label.grid(row=0, column=0, columnspan=3)
        self.entry = tk.Entry(self.button_frame, width=40)
        self.entry.grid(row=1, column=0, columnspan=3)

        # Кнопки управления
        self.button_add = tk.Button(self.button_frame,
                                    text=self.translations[self.current_language]["button_add"],
                                    command=self.add_points)
        self.button_add.grid(row=2, column=0)
        self.button_draw = tk.Button(self.button_frame,
                                     text=self.translations[self.current_language]["button_draw"],
                                     command=self.draw_lines)
        self.button_draw.grid(row=2, column=1)
        self.button_clear_all = tk.Button(self.button_frame,
                                          text=self.translations[self.current_language]["button_clear_all"],
                                          command=self.clear_all)
        self.button_clear_all.grid(row=2, column=2)
        self.button_theme = tk.Button(self.button_frame,
                                      text=self.translations[self.current_language]["button_theme_dark"],
                                      command=self.toggle_theme)
        self.button_theme.grid(row=3, column=0)
        self.button_bg_color = tk.Button(self.button_frame,
                                         text=self.translations[self.current_language]["button_bg_color"],
                                         command=self.change_bg_color)
        self.button_bg_color.grid(row=3, column=1)
        self.button_line_color = tk.Button(self.button_frame,
                                           text=self.translations[self.current_language]["button_line_color"],
                                           command=self.change_line_color)
        self.button_line_color.grid(row=3, column=2)
        self.button_point_color = tk.Button(self.button_frame,
                                            text=self.translations[self.current_language]["button_point_color"],
                                            command=self.change_point_color)
        self.button_point_color.grid(row=4, column=1)
        
        # Кнопка переключения языка
        self.lang_button = tk.Button(self.button_frame,
                                     text=self.translations[self.current_language]["lang_button"],
                                     command=self.toggle_language)
        self.lang_button.grid(row=4, column=2)

        self.draw_grid()
        self.points = []

        # Добавляем watermark в нижнем правом углу
        self.watermark_label = tk.Label(self.root,
                                        text="© BeaverV000 team",
                                        font=("Arial", 10),
                                        fg="gray",
                                        bg=self.root["bg"])
        self.watermark_label.place(relx=0.98, rely=0.98, anchor="se")
        self.watermark_label.lift()

    def draw_grid(self):
        self.canvas.delete("grid")
        for x in range(0, self.window_width, self.grid_spacing):
            self.canvas.create_line(x, 0, x, self.window_height - 150, fill=self.grid_color, width=1, tags="grid")
        for y in range(0, self.window_height - 150, self.grid_spacing):
            self.canvas.create_line(0, y, self.window_width, y, fill=self.grid_color, width=1, tags="grid")
        self.canvas.create_line(self.window_width // 2, 0, self.window_width // 2, self.window_height - 150,
                                fill="black", width=2, tags="grid")
        self.canvas.create_line(0, (self.window_height - 150) // 2, self.window_width, (self.window_height - 150) // 2,
                                fill="black", width=2, tags="grid")

    def add_points(self):
        self.canvas.delete("points")
        self.points = []
        text = self.entry.get()
        coordinates = re.findall(r'\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)', text)
        for coord in coordinates:
            x, y = map(int, coord)
            if -self.grid_size // 2 <= x <= self.grid_size // 2 and -self.grid_size // 2 <= y <= self.grid_size // 2:
                screen_x = self.window_width // 2 + x * self.grid_spacing
                screen_y = (self.window_height - 150) // 2 - y * self.grid_spacing
                self.canvas.create_oval(screen_x - 3, screen_y - 3, screen_x + 3, screen_y + 3,
                                         fill=self.point_color, outline=self.point_color, tags="points")
                self.points.append((screen_x, screen_y))

    def draw_lines(self):
        self.canvas.delete("lines")
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                self.canvas.create_line(self.points[i][0], self.points[i][1],
                                        self.points[i+1][0], self.points[i+1][1],
                                        fill=self.line_color, width=2, tags="lines")

    def clear_all(self):
        self.entry.delete(0, tk.END)
        self.canvas.delete("points")
        self.canvas.delete("lines")
        self.points = []

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        # В зависимости от режима обновляем цвета и текст кнопки темы
        if self.dark_mode:
            self.bg_color = "black"
            self.grid_color = "white"
            self.button_theme.config(text=self.translations[self.current_language]["button_theme_light"])
        else:
            self.bg_color = "white"
            self.grid_color = "gray"
            self.button_theme.config(text=self.translations[self.current_language]["button_theme_dark"])
        self.canvas.config(bg=self.bg_color)
        self.draw_grid()

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            self.canvas.config(bg=self.bg_color)

    def change_line_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.line_color = color

    def change_point_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.point_color = color

    def toggle_language(self):
        # Переключаем язык: если сейчас "uk", то ставим "en", иначе "uk"
        self.current_language = "en" if self.current_language == "uk" else "uk"
        self.update_language()

    def update_language(self):
        # Обновляем заголовок окна
        self.root.title(self.translations[self.current_language]["title"])
        # Обновляем текст виджетов в button_frame
        self.entry_label.config(text=self.translations[self.current_language]["entry_label"])
        self.button_add.config(text=self.translations[self.current_language]["button_add"])
        self.button_draw.config(text=self.translations[self.current_language]["button_draw"])
        self.button_clear_all.config(text=self.translations[self.current_language]["button_clear_all"])
        # Текущее состояние dark_mode влияет на надпись кнопки темы
        if self.dark_mode:
            self.button_theme.config(text=self.translations[self.current_language]["button_theme_light"])
        else:
            self.button_theme.config(text=self.translations[self.current_language]["button_theme_dark"])
        self.button_bg_color.config(text=self.translations[self.current_language]["button_bg_color"])
        self.button_line_color.config(text=self.translations[self.current_language]["button_line_color"])
        self.button_point_color.config(text=self.translations[self.current_language]["button_point_color"])
        self.lang_button.config(text=self.translations[self.current_language]["lang_button"])
        # Обновляем заголовок окна в случае необходимости
        self.root.title(self.translations[self.current_language]["title"])

if __name__ == "__main__":
    root = tk.Tk()
    app = GridPlotter(root)
    root.mainloop()
