# Руководство по коду Python: Умный дом и Фабрика машин

## Часть 1: Умный Дом (Smart Home System)

### 📁 **Структура проекта**
```
smart_home/
├── main.py              # Основной файл программы
├── README.md            # Документация
└── requirements.txt     # Зависимости (пустой - только стандартная библиотека)
```

### 🎯 **Цель системы**
Создать простую систему управления умным домом с:
- Разными режимами работы
- Управлением устройствами через консоль
- Использованием декораторов для логирования
- Лямбда-функциями для быстрых команд

### 🏗️ **Архитектура системы**

#### **1. Структура данных (строки 1-8)**
```python
modes = {
    'day': {'light': 'off', 'music': 'on', 'temp': 18},
    'night': {'light': 'off', 'music': 'off', 'temp': 23},
    'morning': {'light': 'on', 'music': 'off', 'temp': 23},
}
```
**Что это:**
- `modes` - словарь (dictionary), содержащий режимы работы дома
- Ключи: названия режимов (`'day'`, `'night'`, `'morning'`)
- Значения: вложенные словари с параметрами устройств
- `current_mode = 'morning'` - глобальная переменная, хранящая текущий режим

**Зачем нужно:**
- Централизованное хранение всех настроек
- Быстрый доступ к параметрам по названию режима
- Легкое добавление новых режимов

#### **2. Декоратор `show_status` (строки 11-19)**
```python
def show_status(funk):
    def wrapper(*args):
        print(f"\n Действие : {funk.__name__}")
        result = funk(*args)
        print(f"\n Выбран режим : {current_mode}")
        for k, v in modes[current_mode].items():
            print(f"\n  {k} = {v} ")
        return result
    return wrapper
```

**📚 Что такое декоратор:**
- Декоратор - это функция, которая принимает другую функцию и расширяет её поведение
- Синтаксис `@decorator_name` применяется перед определением функции
- Декораторы используются для добавления логирования, проверок, кеширования

**Как работает `show_status`:**
1. При вызове декорированной функции сначала выполняется код в `wrapper`
2. Выводится название вызываемой функции (`funk.__name__`)
3. Выполняется оригинальная функция (`funk(*args)`)
4. Выводится текущий статус системы
5. Возвращается результат оригинальной функции

**Пример использования:**
```python
@show_status
def some_function():
    # код функции
```

#### **3. Функция `change_mode` (строки 22-29)**
```python
@show_status
def change_mode(new_mode):
    global current_mode
    if new_mode in modes:
        current_mode = new_mode
        return f"Установлен режим {new_mode}"
    return f" режим {new_mode} не найден!"
```

**Ключевые элементы:**
- `@show_status` - применение декоратора (автоматический вывод статуса)
- `global current_mode` - объявление, что мы изменяем глобальную переменную
- `new_mode in modes` - проверка существования режима в словаре
- Возврат строки с результатом операции

#### **4. Функция `change_param` (строки 32-38)**
```python
@show_status
def change_param(param, value):
    if param in modes[current_mode]:
        modes[current_mode][param] = value
        return f"Изменили {param} = {value}"
    return "Error"
```

**Как это работает:**
1. Проверяем, существует ли параметр в текущем режиме
2. Если да - обновляем его значение: `modes[current_mode][param] = value`
3. Возвращаем сообщение об успехе
4. Декоратор автоматически выводит обновленный статус

#### **5. Лямбда-функция `light_on` (строка 41)**
```python
light_on = lambda: change_param('light', 'on')
```

**📚 Что такое лямбда:**
- Анонимная (безымянная) функция в одну строку
- Синтаксис: `lambda аргументы: выражение`
- Автоматически возвращает результат выражения

**Эквивалент обычной функции:**
```python
def light_on():
    return change_param('light', 'on')
```

**Преимущества лямбда:**
- Компактность
- Удобство для простых операций
- Можно использовать в словарях и списках

#### **6. Основной цикл `start_home` (строки 44-66)**
```python
def start_home():
    print("=== Умный дом ===")
    print("Доступные команды: light_on, exit")
    
    while True:
        cmd = input("> ").lower().strip()
        
        if not cmd:
            continue

        match cmd:
            case 'light_on':
                light_on()
            
            case 'exit':
                print("Выход из программы")
                break
            
            case _:
                print(f"Неизвестная команда '{cmd}'")
```

**📚 Что такое match-case:**
- Новый синтаксис Python 3.10+
- Альтернатива длинным цепочкам if-elif-else
- Позволяет сопоставлять значения с шаблонами

**Структура match-case:**
```python
match значение:
    case шаблон1:
        # код если значение совпадает с шаблон1
    case шаблон2:
        # код если значение совпадает с шаблон2
    case _:
        # код по умолчанию (как else)
```

