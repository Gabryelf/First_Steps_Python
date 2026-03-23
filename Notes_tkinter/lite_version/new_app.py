import tkinter as tk
from app_notes.storage import load_notes, save_notes
from tkinter import scrolledtext, messagebox, simpledialog


notes = load_notes()
next_id = 1


def view_note():
    selection = listbox.curselection()

    if not selection:
        messagebox.showwarning("Внимание", "Сначала выберите заметку!")
        return

    selected_text = listbox.get(selection[0])

    note_id = int(selected_text.split(']')[0].strip('['))

    for note in notes:
        if note['id'] == note_id:
            # Создаем новое окно
            view_window = tk.Toplevel(root)
            view_window.title(f"Заметка: {note['title']}")
            view_window.geometry("400x300")

            # Текстовое поле с прокруткой
            text_area = scrolledtext.ScrolledText(view_window, wrap=tk.WORD)
            text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_area.insert(tk.END, f"Заголовок: {note['title']}\n\n{note['content']}")
            text_area.config(state=tk.DISABLED)  # Запрещаем редактирование

            tk.Button(view_window, text="Закрыть", command=view_window.destroy).pack(pady=5)
            break


def show_all_notes():
    listbox.delete(0, tk.END)

    if not notes:
        listbox.insert(tk.END, "--- У вас пока нет заметок ---")
    else:
        for note in notes:
            listbox.insert(tk.END, f"[{note['id']}] {note['title']}")


def add_note():
    global next_id

    title = simpledialog.askstring("Новая заметка", "Заголовок:")
    if not title:
        return

    content = simpledialog.askstring("Новая заметка", "Содержание:")
    if content is None:
        return

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


def delete_note():
    global next_id
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Внимание", "Сначала выберите заметку!")
        return

    selected_text = listbox.get(selection[0])

    note_id = int(selected_text.split(']')[0].strip('['))

    for note in notes:
        if note['id'] == note_id:
            # Диалог подтверждения
            if messagebox.askyesno("Подтверждение", f"Удалить '{note['title']}'?"):
                notes.pop(note_id - 1)
                save_notes(notes)
                next_id -= 1
                show_all_notes()
                messagebox.showinfo("Успех", "✓ Заметка удалена!")
            break


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

# Показываем заметки при запуске
show_all_notes()

# Запускаем приложение
root.mainloop()
