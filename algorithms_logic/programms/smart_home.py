"""Программа "Умный дом с использованием lambda выражений и декораторов"""

# === КОНФИГУРАЦИЯ ===
modes = {
    'день': {'свет': 'выкл', 'темп': 22, 'музыка': 'выкл'},
    'ночь': {'свет': 'тускло', 'темп': 20, 'музыка': 'выкл'},
    'вечеринка': {'свет': 'ярко', 'темп': 21, 'музыка': 'вкл'}
}

current_mode = 'день'


# === ДЕКОРАТОРЫ ===
def show_status(func):
    def wrapper(*args):
        print(f"\n--- Действие: {func.__name__} ---")
        result = func(*args)
        print(f"Режим: {current_mode}")
        for k, v in modes[current_mode].items():
            print(f"  {k}: {v}")
        return result

    return wrapper


# === ОСНОВНЫЕ ФУНКЦИИ ===
@show_status
def change_mode(new_mode):  # Смена режима
    global current_mode  # Использование глобальной переменной
    if new_mode in modes:  # Проверка режима
        current_mode = new_mode  # Установка режима
        return f"Установлен режим: {new_mode}"  # Возврат результата
    return "Ошибка: режим не найден"  # Возврат ошибки


@show_status
def change_param(param, value):  # Изменение параметра
    if param in modes[current_mode]:  # Проверка параметра
        modes[current_mode][param] = value  # Изменение значения
        return f"Изменен {param} на {value}"  # Возврат результата
    return "Ошибка: параметр не найден"  # Возврат ошибки


# Лямбда-функции для быстрого изменения
day = lambda: change_mode('day')
light_on = lambda: change_param('свет', 'вкл')  # Включить свет
light_off = lambda: change_param('свет', 'выкл')  # Выключить свет
temp_up = lambda: change_param('темп', modes[current_mode]['темп'] + 1)  # Температура+
temp_down = lambda: change_param('темп', modes[current_mode]['темп'] - 1)  # Температура-


# === ИНТЕРФЕЙС ===
def run_smart_home():  # Основной цикл
    print("=== УМНЫЙ ДОМ ===")  # Заголовок

    while True:
        cmd = input("> ").lower().strip()  # Убрал .split() здесь

        if not cmd:
            continue

        # Разделяем команду на части для анализа
        parts = cmd.split()

        # Используем match с первым словом команды
        match parts[0]:
            case 'day':
                day()
                
            case 'light_on':
                light_on()

            case 'exit':
                print("Выход из программы")
                break

            case _:  # Неизвестная команда
                print(f"Неизвестная команда '{cmd}'. Доступные: light_on, exit")


# === ЗАПУСК ===
if __name__ == "__main__":
    run_smart_home()
