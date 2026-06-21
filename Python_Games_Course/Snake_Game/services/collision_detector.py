from typing import List
from game_objects.food import Food


class CollisionDetector:

    @staticmethod
    def check_wall_collision(position: tuple[int, int], max_x: int, max_y: int) -> bool:
        x, y = position
        return x < 0 or x >= max_x or y < 0 or y >= max_y

    @staticmethod
    def check_food_collision(snake_head: tuple[int, int], food: Food) -> bool:
        return snake_head == food.get_position()

    @staticmethod
    def check_position_collision(position: tuple[int, int], occupied_positions: List[tuple[int, int]]) -> bool:
        return position in occupied_positions
