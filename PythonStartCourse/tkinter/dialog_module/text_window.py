import tkinter as tk
from tkinter import scrolledtext

from note import Note


class TextEditWindow(tk.Toplevel):
    def __init__(self, parent, note: Note):
        self.note = note
        super().__init__(parent)
        self.geometry("800x600")

        self.title = note.get_filename()
        self.text_area = scrolledtext.ScrolledText(self, width=96, height=35)
        self.text_area.pack()
        self.text_area.insert(1.0, note.get_note_text())
        self.button = tk.Button(self, text="Сохранить", command=self.save_note)
        self.button.pack()

    def save_note(self):
        new_text = self.text_area.get(1.0, tk.END)
        self.note.save_note(new_text)
        self.destroy()
