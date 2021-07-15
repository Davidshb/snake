import random

import pygame

import config


class Snake(object):
    DIRECTION_UP = (0, -1)
    DIRECTION_DOWN = (0, 1)
    DIRECTION_LEFT = (-1, 0)
    DIRECTION_RIGHT = (1, 0)
    COLOR = (17, 24, 47)

    def __init__(self, start: (int, int)):
        self.size = 3
        self.positions = [start]
        self.direction = random.choice(
            [Snake.DIRECTION_UP, Snake.DIRECTION_DOWN, Snake.DIRECTION_LEFT, Snake.DIRECTION_RIGHT])

    def get_head_position(self) -> (int, int):
        return self.positions[0]

    def move(self) -> bool:
        last = self.positions.pop()
        direction_x, direction_y = self.direction
        first_x, first_y = last if len(self.positions) == 0 else self.positions[0]
        new = (first_x + direction_x, first_y + direction_y)
        if new in self.positions:
            return False
        self.positions.insert(0, new)
        return True

    def grow(self) -> None:
        last_x, last_y = self.positions[-1]
        direction_x, direction_y = self.direction
        if len(self.positions) == 1:
            self.positions.append((last_x - direction_x, last_y - direction_y))
            return
        second_last_x, second_last_y = self.positions[-2]
        self.positions.append((2 * last_x - second_last_x, 2 * last_y - second_last_y))
