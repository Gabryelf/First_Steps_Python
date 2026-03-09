from app import *
import tkinter as tk
from tkinter import messagebox, scrolledtext


class GUIApp:
    """Графический интерфейс с tkinter"""

    def __init__(self, root):
        self.root = root
        self.root.title("Мои Заметки")
        self.root.geometry("600x500")

        # Используем тот же менеджер, что и в консольной версии!
        self.manager = NoteManager()
        self.current_note = None  # для отслеживания выбранной заметки

        # Создаем интерфейс
        self.create_widgets()

        # Показываем список заметок при запуске
        self.refresh_notes_list()

    def create_widgets(self):
        """Создание всех элементов интерфейса"""

        # === Верхняя панель с кнопками ===
        toolbar = tk.Frame(self.root, bg="#f0f0f0", height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопки
        btn_new = tk.Button(toolbar, text="➕ Новая", command=self.new_note)
        btn_new.pack(side=tk.LEFT, padx=2, pady=5)

        btn_save = tk.Button(toolbar, text="💾 Сохранить", command=self.save_note)
        btn_save.pack(side=tk.LEFT, padx=2, pady=5)

        btn_delete = tk.Button(toolbar, text="🗑 Удалить", command=self.delete_note)
        btn_delete.pack(side=tk.LEFT, padx=2, pady=5)

        # === Основная область ===
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Левая панель - список заметок
        left_frame = tk.Frame(main_frame, width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_frame.pack_propagate(False)  # фиксируем ширину

        tk.Label(left_frame, text="Список заметок:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

        # Список с прокруткой
        list_frame = tk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notes_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.notes_listbox.yview)

        # Привязываем выбор элемента
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)

        # Правая панель - редактирование заметки
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Заголовок
        tk.Label(right_frame, text="Заголовок:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.title_entry = tk.Entry(right_frame, font=("Arial", 12))
        self.title_entry.pack(fill=tk.X, pady=(0, 5))

        # Содержание
        tk.Label(right_frame, text="Содержание:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=15)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # Статус бар
        self.status_bar = tk.Label(self.root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def refresh_notes_list(self):
        """Обновить список заметок"""
        self.notes_listbox.delete(0, tk.END)
        notes = self.manager.get_all_notes()

        for note in notes:
            self.notes_listbox.insert(tk.END, f"{note.id}: {note.title}")

        if notes:
            self.status_bar.config(text=f"Всего заметок: {len(notes)}")
        else:
            self.status_bar.config(text="Нет заметок")

    def new_note(self):
        """Очистить поля для новой заметки"""
        self.current_note = None
        self.title_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.status_bar.config(text="Новая заметка")

    def save_note(self):
        """Сохранить заметку (новую или существующую)"""
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()

        if not title:
            messagebox.showwarning("Предупреждение", "Введите заголовок заметки!")
            return

        if self.current_note:  # Редактирование существующей
            self.manager.update_note(self.current_note.id, title, content)
            messagebox.showinfo("Успех", "Заметка обновлена!")
        else:  # Создание новой
            note = self.manager.add_note(title, content)
            self.current_note = note
            messagebox.showinfo("Успех", "Заметка добавлена!")

        self.refresh_notes_list()
        self.status_bar.config(text=f"Сохранено: {title}")

    def delete_note(self):
        """Удалить выбранную заметку"""
        if not self.current_note:
            messagebox.showwarning("Предупреждение", "Выберите заметку для удаления!")
            return

        # Подтверждение удаления (как в консольной версии!)
        result = messagebox.askyesno("Подтверждение",
                                     f"Удалить заметку '{self.current_note.title}'?")

        if result:
            note_id = self.current_note.id
            if self.manager.delete_note(note_id):
                messagebox.showinfo("Успех", "Заметка удалена!")
                self.new_note()  # очищаем поля
                self.refresh_notes_list()
                self.status_bar.config(text="Заметка удалена")

    def on_note_select(self, event):
        """Обработчик выбора заметки из списка"""
        selection = self.notes_listbox.curselection()
        if not selection:
            return

        # Получаем выбранный элемент
        index = selection[0]
        note_id_text = self.notes_listbox.get(index)

        # Извлекаем ID из строки вида "1: Заголовок"
        try:
            note_id = int(note_id_text.split(":")[0])
        except:
            return

        # Находим заметку через менеджер
        note = self.manager.find_note_by_id(note_id)
        if note:
            self.current_note = note
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note.title)

            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, note.content)

            self.status_bar.config(text=f"Заметка #{note.id}: {note.title}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()