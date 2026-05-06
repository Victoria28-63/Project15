import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os

# Настройки
HISTORY_FILE = "history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32

# Логика генерации пароля
def generate_password(length, use_digits, use_letters, use_special):
    """Генерирует пароль на основе выбранных параметров."""
    if length < MIN_LENGTH:
        raise ValueError(f"Длина пароля должна быть не менее {MIN_LENGTH} символов.")
    if length > MAX_LENGTH:
        raise ValueError(f"Длина пароля не может превышать {MAX_LENGTH} символов.")

    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_special:
        chars += string.punctuation

    if not chars:
        raise ValueError("Необходимо выбрать хотя бы один тип символов.")

    return ''.join(random.choices(chars, k=length))

# Работа с историей
def load_history():
    """Загружает историю из файла."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю в файл."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Обработчики интерфейса
def on_generate():
    try:
        length = scale_length.get()

        # Проверка длины
        if length < MIN_LENGTH or length > MAX_LENGTH:
            messagebox.showerror("Ошибка ввода",
                               f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH} символов." )
            return

        # Получение флагов выбора символов
        use_digits = var_digits.get()
        use_letters = var_letters.get()
        use_special = var_special.get()

        # Генерация пароля
        password = generate_password(length, use_digits, use_letters, use_special)

        # Вывод в интерфейс
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)

        # Сохранение в историю и обновление таблицы
        history = load_history()
        history.append(password)
        save_history(history)
        update_history_table()

    except ValueError as e:
        messagebox.showerror("Ошибка ввода", str(e))
    except Exception as e:
        messagebox.showerror("Критическая ошибка", "Произошла непредвиденная ошибка.")

def update_history_table():
    """Обновляет виджет таблицы с историей."""
    for item in tree.get_children():
        tree.delete(item)
    for pwd in load_history():
        tree.insert('', 'end', values=(pwd,))

# Создание графического интерфейса
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("500x450")
root.resizable(False, False)
root.configure(bg='#f0f0f0')

# Фрейм настроек (Длина и флажки)
frame_settings = tk.Frame(root, bg='#f0f0f0', padx=10, pady=10)
frame_settings.pack(pady=10)

tk.Label(frame_settings, text="Длина пароля:", bg='#f0f0f0').grid(row=0, column=0)
scale_length = tk.Scale(frame_settings, from_=MIN_LENGTH, to=MAX_LENGTH,
                         orient=tk.HORIZONTAL, length=250)
scale_length.set(12)  # Значение по умолчанию
scale_length.grid(row=0, column=1, columnspan=2)

var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=False)

tk.Checkbutton(frame_settings, text="Цифры", variable=var_digits,
              bg='#f0f0f0').grid(row=1, column=0, sticky='w')
tk.Checkbutton(frame_settings, text="Буквы", variable=var_letters,
              bg='#f0f0f0').grid(row=2, column=0, sticky='w')
tk.Checkbutton(frame_settings, text="Спецсимволы", variable=var_special,
              bg='#f0f0f0').grid(row=3, column=0, sticky='w')

# Поле вывода пароля
frame_output = tk.Frame(root, bg='#f0f0f0', padx=10, pady=5)
frame_output.pack(fill='x')

tk.Label(frame_output, text="Сгенерированный пароль:", bg='#f0f0f0').pack(anchor='w')
entry_password = tk.Entry(frame_output, width=50, font=('Arial', 10))
entry_password.pack(fill='x', pady=5)

# Кнопка генерации
btn_generate = tk.Button(root, text="Сгенерировать пароль", command=on_generate,
                       bg='#4CAF50', fg='white', font=('Arial', 12))
btn_generate.pack(pady=10)

# Таблица истории
frame_history = tk.LabelFrame(root, text="История паролей", padx=10, pady=10, bg='#f0f0f0')
frame_history.pack(fill='both', expand=True, padx=10, pady=10)

tree = ttk.Treeview(frame_history, columns=('password',), show='headings')
tree.heading('password', text='История паролей')
tree.column('password', width=450)
tree.pack(fill='both', expand=True)

scrollbar = ttk.Scrollbar(frame_history, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Загрузка истории при запуске приложения
update_history_table()

root.mainloop()
