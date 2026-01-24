# 🌐 **ПРОСТОЙ ПАРСЕР ВЕБ-СТРАНИЦ (работающий пример)**

## **1. БАЗОВЫЙ ПАРСЕР (requests + beautifulsoup)**

```python
# Установите сначала: pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

def simple_parser(url, tag_to_find="h1"):
    """
    Простой парсер: заходит на сайт и ищет теги
    """
    try:
        # 1. Получаем страницу
        print(f"📡 Загружаем: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            print(f"❌ Ошибка {response.status_code}")
            return []
        
        # 2. Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Ищем нужные теги
        elements = soup.find_all(tag_to_find)
        
        # 4. Выводим результат
        print(f"🔍 Найдено {len(elements)} элементов <{tag_to_find}>:")
        for i, elem in enumerate(elements, 1):
            text = elem.get_text(strip=True)
            print(f"  {i}. {text}")
        
        return elements
        
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return []

# ПРОСТОЙ ИНТЕРФЕЙС
print("🎯 ПРОСТОЙ ПАРСЕР СТРАНИЦ")
print("=" * 40)

url = input("Введите URL (например: https://example.com): ")
tag = input("Какой тег ищем? (h1, h2, p, a): ").strip() or "h1"

simple_parser(url, tag)
```

## **2. ПАРСЕР ДЛЯ НОВОСТЕЙ (простой пример)**

```python
import requests
from bs4 import BeautifulSoup

def news_parser():
    """
    Парсим заголовки новостей с сайта
    """
    # Используем тестовый сайт (или реальный)
    url = "https://news.ycombinator.com/"
    
    print(f"📰 Парсим новости с {url}")
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем заголовки (h1-h6)
        all_headings = []
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            headings = soup.find_all(tag)
            for h in headings:
                text = h.get_text(strip=True)
                if text and len(text) > 10:  # убираем короткие
                    all_headings.append(text)
        
        print(f"\n📰 Найдено {len(all_headings)} заголовков:")
        for i, title in enumerate(all_headings[:10], 1):  # первые 10
            print(f"  {i}. {title}")
            
        return all_headings
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

# Запускаем
news_parser()
```

## **3. ПОИСК ВСЕХ ССЫЛОК НА СТРАНИЦЕ**

```python
import requests
from bs4 import BeautifulSoup

def find_all_links(url):
    """
    Находит все ссылки на странице
    """
    print(f"🔗 Ищем все ссылки на: {url}")
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True) or "без текста"
            
            # Показываем только основные ссылки
            if href.startswith('http'):
                links.append((text, href))
        
        print(f"\n📎 Найдено {len(links)} ссылок:")
        for i, (text, href) in enumerate(links[:15], 1):  # первые 15
            print(f"  {i}. {text[:50]}... → {href[:50]}...")
            
        return links
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

# Пример использования
find_all_links("https://python.org")
```

## **4. ПАРСЕР ЦЕН (для магазина)**

```python
import requests
from bs4 import BeautifulSoup
import re

def parse_prices():
    """
    Ищем цены на странице (цифры с рублями/долларами)
    """
    # Тестовая страница (или любой магазин)
    url = input("URL магазина: ") or "https://example.com"
    
    print(f"💰 Ищем цены на: {url}")
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Получаем весь текст страницы
        all_text = soup.get_text()
        
        # Ищем цены по шаблону (цифры с валютами)
        price_pattern = r'\$?\d+[.,]?\d*\s*(?:руб|USD|€|р\.?)'
        prices = re.findall(price_pattern, all_text, re.IGNORECASE)
        
        # Уникальные цены
        unique_prices = list(set(prices))[:20]  # первые 20 уникальных
        
        print(f"\n💰 Найдено {len(unique_prices)} цен:")
        for i, price in enumerate(unique_prices, 1):
            print(f"  {i}. {price}")
            
        return unique_prices
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

# Запускаем
parse_prices()
```

## **5. ИНТЕРАКТИВНЫЙ ПАРСЕР (меню выбора)**

