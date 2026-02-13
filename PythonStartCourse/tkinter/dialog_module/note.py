import os
import uuid
from tkinter import simpledialog, messagebox


class Note:
    def __init__(self, filename):
        self.__filename = filename

    def get_filename(self):
        return self.__filename

    def save_note(self, new_text):
        with open(self.__filename, 'w') as file:
            file.write(new_text)
        messagebox.showinfo("Успех", "Заметка отредактирована!")

    def get_note_text(self):
        with open(self.__filename, 'r') as file:
            return file.read()

    def delete_note(self):
        if messagebox.askyesno("Удалить", "Вы уверены?"):
            os.remove(self.__filename)

    @staticmethod
    def create_note():
        new_text = simpledialog.askstring("Введите имя заметки", "Имя заметки")
        if new_text:
            new_filename = f"note-{uuid.uuid4().hex}.note" if new_text == "" else new_text+".note"
            with open(new_filename, 'w') as file:
                file.write("")
            messagebox.showinfo("Успех", "Заметка создана!")
