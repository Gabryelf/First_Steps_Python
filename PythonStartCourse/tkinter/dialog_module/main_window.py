import tkinter as tk
from methods import Methods
from note import Note
from text_window import TextEditWindow


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.add_button = None
        self.frame_notes = None
        self.__files = []
        self.__name = "Приложение для заметок"

    def start(self):
        self.title(self.__name)

        self.frame_notes = tk.Frame(self)
        self.frame_notes.pack(padx=10, pady=10, fill='both', expand=True)
        self.geometry("800x600")
        # Кнопка добавления новой заметки
        self.add_button = tk.Button(self, text="+", font=('Arial', 16), command=self.create_note_card)
        self.add_button.pack(side='bottom', pady=5)

        self.refresh_notes_list()
        self.show_note_card()
        self.mainloop()

    def add_note_card(self, note: Note):
        card = tk.Frame(self.frame_notes, bg='white', bd=1)
        card.pack(padx=10, pady=5, fill='x')

        title = tk.Label(card, text=note.get_filename())
        title.pack(side='left')

        edit_button = tk.Button(card, text="Редактировать", command=lambda: self.edit_note(note))
        edit_button.pack(side='right')

        delete_button = tk.Button(card, text="Удалить", command=lambda: self.delete_note(note))
        delete_button.pack(side='right')

    def edit_note(self,note:Note):
        edit_note = TextEditWindow(self, note)
        edit_note.grab_set()

    def delete_note(self, note: Note):
        note.delete_note()
        self.refresh_notes_list()
        self.show_note_card()

    def refresh_notes_list(self):
        for widget in self.frame_notes.winfo_children():
            widget.destroy()
        self.__files.clear()
        for note_name in Methods.get_note_list():
            self.add_note_to_note_list(Note(note_name))

    def add_note_to_note_list(self,note:Note):
        self.__files.append(note)

    def show_note_card(self):
        for note in self.__files:
            self.add_note_card(note)

    def create_note_card(self):
        Note.create_note()
        self.refresh_notes_list()
        self.show_note_card()