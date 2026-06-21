# server/src/api/__init__.py
"""
API routes package
"""

from . import auth, users, game, social

__all__ = ["auth", "users", "game", "social"]