import random

import config


class Food(object):
    COLOR = (252, 78, 3)

    def __init__(self):
        self.position = (random.randint(1, config.GRID_WIDTH - 2), random.randint(1, config.GRID_HEIGHT - 2))
