import tkinter as tk
import re

class GridPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Графік зі шкалою")
        self.window_width = 600
        self.window_height = 500
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        # Поточна мова
        self.current_language = "uk"
        self.translations = {
            "uk": {
                "title": "Графік зі шкалою",
                "scale_x_label": "Шкала X (тільки +):",
                "scale_y_label": "Шкала Y (+ і -):",
                "entry_label": "Введіть координати (x,y):",
                "button_add": "Додати точки",
                "button_connect": "З'єднати всі точки",
                "lang_button": "English"
            },
            "en": {
                "title": "Scale Graph",
                "scale_x_label": "Scale X (only +):",
                "scale_y_label": "Scale Y (+ and -):",
                "entry_label": "Enter coordinates (x,y):",
                "button_add": "Add points",
                "button_connect": "Connect all points",
                "lang_button": "Українська"
            }
        }

        # Фрейм для елементів керування
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        # Введення шкали X і Y
        tk.Label(self.button_frame, text=self.translations[self.current_language]["scale_x_label"]).grid(row=0, column=0)
        self.scale_x_entry = tk.Entry(self.button_frame, width=5)
        self.scale_x_entry.grid(row=0, column=1)

        tk.Label(self.button_frame, text=self.translations[self.current_language]["scale_y_label"]).grid(row=0, column=2)
        self.scale_y_entry = tk.Entry(self.button_frame, width=5)
        self.scale_y_entry.grid(row=0, column=3)

        # Поле для введення координат
        tk.Label(self.button_frame, text=self.translations[self.current_language]["entry_label"]).grid(row=1, column=0, columnspan=4)
        self.entry = tk.Entry(self.button_frame, width=40)
        self.entry.grid(row=2, column=0, columnspan=4)

        # Кнопка для додавання точок
        self.button_add = tk.Button(self.button_frame, text=self.translations[self.current_language]["button_add"], command=self.add_points)
        self.button_add.grid(row=3, column=0, columnspan=4)

        # Кнопка для з'єднання точок лінією
        self.connect_all_button = tk.Button(self.button_frame, text=self.translations[self.current_language]["button_connect"], command=self.draw_path_through_all_points)
        self.connect_all_button.grid(row=4, column=0, columnspan=4)

        # Кнопка для перемикання мови
        self.lang_button = tk.Button(self.button_frame, text=self.translations[self.current_language]["lang_button"], command=self.toggle_language)
        self.lang_button.grid(row=5, column=0, columnspan=4)

        # Canvas для малювання
        self.canvas = tk.Canvas(root, width=self.window_width, height=self.window_height-150, bg="white")
        self.canvas.pack()

        self.points = []

    def toggle_language(self):
        self.current_language = "en" if self.current_language == "uk" else "uk"
        self.update_language()

    def update_language(self):
        self.root.title(self.translations[self.current_language]["title"])
        self.button_add.config(text=self.translations[self.current_language]["button_add"])
        self.connect_all_button.config(text=self.translations[self.current_language]["button_connect"])
        self.lang_button.config(text=self.translations[self.current_language]["lang_button"])

    def add_points(self):
        self.canvas.delete("all")
        self.points = []

        scale_x = int(self.scale_x_entry.get()) if self.scale_x_entry.get().isdigit() else 10
        scale_y = int(self.scale_y_entry.get()) if self.scale_y_entry.get().isdigit() else 10

        center_x = 50  
        center_y = (self.window_height - 150) // 2  

        # Ось X тепер проходит по `y = 0`
        self.canvas.create_line(center_x, center_y, self.window_width - 50, center_y, arrow=tk.LAST)
        self.canvas.create_line(center_x, self.window_height - 150, center_x, 50, arrow=tk.BOTH)

        # Додавання чисел під ось X
        for i in range(scale_x + 1):  
            x_pos = center_x + (i * (500 // scale_x))
            self.canvas.create_line(x_pos, center_y, x_pos, 50, dash=(2, 2))
            self.canvas.create_text(x_pos, center_y + 15, text=str(i))  # Числа розташовані під ось X

        for j in range(-scale_y, scale_y + 1):  
            y_pos = center_y - (j * (300 // (2 * scale_y)))
            self.canvas.create_line(center_x, y_pos, self.window_width - 50, y_pos, dash=(2, 2))
            self.canvas.create_text(center_x - 10, y_pos, text=str(j))

        text = self.entry.get()
        coordinates = re.findall(r'\(\s*(\d+)\s*,\s*(-?\d+)\s*\)', text)

        for coord in coordinates:
            x, y = map(int, coord)
            if 0 <= x <= scale_x and -scale_y <= y <= scale_y:
                screen_x = center_x + (x * (500 // scale_x))
                screen_y = center_y - (y * (300 // (2 * scale_y)))

                self.canvas.create_oval(screen_x - 3, screen_y - 3, screen_x + 3, screen_y + 3,
                                         fill="red", outline="red")
                self.points.append((screen_x, screen_y))

    def draw_path_through_all_points(self):
        if len(self.points) < 2:
            return
        
        sorted_points = sorted(self.points, key=lambda p: p[0])

        for i in range(len(sorted_points) - 1):
            self.canvas.create_line(
                sorted_points[i][0], sorted_points[i][1],
                sorted_points[i+1][0], sorted_points[i+1][1],
                fill="blue", width=2
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = GridPlotter(root)
    root.mainloop()
