# server/src/core/__init__.py
"""
Core components package
"""

from .config import settings
from .config_dev import settings
from .config_sqlite import settings

__all__ = ["settings"]
