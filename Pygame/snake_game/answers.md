
> [!NOTE]
> 👨‍🏆 Ответы на задачи для самостоятельной работы.
  <br>

### Задание 1. Поменяй цвет фона
**Файл:** `color.py`
```python
green = (0, 255, 0)
lightblue = (173, 216, 230)  # Добавить эту строку
```

### Задание 2. Увеличь размер фрукта
**Файл:** `Fruit.py`
```python
self.width = 25
self.height = 25
```

### Задание 3. Измени скорость змейки
**Файл:** `consts.py`
```python
game_FPS = 10
```

### Задание 4. Сделай фрукт квадратным
**Файл:** `Fruit.py` (уже сделано в задании 2, если размеры равны)

### Задание 5. Добавь надпись при проигрыше
**Файл:** `SnakeGame.py`
```python
def game_loop(self):
    while not self.game_over:
        self.game_logic()
        self.render.add_render_object(self.fruit,self.snake)
        self.render.render()
    print("Game Over")  # Добавить эту строку
    pygame.quit()
    quit()
```

### Задание 6. Поменяй цвет змейки
**Файл:** `SnakeGame.py`
```python
self.snake = Snake(color.blue,10)
```

### Задание 7. Увеличь громкость звука поедания фрукта
**Файл:** `SoundController.py`
```python
fruit_eat.set_volume(1.0)
```

### Задание 8. Сделай фрукт жёлтым
**Файл:** `Fruit.py`
```python
self.color = (255, 255, 0)
```

### Задание 9. Измени начальную длину змейки
**Файл:** `Snake.py`
```python
self.snake_length = 3
```

### Задание 10. Добавь возможность выхода по клавише ESC
**Файл:** `SnakeGame.py`
```python
elif event.type == pygame.KEYDOWN:
    if event.key == pygame.K_LEFT:
        self.snake.move(-self.snake.speed, 0)
    elif event.key == pygame.K_RIGHT:
        self.snake.move(self.snake.speed, 0)
    elif event.key == pygame.K_UP:
        self.snake.move(0, -self.snake.speed)
    elif event.key == pygame.K_DOWN:
        self.snake.move(0, self.snake.speed)
    elif event.key == pygame.K_ESCAPE:  # Добавить этот блок
        self.game_over = True
```

---
