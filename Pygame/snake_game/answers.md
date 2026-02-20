
> [!NOTE]
> 👨‍🏆 Ответы на задачи для самостоятельной работы.
  <br>

### Задание 1. Плавное движение
**Файл:** `Snake.py`
```python
self.speed = 5  # Было 10
```

### Задание 2. Фрукт за границей
**Файл:** `Fruit.py` — код уже правильный! Задание на внимательность.

### Задание 3. Счёт в заголовке
**Файл:** `SnakeGame.py`
```python
# В методе game_logic() после self.snake.eat()
pygame.display.set_caption(f"{consts.game_title} | Score: {self.snake.snake_length - 1}")
```

### Задание 4. Телепортация
**Файл:** `SnakeGame.py`
```python
# В методе game_logic() после self.snake.update()
if self.snake.head.x > consts.screen_width:
    self.snake.head.x = 0
elif self.snake.head.x < 0:
    self.snake.head.x = consts.screen_width - self.snake.block_size
    
if self.snake.head.y > consts.screen_height:
    self.snake.head.y = 0
elif self.snake.head.y < 0:
    self.snake.head.y = consts.screen_height - self.snake.block_size
```

### Задание 5. Запрет разворота
**Файл:** `SnakeGame.py`
```python
# В event_handler()
if event.key == pygame.K_LEFT and self.snake.vector_x == 0:
    self.snake.move(-self.snake.speed, 0)
elif event.key == pygame.K_RIGHT and self.snake.vector_x == 0:
    self.snake.move(self.snake.speed, 0)
elif event.key == pygame.K_UP and self.snake.vector_y == 0:
    self.snake.move(0, -self.snake.speed)
elif event.key == pygame.K_DOWN and self.snake.vector_y == 0:
    self.snake.move(0, self.snake.speed)
```

### Задание 6. Вторая змейка
**Файл:** `SnakeGame.py`
```python
# В __init__
self.snake2 = Snake(color.red, 10)
self.snake2.head = pygame.Rect(300, 200, 10, 10)

# В event_handler()
elif event.key == pygame.K_a and self.snake2.vector_x == 0:
    self.snake2.move(-self.snake2.speed, 0)
elif event.key == pygame.K_d and self.snake2.vector_x == 0:
    self.snake2.move(self.snake2.speed, 0)
elif event.key == pygame.K_w and self.snake2.vector_y == 0:
    self.snake2.move(0, -self.snake2.speed)
elif event.key == pygame.K_s and self.snake2.vector_y == 0:
    self.snake2.move(0, self.snake2.speed)

# В game_logic()
if self.snake.collide(self.fruit):
    self.snake.eat()
    self.fruit.destroy()
    self.fruit = Fruit()
if self.snake2.collide(self.fruit):
    self.snake2.eat()
    self.fruit.destroy()
    self.fruit = Fruit()
    
self.snake.update()
self.snake2.update()

# В render.add_render_object()
self.render.add_render_object(self.fruit, self.snake, self.snake2)
```

### Задание 7. Столкновение змеек
**Файл:** `SnakeGame.py`
```python
# В game_logic() после обновления позиций
# Проверка столкновения головы snake с телом snake2
for segment in self.snake2.snake_list[:-1]:  # кроме головы
    if self.snake.head.colliderect(segment):
        self.game_over = True
        
# Проверка столкновения головы snake2 с телом snake
for segment in self.snake.snake_list[:-1]:  # кроме головы
    if self.snake2.head.colliderect(segment):
        self.game_over = True
```

### Задание 8. Отображение счёта
**Файл:** `SnakeGame.py`
```python
# Добавить метод
def draw_score(self, surface):
    score1 = self.snake.snake_length - 1
    score2 = self.snake2.snake_length - 1
    text = self.font_style.render(f"P1: {score1}  P2: {score2}", True, color.black)
    surface.blit(text, [10, 10])

# В game_loop() после render.render() или до
self.draw_score(self.render.surface)
pygame.display.update()
```

### Задание 9. Ядовитые фрукты
**Файл:** `Fruit.py`
```python
def __init__(self):
    self.width = 15
    self.height = 15
    self.is_poison = random.random() < 0.3  # 30% шанс
    if self.is_poison:
        self.color = (0, 0, 0)  # чёрный
    else:
        self.color = color.red
    self.x = random.randint(0, consts.screen_width - self.width)
    self.y = random.randint(0, consts.screen_height - self.height)
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
```

**Файл:** `SnakeGame.py`
```python
# В game_logic() заменить обработку столкновения
if self.snake.collide(self.fruit):
    if self.fruit.is_poison:
        self.snake.snake_length = max(1, self.snake.snake_length - 1)
        # Удалить последний сегмент
        if len(self.snake.snake_list) > self.snake.snake_length:
            self.snake.snake_list = self.snake.snake_list[:self.snake.snake_length]
    else:
        self.snake.eat()
    self.fruit.destroy()
    self.fruit = Fruit()
```

### Задание 10. Анимация поедания
**Файл:** `Fruit.py`
```python
def __init__(self):
    # ... существующий код ...
    self.eaten = False
    self.blink_count = 0
    self.blink_phase = 0

def update(self):
    if self.eaten:
        self.blink_count += 1
        if self.blink_count % 10 == 0:  # меняем цвет каждые 10 кадров
            self.blink_phase += 1
            if self.blink_phase % 2 == 0:
                self.color = (255, 255, 255)  # белый
            else:
                self.color = color.red
        if self.blink_count > 30:  # 3 мигания (30 кадров)
            return True  # пора удалить
    return False
```

**Файл:** `SnakeGame.py`
```python
# В game_logic()
if self.fruit and not self.fruit.eaten:
    if self.snake.collide(self.fruit):
        self.fruit.eaten = True
        
if self.fruit and self.fruit.eaten:
    if self.fruit.update():
        self.snake.eat()
        self.fruit = Fruit()
```

---