```python
import requests
from bs4 import BeautifulSoup

def interactive_parser():
    """
    Парсер с меню выбора действий
    """
    print("🌐 ИНТЕРАКТИВНЫЙ ПАРСЕР")
    print("=" * 40)
    
    url = input("Введите URL для анализа: ").strip()
    if not url.startswith('http'):
        url = 'https://' + url
    
    print("\nЧто будем искать?")
    print("1. Все заголовки (h1-h6)")
    print("2. Все ссылки")
    print("3. Все изображения")
    print("4. Весь текст страницы")
    
    choice = input("Ваш выбор (1-4): ")
    
    try:
        print(f"\n📡 Загружаем {url}...")
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if choice == '1':
            # Заголовки
            for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                elements = soup.find_all(tag)
                if elements:
                    print(f"\n📋 Тег <{tag}> ({len(elements)} шт):")
                    for elem in elements[:5]:  # только первые 5
                        print(f"  - {elem.get_text(strip=True)[:100]}...")
        
        elif choice == '2':
            # Ссылки
            links = soup.find_all('a', href=True)
            print(f"\n🔗 Ссылки ({len(links)} шт):")
            for link in links[:10]:  # первые 10
                text = link.get_text(strip=True)[:50] or "ссылка"
                href = link['href'][:80]
                print(f"  - {text} → {href}")
        
        elif choice == '3':
            # Изображения
            images = soup.find_all('img')
            print(f"\n🖼️ Изображения ({len(images)} шт):")
            for img in images[:10]:  # первые 10
                src = img.get('src', 'без src')[:80]
                alt = img.get('alt', 'без alt')[:50]
                print(f"  - alt: '{alt}' → src: {src}")
        
        elif choice == '4':
            # Весь текст
            text = soup.get_text()
            words = text.split()
            print(f"\n📝 Текст страницы ({len(words)} слов):")
            print("Первые 200 символов:")
            print(text[:200], "...")
        
        else:
            print("❌ Неверный выбор")
            
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")

# Запускаем
interactive_parser()
```

## **6. ПРОСТОЙ ПАРСЕР БЕЗ БИБЛИОТЕК (чистый Python)**

```python
import urllib.request
import re

def ultra_simple_parser(url):
    """
    Парсер без дополнительных библиотек
    """
    print(f"🚀 Простой парсер: {url}")
    
    try:
        # 1. Скачиваем страницу
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # 2. Ищем заголовки <h1>
        h1_pattern = r'<h1[^>]*>(.*?)</h1>'
        h1_matches = re.findall(h1_pattern, html, re.DOTALL | re.IGNORECASE)
        
        # 3. Чистим HTML теги из текста
        def clean_html(text):
            return re.sub(r'<[^>]+>', '', text).strip()
        
        print(f"\n🎯 Заголовки h1:")
        for i, match in enumerate(h1_matches[:5], 1):
            clean_text = clean_html(match)[:100]
            if clean_text:
                print(f"  {i}. {clean_text}")
        
        # 4. Ищем все ссылки
        link_pattern = r'href="(https?://[^"]+)"'
        links = re.findall(link_pattern, html)
        
        print(f"\n🔗 Внешние ссылки ({len(links)}):")
        for i, link in enumerate(links[:5], 1):
            print(f"  {i}. {link[:80]}...")
        
        return {
            'h1_count': len(h1_matches),
            'links_count': len(links),
            'first_h1': clean_html(h1_matches[0]) if h1_matches else None
        }
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

# Пример
result = ultra_simple_parser("https://example.com")
if result:
    print(f"\n📊 Статистика: {result['h1_count']} заголовков, {result['links_count']} ссылок")
```

## **7. ПРАКТИЧЕСКОЕ ЗАДАНИЕ ДЛЯ СТУДЕНТОВ**

```python
# student_task.py
import requests
from bs4 import BeautifulSoup

def student_parser():
    """
    Задание для студентов: улучшить парсер
    """
    url = "https://python.org"
    
    # TODO 1: Получить страницу
    response = requests.get(url)
    
    # TODO 2: Создать BeautifulSoup объект
    
    # TODO 3: Найти все заголовки <h2>
    
    # TODO 4: Вывести результаты
    
    # TODO 5*: Сохранить результаты в файл
    
    pass

# БОНУС: Парсер для поиска email на странице
def find_emails(url):
    response = requests.get(url)
    text = response.text
    
    # Регулярное выражение для email
    import re
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    
    print(f"📧 Найдено email: {len(emails)}")
    return emails
```

## **🚀 БЫСТРЫЙ СТАРТ:**

### **1. Установка (в терминале):**
```bash
pip install requests beautifulsoup4
```

### **2. Базовый шаблон:**
```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Ищем что-то
titles = soup.find_all('h1')
for title in titles:
    print(title.text)
```

### **3. Запуск любого примера:**
```python
# Просто скопируйте код в файл parser.py
# И запустите:
python parser.py
```

## **🎯 ЧТО СТУДЕНТЫ УВИДЯТ:**

1. **Вводят URL** → получают реальные данные с сайта
2. **Выбирают что искать** → видят результат сразу
3. **Понимают связь**: URL → Запрос → HTML → Поиск → Результат
4. **Могут экспериментировать** с разными сайтами

## **💡 ПРИМЕР РАБОТЫ:**

```
🎯 ПРОСТОЙ ПАРСЕР СТРАНИЦ
========================================
Введите URL: https://python.org
Какой тег ищем? (h1, h2, p, a): h1

📡 Загружаем: https://python.org
🔍 Найдено 1 элементов <h1>:
  1. Welcome to Python.org
```

**Это работает сразу и показывает реальную мощь Python!** 🌟