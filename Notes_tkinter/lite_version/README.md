
## 1. **Импорт модулей**

```python
import tkinter as tk
from app_notes.storage import load_notes, save_notes
from tkinter import scrolledtext, messagebox, simpledialog
```

- **`tkinter as tk`** - стандартная библиотека Python для GUI
- **`from app_notes.storage import load_notes, save_notes`** - импорт функций для работы с файлом заметок из собственного модуля
- **`scrolledtext`** - текстовое поле с полосой прокрутки
- **`messagebox`** - диалоговые окна (предупреждения, подтверждения, информация)
- **`simpledialog`** - простые диалоги для ввода данных

## 2. **Глобальные переменные**

```python
notes = load_notes()
next_id = 1
```

- **`notes`** - список всех заметок, загруженных из файла при старте
- **`next_id`** - следующий доступный ID для новой заметки (начинается с 1)

## 3. **Функция просмотра заметки**

```python
def view_note():
    selection = listbox.curselection()
```
- `curselection()` - возвращает кортеж с индексами выбранных элементов
- Если ничего не выбрано, кортеж пустой

```python
    if not selection:
        messagebox.showwarning("Внимание", "Сначала выберите заметку!")
        return
```
- Проверка: выбрана ли заметка
- `showwarning()` - показывает предупреждающее окно

```python
    selected_text = listbox.get(selection[0])
    note_id = int(selected_text.split(']')[0].strip('['))
```
- `listbox.get(индекс)` - получает текст выбранного элемента
- Пример: `"[1] Купить хлеб"` → split(']') → `["[1", " Купить хлеб"]`
- `strip('[')` - убирает открывающую скобку → `"1"`
- Преобразуем в число → `1`

```python
    for note in notes:
        if note['id'] == note_id:
            # Создаем новое окно
            view_window = tk.Toplevel(root)
            view_window.title(f"Заметка: {note['title']}")
            view_window.geometry("400x300")
```
- Ищем заметку с нужным ID
- `Toplevel()` - создает дополнительное окно поверх главного
- Устанавливаем заголовок и размер окна

```python
            # Текстовое поле с прокруткой
            text_area = scrolledtext.ScrolledText(view_window, wrap=tk.WORD)
            text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_area.insert(tk.END, f"Заголовок: {note['title']}\n\n{note['content']}")
            text_area.config(state=tk.DISABLED)  # Запрещаем редактирование
```
- `ScrolledText` - текстовое поле с автоматической прокруткой
- `wrap=tk.WORD` - перенос слов целиком
- `fill=tk.BOTH, expand=True` - растягивается во все стороны
- `insert()` - вставляем текст
- `config(state=tk.DISABLED)` - делаем поле только для чтения

```python
            tk.Button(view_window, text="Закрыть", command=view_window.destroy).pack(pady=5)
            break
```
- Кнопка закрытия окна
- `destroy()` - закрывает окно

## 4. **Функция показа всех заметок**

```python
def show_all_notes():
    listbox.delete(0, tk.END)
```
- `delete(0, tk.END)` - очищает весь список (с первого до последнего элемента)

```python
    if not notes:
        listbox.insert(tk.END, "--- У вас пока нет заметок ---")
    else:
        for note in notes:
            listbox.insert(tk.END, f"[{note['id']}] {note['title']}")
```
- Если заметок нет, выводим сообщение
- Иначе добавляем каждую заметку в формате `"[ID] Заголовок"`

## 5. **Функция добавления заметки**

```python
def add_note():
    global next_id
```
- `global next_id` - указываем, что используем глобальную переменную

```python
    title = simpledialog.askstring("Новая заметка", "Заголовок:")
    if not title:
        return
```
- `askstring()` - диалоговое окно с полем ввода
- Возвращает введенную строку или None при отмене
- Если заголовок не введен или нажата отмена, выходим

```python
    content = simpledialog.askstring("Новая заметка", "Содержание:")
    if content is None:
        return
```
- Запрашиваем содержимое заметки
- `None` - если нажата отмена

```python
    note = {
        'id': next_id,
        'title': title,
        'content': content
    }
    
    notes.append(note)
    next_id += 1
    save_notes(notes)
    show_all_notes()
    messagebox.showinfo("Успех", "✓ Заметка добавлена!")
```
- Создаем словарь заметки
- Добавляем в список
- Увеличиваем счетчик ID
- Сохраняем в файл
- Обновляем список на экране
- Показываем сообщение об успехе

## 6. **Функция удаления заметки**

```python
def delete_note():
    global next_id
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Внимание", "Сначала выберите заметку!")
        return
```
- Аналогично проверяем, выбрана ли заметка

```python
    selected_text = listbox.get(selection[0])
    note_id = int(selected_text.split(']')[0].strip('['))
```
- Извлекаем ID заметки из выбранного элемента

