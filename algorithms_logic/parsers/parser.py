import urllib.request
import re


def parser(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8', errors='ignore')

        h1_pattern = r'<h1[^>]*>(.*?)</h1>'
        h1_matches = re.findall(h1_pattern, html, re.DOTALL | re.IGNORECASE)

        def clean_html(text):
            return re.sub(r'<[^>]+>', '', text).strip()

        print(f"\n🎯 Заголовки h1:")
        for i, match in enumerate(h1_matches[:5], 1):
            clean_text = clean_html(match)[:100]
            if clean_text:
                print(f"  {i}. {clean_text}")

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


result = parser("https://github.com/Gabryelf/TutorialApp/blob/main/index.html")
if result:
    print(f"\n📊 Статистика: {result['h1_count']} заголовков, {result['links_count']} ссылок")

