import os

structure = ["index.html", "styles.css", "main.js", "assets/", "src/", "src/game.js"]

name = input("Название: ") or "Game"
path = input("Путь: ") or "."

full = os.path.join(path, name)
os.makedirs(full, exist_ok=True)

for item in structure:
    p = os.path.join(full, item)
    if item.endswith('/'):
        os.makedirs(p, exist_ok=True)
    else:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').close()

