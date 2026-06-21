# server/src/utils/logger.py
import logging
import sys
from datetime import datetime


def setup_logging():
    """Настройка логирования для сервера"""
    logger = logging.getLogger("idle_tower_defense_server")
    logger.setLevel(logging.INFO)

    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # Консольный handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (опционально)
    file_handler = logging.FileHandler(f"server_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger