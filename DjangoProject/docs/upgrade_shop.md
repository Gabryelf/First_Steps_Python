# Возможные улучшения модели Order:
## 1. Добавление статусов заказа
```python
STATUS_CHOICES = [
    ('pending', 'Ожидает обработки'),
    ('processing', 'В обработке'),
    ('shipped', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('cancelled', 'Отменен'),
]
status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
```

## 2. Добавление скидки на заказ
```python
    discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name='Скидка (в рублях)'
    )
```

```python
def get_subtotal(self):
        """Стоимость без скидки"""
        return sum(item.get_cost() for item in self.items.all())
    
    def get_total_cost(self):
        """Окончательная стоимость со скидкой"""
        subtotal = self.get_subtotal()
        return max(subtotal - self.discount, 0)  # Не может быть меньше 0
```
