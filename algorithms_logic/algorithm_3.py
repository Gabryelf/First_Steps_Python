class DynamicArray:
    """Учебная реализация динамического массива"""

    def __init__(self):
        self.capacity = 2  # Начальная вместимость
        self.length = 0  # Текущая длина
        self.array = [None] * self.capacity

    def __getitem__(self, index):
        if 0 <= index < self.length:
            return self.array[index]
        raise IndexError("Индекс вне границ массива")

    def append(self, value):
        """Добавление элемента в конец"""
        if self.length == self.capacity:
            self._resize()  # Увеличиваем массив при необходимости

        self.array[self.length] = value
        self.length += 1

    def _resize(self):
        """Увеличение размера массива в 2 раза"""
        new_capacity = self.capacity * 2
        new_array = [None] * new_capacity

        for i in range(self.length):
            new_array[i] = self.array[i]

        self.array = new_array
        self.capacity = new_capacity

    def __str__(self):
        return str([self.array[i] for i in range(self.length)])


# Демонстрация работы
arr = DynamicArray()
print("Начальное состояние:", arr)

for i in range(10):
    arr.append(i)
    print(f"После добавления {i}: {arr}")