#### **7. Запуск программы (строка 69)**
```python
start_home()
```

**Поток выполнения:**
1. Определение данных и функций
2. Вызов `start_home()`
3. Бесконечный цикл ввода команд
4. Обработка команд через match-case
5. Вызов соответствующих функций
6. Автоматический вывод статуса через декоратор

### 🎨 **Визуализация работы программы**

```
Инициализация
    ↓
Загрузка режимов
    ↓
Создание функций и декораторов
    ↓
Запуск start_home()
    ↓
    ┌─────────────┐
    │ Ввод команды│
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │ Обработка   │
    │ через match │
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │ Вызов       │
    │ функции     │
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │ Декоратор   │
    │ show_status │
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │ Вывод       │
    │ статуса     │
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │ Новая       │
    │ команда?    │─Да─┐
    └──────┬──────┘    │
           Нет         ↓
           ↓     ┌─────────────┐
    ┌─────────────┐    │
    │  Завершение │    │
    └─────────────┘    │
                       │
                       └───┐
```

### 🔧 **Как добавить новую команду**

**Шаг 1: Добавить лямбда-функцию**
```python
light_off = lambda: change_param('light', 'off')
music_on = lambda: change_param('music', 'on')
```

**Шаг 2: Расширить match-case**
```python
match cmd:
    case 'light_on':
        light_on()
    case 'light_off':
        light_off()
    case 'music_on':
        music_on()
```

**Шаг 3: Обновить список команд**
```python
print("Доступные команды: light_on, light_off, music_on, exit")
```

### 🚀 **Расширение системы**

**Добавление нового устройства:**
1. Добавить параметр в словарь modes
2. Создать функции управления
3. Добавить обработку в интерфейс

**Пример - добавление кондиционера:**
```python
# 1. Добавить в режимы
modes = {
    'day': {'light': 'off', 'music': 'on', 'temp': 18, 'ac': 'off'},
    # ...
}

# 2. Создать функции
ac_on = lambda: change_param('ac', 'on')
ac_off = lambda: change_param('ac', 'off')

# 3. Добавить в интерфейс
match cmd:
    case 'ac_on':
        ac_on()
```

---

## Часть 2: Фабрика Машин (Car Factory System)

### 📁 **Структура проекта**
```
car_factory/
├── main.py              # Основной файл программы
├── components/          # Модули компонентов
│   ├── __init__.py
│   ├── base.py         # Базовый класс Component
│   ├── engine.py       # Класс Engine
│   ├── wheel.py        # Класс Wheel
│   └── body.py         # Класс Body
├── models/             # Модели изделий
│   ├── __init__.py
│   └── car.py          # Класс Car
├── factories/          # Фабрики
│   ├── __init__.py
│   └── car_factory.py  # Класс CarFactory
└── main_app.py         # Точка входа
```

### 🎯 **Цель системы**
Создать систему для конструирования машин с:
- Абстрактными компонентами
- Наследованием классов
- Фабричным методом создания
- Интерактивным интерфейсом

### 🏗️ **Архитектура системы**

#### **1. Абстрактный класс Component (строки 1-8)**
```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass
```

**📚 Что такое абстрактный класс:**
- Класс, который не предназначен для создания экземпляров
- Содержит абстрактные методы (без реализации)
- Наследники обязаны реализовать абстрактные методы
- `ABC` (Abstract Base Class) - базовый класс для абстрактных классов
- `@abstractmethod` - декоратор для объявления абстрактного метода

**Зачем нужен:**
- Определение общего интерфейса для всех компонентов
- Гарантия, что все компоненты имеют метод `get_info()`
- Полиморфизм - работа с разными компонентами через единый интерфейс

#### **2. Перечисление EngineType (строки 11-16)**
```python
from enum import Enum

class EngineType(Enum):
    GASOLINE = "бензиновый"
    DIESEL = "дизельный"
    ELECTRIC = "электрический"
    HYBRID = "гибридный"
```

**📚 Что такое Enum:**
- Перечисление - набор именованных констант
- Гарантирует, что переменная принимает только предопределенные значения
- Улучшает читаемость кода
- Предотвращает ошибки с недопустимыми значениями

**Доступ к значениям:**
```python
# Получение значения
EngineType.GASOLINE.value  # "бензиновый"

# Перебор всех значений
for engine_type in EngineType:
    print(engine_type.value)
```

#### **3. Класс Engine (строки 19-30)**
```python
class Engine(Component):
    def __init__(self, power: int, engine_type: EngineType):
        self.power = power
        self.engine_type = engine_type
    
    def get_info(self) -> str:
        return f"Двигатель: {self.engine_type.value}, {self.power} л.с."
```

