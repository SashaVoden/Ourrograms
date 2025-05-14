import tkinter as tk
from tkinter import ttk, messagebox
from sympy import symbols, Eq, solve

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        # Язык по умолчанию
        self.lang = "uk"
        self.translations = {
            "uk": {
                "title": "Професійний Калькулятор",
                "tab_simple": "Прості приклади",
                "tab_equation": "Рівняння",
                "simple_clear": "Очистити",
                "eq_solve": "Розв’язати",
                "eq_clear": "Очистити",
                "error": "Помилка"
            },
            "en": {
                "title": "Professional Calculator",
                "tab_simple": "Simple Examples",
                "tab_equation": "Equations",
                "simple_clear": "Clear",
                "eq_solve": "Solve",
                "eq_clear": "Clear",
                "error": "Error"
            }
        }

        self.configure(bg='#2e2e2e')
        self.geometry("500x600")
        self.title(self.translations[self.lang]["title"])

        # Меню для переключения языка
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language", menu=language_menu)
        language_menu.add_command(label="Українська", command=lambda: self.set_language("uk"))
        language_menu.add_command(label="English", command=lambda: self.set_language("en"))

        # Инициализация переменных для решения уравнений
        self.variables = {'x': symbols('x'), 'y': symbols('y'), 'z': symbols('z')}
        # Построение интерфейса
        self.create_widgets()

        # Добавляем watermark (водяной знак)
        self.watermark_label = tk.Label(self, text="© BeaverV000 team", bg='#2e2e2e', 
                                        fg='gray', font=("Arial", 10))
        self.watermark_label.place(relx=0.98, rely=0.98, anchor="se")

    def create_widgets(self):
        # Notebook для двух вкладок
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Создаем вкладку простых примеров; сохраняем ссылку в self.simple_tab
        self.simple_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.simple_tab, text=self.translations[self.lang]["tab_simple"])
        self.create_simple_calculator_tab()

        # Создаем вкладку уравнений; сохраняем ссылку в self.equation_tab
        self.equation_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.equation_tab, text=self.translations[self.lang]["tab_equation"])
        self.create_equation_solver_tab()

    def create_simple_calculator_tab(self):
        # Поле для ввода (результата)
        self.simple_entry = tk.Entry(self.simple_tab, font=("Arial", 24), bg='#3c3c3c', fg='white')
        self.simple_entry.pack(pady=10, padx=10, fill='x')
        self.simple_result = tk.Label(self.simple_tab, text="", font=("Arial", 24),
                                      bg='#2e2e2e', fg='white')
        self.simple_result.pack(pady=10)
        self.simple_buttons_frame = tk.Frame(self.simple_tab, bg='#2e2e2e')
        self.simple_buttons_frame.pack()

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        row = 0
        col = 0
        for button in buttons:
            action = lambda x=button: self.on_simple_button_click(x)
            tk.Button(self.simple_buttons_frame, text=button, command=action,
                      width=5, bg='#3c3c3c', fg='white').grid(row=row, column=col,
                                                               padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.simple_clear_button = tk.Button(self.simple_tab,
                                             text=self.translations[self.lang]["simple_clear"],
                                             command=self.clear_simple_entry,
                                             bg='#3c3c3c', fg='white')
        self.simple_clear_button.pack(pady=10)

    def on_simple_button_click(self, char):
        if char == '=':
            try:
                result = eval(self.simple_entry.get())
                self.simple_result.config(text=str(result))
            except Exception as e:
                self.simple_result.config(text=self.translations[self.lang]["error"])
                print(f"{self.translations[self.lang]['error']}: {e}")
        else:
            self.simple_entry.insert(tk.END, char)

    def clear_simple_entry(self):
        self.simple_entry.delete(0, tk.END)
        self.simple_result.config(text="")

    def create_equation_solver_tab(self):
        self.equation_entry = tk.Entry(self.equation_tab, font=("Arial", 24),
                                       bg='#3c3c3c', fg='white')
        self.equation_entry.pack(pady=10, padx=10, fill='x')
        self.equation_result = tk.Label(self.equation_tab, text="", font=("Arial", 24),
                                        bg='#2e2e2e', fg='white')
        self.equation_result.pack(pady=10)
        self.eq_solve_button = tk.Button(self.equation_tab,
                                         text=self.translations[self.lang]["eq_solve"],
                                         command=self.solve_equation,
                                         bg='#3c3c3c', fg='white')
        self.eq_solve_button.pack(pady=10)
        self.eq_clear_button = tk.Button(self.equation_tab,
                                         text=self.translations[self.lang]["eq_clear"],
                                         command=self.clear_equation_entry,
                                         bg='#3c3c3c', fg='white')
        self.eq_clear_button.pack(pady=10)

    def solve_equation(self):
        # Решение уравнения в формате "выражение=выражение"
        x, y, z = symbols('x y z')
        equation_text = self.equation_entry.get()
        try:
            lhs, rhs = equation_text.split('=')
            equation = Eq(eval(lhs), eval(rhs))
            solution = solve(equation, (x, y, z))
            self.equation_result.config(text=f"Решение: {solution}")
        except Exception as e:
            self.equation_result.config(text=self.translations[self.lang]["error"])
            print(f"{self.translations[self.lang]['error']}: {e}")

    def clear_equation_entry(self):
        self.equation_entry.delete(0, tk.END)
        self.equation_result.config(text="")

    def set_language(self, lang):
        self.lang = lang
        self.update_language()

    def update_language(self):
        # Обновляем заголовок окна
        self.title(self.translations[self.lang]["title"])
        # Обновляем названия вкладок
        self.notebook.tab(self.simple_tab, text=self.translations[self.lang]["tab_simple"])
        self.notebook.tab(self.equation_tab, text=self.translations[self.lang]["tab_equation"])
        # Обновляем тексты кнопок и меток в простом калькуляторе
        self.simple_clear_button.config(text=self.translations[self.lang]["simple_clear"])
        # Вкладка уравнений
        self.eq_solve_button.config(text=self.translations[self.lang]["eq_solve"])
        self.eq_clear_button.config(text=self.translations[self.lang]["eq_clear"])
        # Если необходимо, можно добавить обновление для ошибок или других сообщений

if __name__ == "__main__":
    try:
        app = Calculator()
        app.mainloop()
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")