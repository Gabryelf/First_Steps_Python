import tkinter as tk
import random
import math

WIDTH, HEIGHT = 800, 600

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()

        self.player = self.canvas.create_polygon(400, 550, 390, 580, 410, 580, fill='cyan')
        self.bullets = []
        self.enemies = []
        self.asteroids = []

        self.health = 100
        self.ammo = 10
        self.score = 0
        self.level = 1

        self.xp = 0
        self.xp_threshold = 100
        self.xp_min = 0

        self.paused = False
        self.in_menu = True

        self.create_ui()
        self.show_menu()

    def create_ui(self):
        self.health_bar = self.canvas.create_rectangle(10, 10, 110, 30, fill='green')
        self.ammo_bar = self.canvas.create_rectangle(10, 40, 10 + self.ammo * 10, 60, fill='blue')
        self.xp_bar = self.canvas.create_rectangle(10, 70, 110, 90, fill='yellow')
        self.pause_button = tk.Button(self.root, text="Пауза", command=self.toggle_pause)
        self.pause_button.place(x=WIDTH - 80, y=10)

    def show_menu(self):
        self.canvas.delete("all")
        self.in_menu = True
        self.menu_frame = tk.Frame(self.root, bg='black')
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        start_btn = tk.Button(self.menu_frame, text="Старт", width=20, command=self.start_game)
        start_btn.pack(pady=10)

        exit_btn = tk.Button(self.menu_frame, text="Выход", width=20, command=self.root.destroy)
        exit_btn.pack(pady=10)

    def start_game(self):
        self.menu_frame.destroy()
        self.in_menu = False
        self.health = 100
        self.ammo = 10
        self.score = 0
        self.level = 1
        self.xp = 0
        self.xp_min = 0
        self.xp_threshold = 100
        self.update_ui()
        self.game_loop()

    def toggle_pause(self):
        if self.paused:
            self.resume_game()
        else:
            self.pause_game()

    def pause_game(self):
        self.paused = True
        self.pause_frame = tk.Frame(self.root, bg='black')
        self.pause_frame.place(relx=0.5, rely=0.5, anchor="center")

        resume_btn = tk.Button(self.pause_frame, text="Возобновить", width=20, command=self.resume_game)
        resume_btn.pack(pady=10)

        menu_btn = tk.Button(self.pause_frame, text="Выйти в меню", width=20, command=self.return_to_menu)
        menu_btn.pack(pady=10)

    def resume_game(self):
        self.paused = False
        if hasattr(self, "pause_frame"):
            self.pause_frame.destroy()
        self.game_loop()

    def return_to_menu(self):
        if hasattr(self, "pause_frame"):
            self.pause_frame.destroy()
        self.show_menu()

    def update_ui(self):
        self.canvas.coords(self.health_bar, 10, 10, 10 + self.health, 30)
        self.canvas.coords(self.ammo_bar, 10, 40, 10 + self.ammo * 10, 60)
        xp_width = 100 * (self.xp - self.xp_min) / (self.xp_threshold - self.xp_min)
        self.canvas.coords(self.xp_bar, 10, 70, 10 + xp_width, 90)

    def game_loop(self):
        if self.paused or self.in_menu:
            return

        self.move_bullets()
        self.spawn_enemies()
        self.move_enemies()
        self.check_collisions()

        self.update_ui()

        self.root.after(50, self.game_loop)

    def move_bullets(self):
        for bullet in self.bullets:
            self.canvas.move(bullet, 0, -10)
        self.bullets = [b for b in self.bullets if self.canvas.coords(b)[1] > 0]

    def spawn_enemies(self):
        if random.randint(1, 30) == 1:
            x = random.randint(20, WIDTH - 20)
            enemy = self.canvas.create_polygon(x, 0, x - 10, 30, x + 10, 30, fill='red')
            self.enemies.append(enemy)

    def move_enemies(self):
        for enemy in self.enemies:
            self.canvas.move(enemy, 0, 5)
        self.enemies = [e for e in self.enemies if self.canvas.coords(e)[1] < HEIGHT]

    def check_collisions(self):
        for bullet in self.bullets:
            bullet_coords = self.canvas.bbox(bullet)
            for enemy in self.enemies:
                if self.canvas.bbox(enemy) and self.check_overlap(bullet_coords, self.canvas.bbox(enemy)):
                    self.canvas.delete(bullet)
                    self.canvas.delete(enemy)
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    self.gain_xp(20)
                    break

    def check_overlap(self, box1, box2):
        return (box1[2] > box2[0] and box1[0] < box2[2] and
                box1[3] > box2[1] and box1[1] < box2[3])

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_threshold:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp_min = self.xp_threshold
        self.xp_threshold += 100
        self.xp = self.xp_min
        print(f"Уровень повышен до {self.level}!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Космическая стрелялка")
    game = Game(root)
    root.mainloop()