**📚 Наследование классов:**
```python
class ChildClass(ParentClass):
    # Код класса
```
- `Engine` наследует от `Component`
- Наследует все методы и свойства родителя
- Может добавлять свои методы и свойства
- **Обязан** реализовать абстрактные методы

**Аннотации типов:**
```python
def __init__(self, power: int, engine_type: EngineType):
```
- `: int` - указывает, что power должен быть целым числом
- `: EngineType` - указывает, что engine_type должен быть из перечисления
- `-> str` - указывает, что функция возвращает строку
- **Важно**: Python не проверяет типы во время выполнения (type hints)

#### **4. Классы Wheel и Body (строки 33-52)**
```python
class Wheel(Component):
    def __init__(self, size: int, material: str):
        self.size = size
        self.material = material
    
    def get_info(self) -> str:
        return f"Колесо: {self.size}\", материал: {self.material}"

class Body(Component):
    def __init__(self, color: str, body_type: str):
        self.color = color
        self.body_type = body_type
    
    def get_info(self) -> str:
        return f"Кузов: {self.body_type}, цвет: {self.color}"
```

**Полиморфизм в действии:**
```python
components = [Engine(150, EngineType.GASOLINE), 
              Wheel(17, "сталь"),
              Body("красный", "седан")]

for component in components:
    print(component.get_info())
# Все компоненты имеют метод get_info(), но реализация разная
```

#### **5. Класс Car (строки 55-73)**
```python
class Car:
    def __init__(self, model: str):
        self.model = model
        self.components = []
    
    def add_component(self, component: Component):
        self.components.append(component)
        return self
    
    def show_info(self):
        print(f"\n=== Машина: {self.model} ===")
        print("Компоненты:")
        for component in self.components:
            print(f"  - {component.get_info()}")
        print("=" * 30)
```

**Метод цепочки (Fluent Interface):**
```python
return self  # в методе add_component
```

**Позволяет делать:**
```python
car = Car("Tesla")
car.add_component(engine).add_component(wheel).add_component(body)
```

**Вместо:**
```python
car = Car("Tesla")
car.add_component(engine)
car.add_component(wheel)
car.add_component(body)
```

#### **6. Класс CarFactory (строки 76-114)**
```python
class CarFactory:
    @staticmethod
    def create_car() -> Car:
        # ... интерактивное создание машины
```

**📚 Что такое статический метод:**
```python
@staticmethod
def method_name():
    # код метода
```
- Метод, принадлежащий классу, а не экземпляру
- Не имеет доступа к `self` (не может использовать атрибуты экземпляра)
- Вызывается через класс: `CarFactory.create_car()`
- Используется для утилитарных функций, связанных с классом

**Альтернативы:**
- **Метод класса** (`@classmethod`) - имеет доступ к классу через `cls`
- **Обычный метод** - имеет доступ к экземпляру через `self`

#### **7. Интерактивное создание (строки 78-114)**
```python
print("\n=== СОЗДАНИЕ МАШИНЫ ===")
model = input("Введите модель машины: ")
car = Car(model)

# Выбор двигателя
print("\nВыберите тип двигателя:")
for i, engine_type in enumerate(EngineType, 1):
    print(f"{i}. {engine_type.value}")

engine_choice = int(input("Ваш выбор (1-4): ")) - 1
power = int(input("Введите мощность двигателя (л.с.): "))

engine_type = list(EngineType)[engine_choice]
engine = Engine(power, engine_type)
car.add_component(engine)
```

**Функция `enumerate`:**
```python
for i, engine_type in enumerate(EngineType, 1):
```
- Возвращает пары (индекс, элемент)
- `1` - начальное значение индекса (по умолчанию 0)
- Позволяет создавать нумерованные списки

**Преобразование в список:**
```python
list(EngineType)[engine_choice]
```
- `EngineType` - перечисление (итерируемый объект)
- `list()` - преобразует в список для индексации
- Позволяет получить элемент по индексу

#### **8. Основная функция main (строки 117-146)**
```python
def main():
    cars = []
    
    while True:
        print("\n1. Создать новую машину")
        print("2. Показать все машины")
        print("3. Выход")
        
        choice = input("Ваш выбор: ")
        
        match choice:
            case "1":
                car = CarFactory.create_car()
                cars.append(car)
                car.show_info()
            # ... другие case
```

**Управление коллекцией машин:**
- `cars = []` - список для хранения созданных машин
- `cars.append(car)` - добавление новой машины в список
- Итерация по списку для отображения всех машин

### 🎨 **Визуализация иерархии классов**

```
                    Component (Абстрактный)
                    ├── get_info() - abstract
                    │
        ┌───────────┼───────────┐
        │           │           │
      Engine      Wheel       Body
      ├── power   ├── size    ├── color
      ├── type    ├── material├── body_type
      └── get_info() └── get_info() └── get_info()
            │
            ▼
       EngineType (Enum)
       ├── GASOLINE
       ├── DIESEL
       ├── ELECTRIC
       └── HYBRID
```

