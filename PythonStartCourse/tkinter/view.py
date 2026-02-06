import tkinter as tk
from config import *
import controller

main_window = tk.Tk()
main_window.title(TITLE)
main_window.geometry(f"{WIDTH}x{HEIGHT}")
main_window.iconbitmap(ICON)

tk.Label(main_window, text="ЛОГИН").pack()
loginText = tk.Text(main_window, width=15, height=1)
loginText.pack()

tk.Label(main_window, text="ПАРОЛЬ").pack()
passwordText = tk.Text(main_window, width=15, height=1)
passwordText.pack()

button = tk.Button(main_window, text=" ВОЙТИ ", command=lambda: controller.auth_user(loginText.get(1.0, tk.END), passwordText.get(1.0, tk.END)))
button.pack()


if __name__ == "__main__":
    main_window.mainloop()
