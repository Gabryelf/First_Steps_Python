import tkinter as tk
import random

class SpaceShooter:
    def __init__(self, root):
        """Инициализация окна игры, объектов и привязка событий клавиш"""
        self.root = root
        self.root.title("Космическая стрелялка")

        # Получаем размеры экрана
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.width = self.screen_width
        self.height = self.screen_height

        # Создаём холст на весь экран
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.level = 1
        self.score = 0
        self.lives = 3
        self.running = True

        # Игрок — треугольник внизу по центру
        px = self.width // 2
        py = self.height - 150
        self.player = self.canvas.create_polygon(
            px, py, px - 10, py + 20, px + 10, py + 20,
            fill="cyan", outline="white"
        )

        self.bullets = []
        self.enemies = []
        self.stars = []

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.shoot)

        self.update_game()

    # ===== Управление игроком =====

    def move_left(self, event):
        """Двигает игрока влево"""
        self.canvas.move(self.player, -20, 0)

    def move_right(self, event):
        """Двигает игрока вправо"""
        self.canvas.move(self.player, 20, 0)

    def shoot(self, event):
        """Создаёт пулю над игроком"""
        coords = self.canvas.coords(self.player)
        x = coords[0]
        y = coords[1]
        bullet = self.canvas.create_rectangle(x - 3, y - 20, x + 3, y, fill="yellow")
        self.bullets.append(bullet)

    # ===== Генерация объектов =====

    def spawn_enemy(self):
        """Создаёт врага в случайной позиции"""
        x = random.randint(50, 550)
        enemy = self.canvas.create_oval(x, 0, x+30, 30, fill="red")
        self.enemies.append(enemy)

    def spawn_star(self):
        """Создаёт звезду в случайной позиции"""
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        star = self.canvas.create_oval(x, y, x+2, y+2, fill="white", outline="")
        self.stars.append(star)

    # ===== Основной игровой цикл =====

    def update_game(self):
        """Основной игровой цикл — обновляет позиции объектов и логику игры"""
        if not self.running:
            return

        # Движение звёзд (фон)
        for star in self.stars:
            self.canvas.move(star, 0, 2)
            x1, y1, x2, y2 = self.canvas.coords(star)
            if y1 > self.height:
                new_x = random.randint(0, self.width)
                self.canvas.coords(star, new_x, 0, new_x + 2, 2)

        if random.random() < 0.05:
            self.spawn_star()

        # Движение пуль
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -10)
            if self.canvas.coords(bullet)[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)

        # Движение врагов
        for enemy in self.enemies[:]:
            self.canvas.move(enemy, 0, 5)
            if self.canvas.coords(enemy)[3] > self.height:
                self.canvas.delete(enemy)
                self.enemies.remove(enemy)

        # Столкновения пуль с врагами
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if self._check_collision(bullet, enemy):
                    self.canvas.delete(bullet)
                    self.canvas.delete(enemy)
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

        # Столкновения врагов с игроком
        for enemy in self.enemies[:]:
            if self._check_collision(self.player, enemy):
                self.canvas.delete(enemy)
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
                    return

        # Спавн врагов
        if random.random() < 0.02 + self.level * 0.01:
            self.spawn_enemy()

        # Обновление уровня
        if self.score >= self.level * 100:
            self.level += 1

        # Отображение интерфейса
        self.canvas.delete("hud")
        self.canvas.create_text(70, 30, text=f"Очки: {self.score}", fill="white", font=("Arial", 14), tag="hud")
        self.canvas.create_text(300, 30, text=f"Уровень: {self.level}", fill="white", font=("Arial", 14), tag="hud")
        self.canvas.create_text(530, 30, text=f"Жизни: {self.lives}", fill="white", font=("Arial", 14), tag="hud")

        self.root.after(50, self.update_game)

    def _check_collision(self, obj1, obj2):
        """Проверяет пересечение двух объектов"""
        x1, y1, x2, y2 = self.canvas.bbox(obj1)
        x3, y3, x4, y4 = self.canvas.bbox(obj2)
        return not (x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4)

    def game_over(self):
        """Завершает игру и показывает сообщение"""
        self.running = False
        self.canvas.create_text(self.width // 2, self.height // 2,
                                text="ИГРА ОКОНЧЕНА",
                                fill="red", font=("Arial", 32))

# Запуск игры
if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceShooter(root)
    root.mainloop()

