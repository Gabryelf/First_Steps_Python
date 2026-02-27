import pygame
import random
from config import *


class GameObject:
    """Базовый класс для всех игровых объектов"""

    def __init__(self, x, y, width, height, color):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.color = color

    def get_rect(self):
        """Возвращает прямоугольник объекта для коллизий"""
        return pygame.Rect(
            int(self.x * CELL_SIZE),
            int(self.y * CELL_SIZE + 80),
            int(self.width * CELL_SIZE),
            int(self.height * CELL_SIZE)
        )

    def draw(self, screen):
        """Отрисовывает объект на экране"""
        pygame.draw.rect(screen, self.color, self.get_rect())


class Bullet(GameObject):
    """Класс пули"""

    def __init__(self, x, y, direction, owner):
        super().__init__(x, y, 0.3, 0.3, YELLOW)
        self.direction = direction
        self.owner = owner
        self.speed = BULLET_SPEED

    def get_rect(self):
        """Более точный хитбокс для пули"""
        size = int(0.3 * CELL_SIZE)
        return pygame.Rect(
            int((self.x - 0.15) * CELL_SIZE),
            int((self.y - 0.15) * CELL_SIZE + 80),
            size, size
        )


class Wall(GameObject):
    """Класс стены"""

    def __init__(self, x, y):
        super().__init__(x, y, 1, 1, BROWN)
        self.hits_remaining = WALL_HITS_TO_BREAK
        self.max_hits = WALL_HITS_TO_BREAK

    def hit(self):
        """Попадание в стену"""
        self.hits_remaining -= 1
        if self.hits_remaining <= 0:
            return True
        # Меняем цвет в зависимости от прочности
        intensity = 0.3 + 0.7 * (self.hits_remaining / self.max_hits)
        self.color = (
            int(139 * intensity),
            int(69 * intensity),
            int(19 * intensity)
        )
        return False


