# Пример 1
def example1(n):
    total = 0
    for i in range(n):
        total += i
    print(total)
    return total


# Пример 2
def example2(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += i * j
    print(total)
    return total


# Пример 3
def example3(n):
    return print(n * (n + 1) // 2)


example1(10)
example2(10)
example3(10)
