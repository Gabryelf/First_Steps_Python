import tkinter as tk
import random
import time
import json
import os

class SpaceShooter:
    def __init__(self, root):
        self.root = root
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.bullets = []
        self.enemies = []
        self.asteroids = []
        self.enemy_bullets = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.player_name = "Игрок"
        self.max_ammo = 10
        self.ammo = self.max_ammo
        self.reloading = False
        self.game_running = False

        self.show_main_menu()

    def clear_screen(self):
        self.canvas.delete("all")

    def show_main_menu(self):
        self.clear_screen()
        self.canvas.create_text(self.width//2, 200, text="КОСМИЧЕСКАЯ СТРЕЛЯЛКА", fill="white", font=("Arial", 32))

        self.canvas.create_rectangle(self.width//2 - 100, 300, self.width//2 + 100, 350, fill="green", tags="start")
        self.canvas.create_text(self.width//2, 325, text="СТАРТ", fill="white", font=("Arial", 16), tags="start")

        self.canvas.create_rectangle(self.width//2 - 100, 370, self.width//2 + 100, 420, fill="blue", tags="records")
        self.canvas.create_text(self.width//2, 395, text="РЕКОРДЫ", fill="white", font=("Arial", 16), tags="records")

        self.canvas.create_rectangle(self.width//2 - 100, 440, self.width//2 + 100, 490, fill="orange", tags="settings")
        self.canvas.create_text(self.width//2, 465, text="НАСТРОЙКИ", fill="white", font=("Arial", 16), tags="settings")

        self.canvas.tag_bind("start", "<Button-1>", self.start_game)
        self.canvas.tag_bind("records", "<Button-1>", self.show_leaderboard)
        self.canvas.tag_bind("settings", "<Button-1>", self.show_settings)

    def start_game(self, event=None):
        self.clear_screen()
        self.score = 0
        self.lives = 3
        self.level = 1
        self.ammo = self.max_ammo
        self.reloading = False
        self.bullets.clear()
        self.enemies.clear()
        self.asteroids.clear()
        self.enemy_bullets.clear()
        px = self.width // 2
        py = self.height - 60
        self.player = self.canvas.create_polygon(px, py, px - 25, py + 40, px + 25, py + 40, fill="cyan", tag="player")
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.shoot)
        self.game_running = True
        self.update_game()

    def move_left(self, event):
        self.canvas.move("player", -15, 0)

    def move_right(self, event):
        self.canvas.move("player", 15, 0)

    def shoot(self, event):
        if self.reloading or self.ammo <= 0:
            return
        coords = self.canvas.coords("player")
        x = (coords[0] + coords[2]) / 2
        y = (coords[1] + coords[5]) / 2 - 20
        bullet = self.canvas.create_rectangle(x - 3, y - 20, x + 3, y, fill="yellow")
        self.bullets.append(bullet)
        self.ammo -= 1
        if self.ammo == 0:
            self.reloading = True
            self.root.after(2000, self.reload_ammo)

    def reload_ammo(self):
        self.ammo = self.max_ammo
        self.reloading = False

    def spawn_enemy(self):
        x = random.randint(30, self.width - 30)
        enemy = self.canvas.create_polygon(x, 0, x - 15, 30, x + 15, 30, fill="red")
        self.enemies.append(enemy)

    def spawn_asteroid(self):
        x = random.randint(30, self.width - 30)
        asteroid = self.canvas.create_oval(x - 20, 0, x + 20, 40, fill="gray")
        self.asteroids.append(asteroid)

    def update_game(self):
        if not self.game_running:
            return

        self.canvas.delete("hud")

        # HUD текст
        self.canvas.create_text(100, 30, text=f"Очки: {self.score}", fill="white", font=("Arial", 14), tag="hud")
        self.canvas.create_text(100, 60, text=f"Уровень: {self.level}", fill="white", font=("Arial", 14), tag="hud")

        # Прогресс-бар жизней
        self.canvas.create_text(250, 30, text="Жизни:", fill="white", font=("Arial", 12), tag="hud")
        self.canvas.create_rectangle(300, 20, 400, 40, outline="white", tag="hud")
        self.canvas.create_rectangle(300, 20, 300 + (self.lives / 3) * 100, 40, fill="green", tag="hud")

        # Прогресс-бар патронов
        self.canvas.create_text(250, 60, text="Патроны:", fill="white", font=("Arial", 12), tag="hud")
        self.canvas.create_rectangle(300, 50, 400, 70, outline="white", tag="hud")
        if not self.reloading:
            self.canvas.create_rectangle(300, 50, 300 + (self.ammo / self.max_ammo) * 100, 70, fill="yellow", tag="hud")
        else:
            self.canvas.create_text(350, 60, text="Перезарядка", fill="white", font=("Arial", 10), tag="hud")

        # Спавн врагов и астероидов
        if random.random() < 0.01 + 0.005 * self.level:
            self.spawn_asteroid()
        if random.random() < 0.005 + 0.002 * self.level:
            self.spawn_enemy()

        # Обработка движения пуль
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -10)
            if self.canvas.coords(bullet)[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)

        # Обработка врагов
        for enemy in self.enemies[:]:
            self.canvas.move(enemy, 0, 5)
            if self.canvas.bbox(enemy)[3] > self.height:
                self.canvas.delete(enemy)
                self.enemies.remove(enemy)
                self.lives -= 1

        # Враги стреляют с шансом
        for enemy in self.enemies:
            if random.random() < 0.01:  # шанс выстрела
                coords = self.canvas.coords(enemy)
                if coords:
                    ex = (coords[0] + coords[2]) / 2
                    ey = (coords[1] + coords[5]) / 2
                    bullet = self.canvas.create_rectangle(ex - 3, ey, ex + 3, ey + 20, fill="orange")
                    self.enemy_bullets.append(bullet)

                # Обработка вражеских пуль
        for bullet in self.enemy_bullets[:]:
            self.canvas.move(bullet, 0, 10)
            if self.canvas.coords(bullet)[3] > self.height:
                self.canvas.delete(bullet)
                self.enemy_bullets.remove(bullet)
                continue

            b_box = self.canvas.bbox(bullet)
            player_box = self.canvas.bbox("player")
            if (player_box and b_box and
                b_box[2] >= player_box[0] and b_box[0] <= player_box[2] and
                b_box[3] >= player_box[1] and b_box[1] <= player_box[3]):
                self.canvas.delete(bullet)
                self.enemy_bullets.remove(bullet)
                self.lives -= 1


        # Обработка астероидов
        for asteroid in self.asteroids[:]:
            self.canvas.move(asteroid, 0, 5)
            if self.canvas.coords(asteroid)[3] > self.height:
                self.canvas.delete(asteroid)
                self.asteroids.remove(asteroid)
                self.score = max(0, self.score - 1)

        # Проверка попаданий
        for bullet in self.bullets[:]:
            b_box = self.canvas.bbox(bullet)
            for target in self.enemies + self.asteroids:
                if self.canvas.bbox(target) and b_box:
                    t_box = self.canvas.bbox(target)
                    if (b_box[2] >= t_box[0] and b_box[0] <= t_box[2] and
                        b_box[3] >= t_box[1] and b_box[1] <= t_box[3]):
                        self.canvas.delete(bullet)
                        self.canvas.delete(target)
                        self.bullets.remove(bullet)
                        if target in self.enemies:
                            self.enemies.remove(target)
                            self.score += 10
                        else:
                            self.asteroids.remove(target)
                            self.score += 5
                        break

        # Проверка поражения
        if self.lives <= 0:
            self.game_running = False
            self.save_score()
            self.canvas.create_text(self.width//2, self.height//2, text="Игра окончена", fill="white", font=("Arial", 24))
            self.canvas.create_text(self.width//2, self.height//2 + 40, text="Нажмите любую клавишу", fill="white", font=("Arial", 16))
            self.root.bind("<Key>", lambda e: self.show_main_menu())
            return

        # Уровень
        if self.score >= self.level * 100:
            self.level += 1

        self.root.after(30, self.update_game)

    def save_score(self):
        scores = []
        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as f:
                scores = json.load(f)
        scores.append({"name": self.player_name, "score": self.score})
        scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
        with open("leaderboard.json", "w") as f:
            json.dump(scores, f)

    def show_leaderboard(self, event=None):
        self.clear_screen()
        self.canvas.create_text(self.width//2, 100, text="Таблица рекордов", fill="white", font=("Arial", 24))
        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as f:
                scores = json.load(f)
                for i, entry in enumerate(scores):
                    self.canvas.create_text(self.width//2, 150 + i * 30,
                                            text=f"{i + 1}. {entry['name']} - {entry['score']}", fill="white", font=("Arial", 16))
        self.back_button()

    def show_settings(self, event=None):
        self.clear_screen()
        self.canvas.create_text(self.width//2, 200, text="НАСТРОЙКИ", fill="white", font=("Arial", 24))
        self.name_entry = tk.Entry(self.root, font=("Arial", 14))
        self.canvas.create_window(self.width//2, 300, window=self.name_entry)
        self.canvas.create_rectangle(self.width//2 - 60, 350, self.width//2 + 60, 390, fill="green", tags="ok")
        self.canvas.create_text(self.width//2, 370, text="ОК", fill="white", font=("Arial", 14), tags="ok")
        self.canvas.tag_bind("ok", "<Button-1>", self.save_username)
        self.back_button()

    def save_username(self, event):
        self.player_name = self.name_entry.get() or "Игрок"
        self.name_entry.destroy()
        self.show_main_menu()

    def back_button(self):
        self.canvas.create_rectangle(20, 20, 100, 60, fill="gray", tags="back")
        self.canvas.create_text(60, 40, text="Назад", fill="white", font=("Arial", 12), tags="back")
        self.canvas.tag_bind("back", "<Button-1>", lambda e: self.show_main_menu())

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Космическая стрелялка")
    root.attributes("-fullscreen", True)
    game = SpaceShooter(root)
    root.mainloop()