class Tank(GameObject):
    """Базовый класс танка"""

    def __init__(self, x, y, color, lives, speed, shoot_delay):
        super().__init__(x, y, TANK_SIZE, TANK_SIZE, color)
        self.lives = lives
        self.direction = 0  # 0-вверх, 1-право, 2-вниз, 3-влево
        self.speed = speed
        self.shoot_cooldown = 0
        self.shoot_delay = shoot_delay

        # Уменьшенный хитбокс для прохода между стенами
        hitbox_size = TANK_SIZE * TANK_HITBOX_REDUCE
        self.hitbox_offset = (TANK_SIZE - hitbox_size) / 2

    def get_hitbox(self):
        """Возвращает уменьшенный хитбокс для коллизий"""
        return pygame.Rect(
            int((self.x + self.hitbox_offset) * CELL_SIZE),
            int((self.y + self.hitbox_offset) * CELL_SIZE + 80),
            int(TANK_SIZE * TANK_HITBOX_REDUCE * CELL_SIZE),
            int(TANK_SIZE * TANK_HITBOX_REDUCE * CELL_SIZE)
        )

    def move(self, dx, dy, walls, tanks):
        """Попытка переместить танк с уменьшенным хитбоксом"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверяем границы поля
        if new_x < 0 or new_x + self.width > FIELD_WIDTH:
            return False
        if new_y < 0 or new_y + self.height > FIELD_HEIGHT:
            return False

        # Временный объект для проверки коллизий
        # Используем прямоугольник для проверки, а не создаем новый танк
        temp_rect = pygame.Rect(
            int((new_x + self.hitbox_offset) * CELL_SIZE),
            int((new_y + self.hitbox_offset) * CELL_SIZE + 80),
            int(TANK_SIZE * TANK_HITBOX_REDUCE * CELL_SIZE),
            int(TANK_SIZE * TANK_HITBOX_REDUCE * CELL_SIZE)
        )

        # Проверяем столкновение со стенами
        for wall in walls:
            if temp_rect.colliderect(wall.get_rect()):
                return False

        # Проверяем столкновение с другими танками
        for tank in tanks:
            if tank != self and temp_rect.colliderect(tank.get_hitbox()):
                return False

        # Если всё хорошо, перемещаемся
        self.x = new_x
        self.y = new_y
        return True

    def can_shoot(self):
        return self.shoot_cooldown <= 0

    def shoot(self):
        if not self.can_shoot():
            return None
        self.shoot_cooldown = self.shoot_delay
        bullet_x = self.x + self.width / 2
        bullet_y = self.y + self.height / 2
        return Bullet(bullet_x, bullet_y, self.direction, self)

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, screen):
        """Отрисовка танка с учетом направления"""
        rect = self.get_rect()

        # Рисуем корпус танка
        pygame.draw.rect(screen, self.color, rect)

        # Рисуем пушку в зависимости от направления
        gun_length = CELL_SIZE // 2
        gun_width = CELL_SIZE // 4
        center_x = rect.centerx
        center_y = rect.centery

        if self.direction == 0:  # вверх
            gun_rect = pygame.Rect(center_x - gun_width // 2, rect.top - gun_length, gun_width, gun_length)
        elif self.direction == 2:  # вниз
            gun_rect = pygame.Rect(center_x - gun_width // 2, rect.bottom, gun_width, gun_length)
        elif self.direction == 1:  # вправо
            gun_rect = pygame.Rect(rect.right, center_y - gun_width // 2, gun_length, gun_width)
        else:  # влево
            gun_rect = pygame.Rect(rect.left - gun_length, center_y - gun_width // 2, gun_length, gun_width)

        pygame.draw.rect(screen, DARK_GRAY, gun_rect)


class PlayerTank(Tank):
    """Класс танка игрока"""

    def __init__(self, x, y):
        super().__init__(x, y, GREEN, PLAYER_LIVES, PLAYER_SPEED, PLAYER_SHOOT_DELAY)
        self.stars = 0

    def handle_input(self, keys):
        dx = dy = 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = 3
            dx = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = 1
            dx = self.speed
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = 0
            dy = -self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = 2
            dy = self.speed

        return dx, dy


class EnemyTank(Tank):
    """Улучшенный класс вражеского танка"""

    def __init__(self, x, y):
        super().__init__(x, y, RED, ENEMY_LIVES, ENEMY_SPEED, ENEMY_SHOOT_DELAY)
        self.state_timer = 0
        self.state_duration = 120  # Действуем 2 секунды (при 60 FPS)
        self.current_state = "patrol"
        self.target_direction = random.randint(0, 3)
        self.stuck_counter = 0
        self.last_x = x
        self.last_y = y

    def change_state(self):
        """Меняет состояние бота"""
        if random.random() < 0.3:  # 30% шанс атаковать
            self.current_state = "attack"
            self.state_duration = 90  # 1.5 секунды атаки
        else:
            self.current_state = "patrol"
            self.state_duration = 180  # 3 секунды патруля
            self.target_direction = random.randint(0, 3)

    def check_if_stuck(self):
        """Проверяет, застрял ли бот"""
        if abs(self.x - self.last_x) < 0.01 and abs(self.y - self.last_y) < 0.01:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0

        self.last_x = self.x
        self.last_y = self.y

        # Если застрял, меняем направление
        if self.stuck_counter > 30:  # полсекунды без движения
            self.stuck_counter = 0
            self.target_direction = (self.target_direction + 2) % 4  # разворачиваемся
            return True
        return False

    def update_ai(self, walls, tanks, player):
        """Улучшенный ИИ с состояниями"""
        self.state_timer += 1

        # Меняем состояние по таймеру
        if self.state_timer >= self.state_duration:
            self.state_timer = 0
            self.change_state()

        # Проверяем, не застрял ли
        self.check_if_stuck()

        # Действуем в зависимости от состояния
        if self.current_state == "attack" and player:
            # Атакуем игрока
            self.attack_player(walls, tanks, player)
        else:
            # Патрулируем
            self.patrol(walls, tanks, player)

    def attack_player(self, walls, tanks, player):
        """Атака игрока - более осмысленное движение"""
        dx_to_player = player.x - self.x
        dy_to_player = player.y - self.y

        # Выбираем направление к игроку
        if abs(dx_to_player) > abs(dy_to_player):
            if dx_to_player > 0:
                target_dir = 1  # вправо
            else:
                target_dir = 3  # влево
        else:
            if dy_to_player > 0:
                target_dir = 2  # вниз
            else:
                target_dir = 0  # вверх

        # Пытаемся двигаться в выбранном направлении
        dx = dy = 0
        if target_dir == 0:
            dy = -self.speed
        elif target_dir == 1:
            dx = self.speed
        elif target_dir == 2:
            dy = self.speed
        else:
            dx = -self.speed

        if not self.move(dx, dy, walls, tanks + [player] if player else tanks):
            # Если не можем двигаться к игроку, пробуем другое направление
            self.target_direction = (target_dir + 1) % 4
            self.patrol(walls, tanks, player)
        else:
            self.direction = target_dir

    def patrol(self, walls, tanks, player):
        """Патрулирование - медленное, осмысленное движение"""
        # Двигаемся в текущем направлении
        dx = dy = 0
        if self.target_direction == 0:
            dy = -self.speed
        elif self.target_direction == 1:
            dx = self.speed
        elif self.target_direction == 2:
            dy = self.speed
        else:
            dx = -self.speed

        # Если не можем двигаться, меняем направление
        tanks_list = tanks + [player] if player else tanks
        if not self.move(dx, dy, walls, tanks_list):
            self.target_direction = random.randint(0, 3)
        else:
            self.direction = self.target_direction