import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Создаем главное окно
root = tk.Tk()
root.title("Weather Diary")

# Поля для ввода
tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
date_var = tk.StringVar()
entry_date = tk.Entry(root, textvariable=date_var)
entry_date.grid(row=0, column=1)

tk.Label(root, text="Температура (°C):").grid(row=1, column=0)
temp_var = tk.StringVar()
entry_temp = tk.Entry(root, textvariable=temp_var)
entry_temp.grid(row=1, column=1)

tk.Label(root, text="Описание погоды:").grid(row=2, column=0)
desc_var = tk.StringVar()
entry_desc = tk.Entry(root, textvariable=desc_var)
entry_desc.grid(row=2, column=1)

rain_var = tk.BooleanVar()
checkbox_rain = tk.Checkbutton(root, text="Осадки", variable=rain_var)
checkbox_rain.grid(row=3, column=0, columnspan=2)

# Таблица для отображения записей
columns = ("дата", "температура", "описание", "осадки")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.grid(row=5, column=0, columnspan=2)

# Функция добавления записи
def add_record():
    date_str = date_var.get()
    temp_str = temp_var.get()
    desc = desc_var.get()
    rain = rain_var.get()
    
    # Проверка корректности
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат даты")
        return
    try:
        temperature = float(temp_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Температура должна быть числом")
        return
    if not desc:
        messagebox.showerror("Ошибка", "Описание не может быть пустым")
        return
    
    # Добавляем в таблицу
    tree.insert("", "end", values=(date_str, temperature, desc, rain))
    # Очистка полей
    date_var.set("")
    temp_var.set("")
    desc_var.set("")
    rain_var.set(False)

tk.Button(root, text="Добавить запись", command=add_record).grid(row=4, column=0, columnspan=2)

#добавление фильтров
def filter_by_temp():
    threshold = 10  # Например, показывать выше +10°C
    for item in tree.get_children():
        values = tree.item(item, "values")
        temp = float(values[1])
        if temp > threshold:
            tree.reattach(item, '', 'end')
        else:
            tree.detach(item)

#сохранение и загрузка
def save_to_json():
    data = []
    for item in tree.get_children():
        data.append(tree.item(item)['values'])
    with open('weather_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json():
    try:
        with open('weather_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for row in data:
            tree.insert("", "end", values=row)
    except FileNotFoundError:
        pass

tk.Button(root, text="Сохранить", command=save_to_json).grid(row=6, column=0)
tk.Button(root, text="Загрузить", command=load_from_json).grid(row=6, column=1)
