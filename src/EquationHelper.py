import tkinter as tk
from tkinter import messagebox
import sympy as sp

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        # Язык по умолчанию – украинский; возможные варианты: "uk" или "en"
        self.language = "uk"
        # Словарь переводов
        self.translations = {
            "uk": {
                "title": "Професійний Калькулятор",
                "error_title": "Помилка",
                "error_no_equal": "Будь ласка, використовуйте знак '=' для рівнянь",
                "error_invalid": "Некоректне рівняння",
                "watermark": "© BeaverV000 team"
            },
            "en": {
                "title": "Professional Calculator",
                "error_title": "Error",
                "error_no_equal": "Please include '=' in the equation",
                "error_invalid": "Invalid Equation",
                "watermark": "© BeaverV000 team"
            }
        }
        # Настройка главного окна
        self.title(self.translations[self.language]["title"])
        self.geometry("400x600")
        self.configure(bg="#1e1e1e")  # Темный фон

        # Инициализация переменных калькулятора
        self.expression = ""
        self.variables = {'x': sp.Symbol('x'), 'y': sp.Symbol('y'), 'z': sp.Symbol('z')}

        # Меню для переключения языка
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language", menu=language_menu)
        language_menu.add_command(label="Українська", command=lambda: self.set_language("uk"))
        language_menu.add_command(label="English", command=lambda: self.set_language("en"))

        # Фрейм для отображения выражения (Entry)
        self.display_frame = tk.Frame(self, bg="#1e1e1e")
        self.display_frame.pack(pady=10)
        self.entry = tk.Entry(self.display_frame, width=30, borderwidth=5, font=("Arial", 16))
        self.entry.grid(row=0, column=0, padx=10, pady=10)

        # Фрейм для кнопок
        self.button_frame = tk.Frame(self, bg="#1e1e1e")
        self.button_frame.pack()
        self.create_buttons()

        # Добавляем watermark (водяной знак)
        self.watermark_label = tk.Label(self, 
                                        text=self.translations[self.language]["watermark"],
                                        font=("Arial", 10),
                                        fg="gray",
                                        bg="#1e1e1e")
        self.watermark_label.place(relx=0.98, rely=0.98, anchor="se")

    def create_buttons(self):
        # Список кнопок: (текст, строка, столбец, [опционально: colspan])
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('C', 5, 0), ('√', 5, 1), ('^', 5, 2), ('(', 5, 3),
            (')', 6, 0), ('x', 6, 1), ('y', 6, 2), ('z', 6, 3),
            ('Solve', 7, 0, 4)
        ]
        for btn in buttons:
            text, row, col = btn[0], btn[1], btn[2]
            colspan = btn[3] if len(btn) > 3 else 1
            button = tk.Button(self.button_frame, text=text, width=5 * colspan, height=2,
                               font=("Arial", 14),
                               command=lambda ch=text: self.on_button_click(ch))
            button.grid(row=row, column=col, columnspan=colspan, padx=3, pady=3)

    def on_button_click(self, char):
        if char == "Solve":
            try:
                if "=" not in self.expression:
                    messagebox.showerror(self.translations[self.language]["error_title"],
                                         self.translations[self.language]["error_no_equal"])
                    return
                left_expr, right_expr = self.expression.split("=")
                left_expr = sp.sympify(left_expr, locals=self.variables)
                right_expr = sp.sympify(right_expr, locals=self.variables)
                solutions = sp.solve(left_expr - right_expr, list(self.variables.values()))
                self.display_result(solutions)
            except Exception:
                messagebox.showerror(self.translations[self.language]["error_title"],
                                     self.translations[self.language]["error_invalid"])
        elif char == "C":
            self.clear_entry()
        else:
            self.expression += char
            self.update_entry()

    def display_result(self, result):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, str(result))
        self.expression = str(result)

    def clear_entry(self):
        self.entry.delete(0, tk.END)
        self.expression = ""

    def update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def set_language(self, lang):
        self.language = lang
        # Обновляем заголовок окна и watermark
        self.title(self.translations[self.language]["title"])
        self.watermark_label.config(text=self.translations[self.language]["watermark"])

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()