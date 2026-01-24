# ШАБЛОНЫ как дерево (теги внутри тегов)
TEMPLATES = {
    "site": {
        "tag": "html",
        "children": [
            {
                "tag": "head",
                "children": [
                    {"tag": "title", "text": "{title}"},
                    {"tag": "style", "text": "{css}"}
                ]
            },
            {
                "tag": "body",
                "children": [
                    {"tag": "header", "children": [
                        {"tag": "h1", "text": "{header}"},
                        {"tag": "nav", "children": [
                            {"tag": "a", "attrs": {"href": "/"}, "text": "Главная"},
                            {"tag": "a", "attrs": {"href": "/about"}, "text": "О нас"}
                        ]}
                    ]},
                    {"tag": "main", "children": [
                        {"tag": "p", "text": "{content}"},
                        {"tag": "div", "attrs": {"class": "box"}, "text": "Бокс"}
                    ]},
                    {"tag": "footer", "text": "© Company"}
                ]
            }
        ]
    },

    "simple_page": {
        "tag": "div",
        "attrs": {"class": "page"},
        "children": [
            {"tag": "h2", "text": "{title}"},
            {"tag": "p", "text": "{text}"}
        ]
    }
}

# СТИЛИ как дерево
STYLES = {
    "light": """
        body { font-family: Arial; background: white; color: black; }
        .box { border: 1px solid #ccc; padding: 10px; }
    """,
    "dark": """
        body { background: #333; color: white; }
        .box { border: 1px solid #666; background: #444; }
    """
}