```python
    for note in notes:
        if note['id'] == note_id:
            if messagebox.askyesno("Подтверждение", f"Удалить '{note['title']}'?"):
                notes.pop(note_id - 1)
                save_notes(notes)
                next_id -= 1
                show_all_notes()
                messagebox.showinfo("Успех", "✓ Заметка удалена!")
            break
```
- `askyesno()` - диалог с кнопками Да/Нет
- `pop(note_id - 1)` - удаляем элемент по индексу (индексация с 0, ID с 1)
- Уменьшаем `next_id` (⚠️ **потенциальная проблема!**)
- Сохраняем и обновляем список

## 7. **Создание графического интерфейса**

```python
# Создаем главное окно
root = tk.Tk()
root.title("МОИ ЗАМЕТКИ")
root.geometry("600x450")

# Создаем список заметок
listbox = tk.Listbox(root, height=15, font=("Arial", 10))
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Создаем фрейм для кнопок
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Создаем кнопки
tk.Button(button_frame, text="1. Показать все", command=show_all_notes, width=15).pack(side=tk.LEFT, padx=2)
tk.Button(button_frame, text="2. Добавить", command=add_note, width=15).pack(side=tk.LEFT, padx=2)
tk.Button(button_frame, text="3. Посмотреть", command=view_note, width=15).pack(side=tk.LEFT, padx=2)
tk.Button(button_frame, text="4. Удалить", command=delete_note, width=15).pack(side=tk.LEFT, padx=2)
tk.Button(button_frame, text="0. Выход", command=root.quit, width=15).pack(side=tk.LEFT, padx=2)
```
- Создаем все элементы интерфейса (аналогично предыдущему примеру)

```python
# Показываем заметки при запуске
show_all_notes()

# Запускаем приложение
root.mainloop()
```

## **Проблемы в коде:**

### 1. **Проблема с удалением заметок**
```python
notes.pop(note_id - 1)  # ⚠️ ОПАСНО!
```
**Почему проблема:**
- Если ID не совпадают с индексами (например, после удаления заметки с ID=2, заметка с ID=3 становится на индекс 1)
- После удаления ID становятся несвязными

**Правильное решение:**
```python
# Удаляем по ID, а не по индексу
notes = [note for note in notes if note['id'] != note_id]
```

### 2. **Проблема с next_id**
```python
next_id -= 1  # ⚠️ НЕПРАВИЛЬНО!
```
- При удалении заметки из середины, next_id уменьшается только на 1
- Должен быть равен `max(note['id'] for note in notes) + 1` после удаления

**Исправление:**
```python
def delete_note():
    # ... код ...
    notes = [note for note in notes if note['id'] != note_id]
    # Пересчитываем next_id
    global next_id
    next_id = max([note['id'] for note in notes], default=0) + 1
    save_notes(notes)
    show_all_notes()
```

### 3. **Улучшенная версия функции удаления:**
```python
def delete_note():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Внимание", "Сначала выберите заметку!")
        return
    
    selected_text = listbox.get(selection[0])
    note_id = int(selected_text.split(']')[0].strip('['))
    
    # Находим заметку по ID
    note_to_delete = None
    for note in notes:
        if note['id'] == note_id:
            note_to_delete = note
            break
    
    if note_to_delete:
        if messagebox.askyesno("Подтверждение", f"Удалить '{note_to_delete['title']}'?"):
            # Удаляем заметку из списка
            global notes, next_id
            notes = [note for note in notes if note['id'] != note_id]
            
            # Пересчитываем next_id
            if notes:
                next_id = max(note['id'] for note in notes) + 1
            else:
                next_id = 1
            
            save_notes(notes)
            show_all_notes()
            messagebox.showinfo("Успех", "✓ Заметка удалена!")
```

## **Структура файлов:**
```
project/
├── app.py              # Главный файл с GUI
└── app_notes/
    ├── __init__.py
    └── storage.py      # Модуль для работы с файлом
```

## **storage.py (пример):**
```python
import json
import os

NOTES_FILE = 'notes.json'

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
```

## **Визуальная схема работы:**
```
┌──────────────────────────────────────┐
│  МОИ ЗАМЕТКИ                    _ □ X │
├──────────────────────────────────────┤
│  [1] Купить хлеб                    │
│  [2] Позвонить маме                 │ ← listbox
│  [3] Сделать домашку                │
├──────────────────────────────────────┤
│  [1.Показать] [2.Добавить] [3.П...] │
└──────────────────────────────────────┘

При нажатии "3. Посмотреть":
┌─────────────────┐
│ Заметка: Купить │
├─────────────────┤
│ Заголовок:      │
│ Купить хлеб     │
│                 │
│ Содержание:     │ ← ScrolledText
│ Купить белый    │
│ и черный хлеб   │
│                 │
│    [Закрыть]    │
└─────────────────┘
```