### 🏭 **Процесс создания машины**

```
       Пользователь
           ↓
       CarFactory.create_car()
           ↓
    [Ввод модели машины]
           ↓
    [Выбор двигателя]
           ↓       ↘
   [Ввод мощности]  [Выбор типа из EngineType]
           ↓       ↗
    [Создание Engine]
           ↓
    [Выбор колес]
           ↓
    [Создание Wheel]
           ↓
    [Выбор кузова]
           ↓
    [Создание Body]
           ↓
    [Сборка Car]
           ↓
    [Добавление в cars]
           ↓
    [Вывод информации]
```

### 🔧 **Как добавить новый компонент**

**Шаг 1: Создать класс компонента**
```python
class Transmission(Component):
    def __init__(self, transmission_type: str, gears: int):
        self.transmission_type = transmission_type
        self.gears = gears
    
    def get_info(self) -> str:
        return f"Коробка передач: {self.transmission_type}, {self.gears} передач"
```

**Шаг 2: Добавить в фабрику**
```python
# В методе CarFactory.create_car()
print("\nВыберите коробку передач:")
trans_type = input("Тип (механика/автомат): ")
gears = int(input("Количество передач: "))

transmission = Transmission(trans_type, gears)
car.add_component(transmission)
```

**Шаг 3: Магия полиморфизма**
- Машина уже умеет показывать новый компонент
- `car.show_info()` автоматически вызовет `transmission.get_info()`
- Никаких изменений в классе Car не требуется!

### 🎯 **Ключевые принципы ООП в проекте**

#### **1. Абстракция**
```python
class Component(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass
```
- Скрытие сложности
- Определение общего интерфейса
- Работа на уровне концепций, а не реализаций

#### **2. Наследование**
```python
class Engine(Component):
    # Наследует требование реализовать get_info()
```
- Переиспользование кода
- Создание иерархии "является" (Engine является Component)

#### **3. Полиморфизм**
```python
for component in car.components:
    print(component.get_info())  # Вызывает разную реализацию для каждого типа
```
- Один интерфейс - много реализаций
- Возможность работать с разными типами через общий интерфейс

#### **4. Инкапсуляция**
```python
self.components = []  # Внутреннее состояние объекта
```
- Сокрытие внутреннего состояния
- Доступ через публичные методы
- Защита от неправильного использования

### 🚀 **Расширение системы**

**Добавление новой фабрики:**
```python
class TruckFactory:
    @staticmethod
    def create_truck() -> Truck:
        # Создание грузовика
```

**Добавление валидации:**
```python
class Engine(Component):
    def __init__(self, power: int, engine_type: EngineType):
        if power <= 0:
            raise ValueError("Мощность должна быть положительной")
        self.power = power
        self.engine_type = engine_type
```

**Сохранение в файл:**
```python
import json

class Car:
    def to_dict(self):
        return {
            'model': self.model,
            'components': [comp.get_info() for comp in self.components]
        }
    
    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f)
```

### 📝 **Сравнение двух систем**

| Аспект | Умный дом | Фабрика машин |
|--------|-----------|---------------|
| **Парадигма** | Функциональная + процедурная | Объектно-ориентированная |
| **Организация** | Словари + функции | Классы + наследование |
| **Расширяемость** | Добавление в словарь | Добавление новых классов |
| **Принципы** | Декораторы, лямбды | ООП, полиморфизм, абстракция |
| **Использование** | Простые скрипты | Сложные системы с иерархией |

### ✅ **Практические задания**

**Для Умного дома:**
1. Добавить режим "отпуск" с особыми настройками
2. Создать декоратор для логирования действий в файл
3. Добавить возможность сохранения и загрузки настроек

**Для Фабрики машин:**
1. Добавить класс `ElectricEngine` с дополнительным свойством `battery_capacity`
2. Создать фабрику для мотоциклов
3. Реализовать сохранение каталога машин в JSON
4. Добавить валидацию вводимых данных

### 📚 **Ключевые термины**

- **Декоратор** - функция, расширяющая поведение другой функции
- **Лямбда** - анонимная функция в одну строку
- **Абстрактный класс** - класс, который нельзя инстанциировать
- **Наследование** - создание нового класса на основе существующего
- **Полиморфизм** - возможность работать с разными типами через общий интерфейс
- **Статический метод** - метод, принадлежащий классу, а не экземпляру
- **Enum** - перечисление именованных констант
- **Type Hints** - аннотации типов для лучшей читаемости кода

Это руководство охватывает все ключевые аспекты обоих проектов. Каждый раздел можно изучать независимо, а примеры кода готовы к использованию и расширению.