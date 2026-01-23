# 📊 Наглядное сравнение сложностей
import matplotlib.pyplot as plt
import numpy as np

# Данные для графика
n = np.arange(1, 10)
complexities = {
    'O(1)': np.ones_like(n),
    'O(log n)': np.log2(n),
    'O(n)': n,
    'O(n log n)': n * np.log2(n),
    'O(n²)': n ** 2
}

plt.figure(figsize=(10, 6))
for name, values in complexities.items():
    plt.plot(n, values, label=name, linewidth=2)

plt.xlabel('Размер данных (n)')
plt.ylabel('Количество операций')
plt.title('Сравнение сложности алгоритмов')
plt.legend()
plt.grid(True)
plt.show()
