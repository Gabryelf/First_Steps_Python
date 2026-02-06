import tkinter as tk
from config import *

main_window = tk.Tk()
main_window.title(TITLE)
main_window.geometry(f"{WIDTH}x{HEIGHT}")
main_window.iconbitmap(ICON)

textBox = tk.Text(main_window, width=15, height=1)
textBox.pack()

button = tk.Button(main_window, text=" Hello ", command=lambda: print(textBox.get(1.0, tk.END)))
button.pack()

main_window.mainloop()
