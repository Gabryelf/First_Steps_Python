class Node:
    """Узел связного списка"""

    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    """Односвязный список"""

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, data):
        """Добавление в конец списка"""
        new_node = Node(data)

        if self.head is None:  # Если список пуст
            self.head = new_node
            self.tail = new_node
        else:  # Если в списке уже есть элементы
            self.tail.next = new_node
            self.tail = new_node

        self.length += 1

    def prepend(self, data):
        """Добавление в начало списка"""
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

        self.length += 1

    def insert(self, index, data):
        """Вставка по индексу"""
        if index <= 0:
            self.prepend(data)
        elif index >= self.length:
            self.append(data)
        else:
            new_node = Node(data)
            current = self.head

            for _ in range(index - 1):
                current = current.next

            new_node.next = current.next
            current.next = new_node
            self.length += 1

    def visualize(self):
        """Визуализация списка"""
        result = []
        current = self.head

        while current:
            result.append(f"({current.data})")
            if current.next:
                result.append("→")
            current = current.next

        return " ".join(result)


# 🎨 Создание и визуализация списка
llist = LinkedList()
for value in [10, 20, 30, 40, 50]:
    llist.append(value)

print("Связный список:")
print(llist.visualize())
print(f"Длина списка: {llist.length}")

# Вставка нового элемента
llist.insert(2, 25)
print("\nПосле вставки 25 на позицию 2:")
print(llist.visualize())