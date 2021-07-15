import sys
import pygame
import config

from food import Food
from snake import Snake


def create_game_case(x, y) -> pygame.Rect:
    return pygame.Rect((x * config.GRID_SIZE, y * config.GRID_SIZE), (config.GRID_SIZE, config.GRID_SIZE))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 0, 32)
        self.running = False
        self.snake = Snake(config.SNAKE_START)
        self.clock = pygame.time.Clock()
        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.score = 0
        self.color = (17, 24, 47)
        self.game_speed = 6
        self.food = Food()
        self.pause = False

        self.draw_grid()

    def draw_grid(self) -> None:
        for y in range(1, config.GRID_HEIGHT - 1):
            for x in range(1, config.GRID_WIDTH - 1):
                r = create_game_case(x, y)
                pygame.draw.rect(self.surface,
                                 config.BACKGROUND_ODD_COLOR if (x + y) % 2 else config.BACKGROUND_EVEN_COLOR, r)

    def draw_snake(self):
        for position in self.snake.positions:
            r = create_game_case(position[0], position[1])
            pygame.draw.rect(self.surface, Snake.COLOR, r)
            pygame.draw.rect(self.surface, config.BACKGROUND_ODD_COLOR, r, 1)

    def draw_food(self):
        r = create_game_case(self.food.position[0], self.food.position[1])
        pygame.draw.rect(self.surface, Food.COLOR, r)
        pygame.draw.rect(self.surface, config.BACKGROUND_ODD_COLOR, r, 1)

    def draw_score(self):
        text = pygame.font.SysFont("monospace", 16).render("Score %d" % self.score, True, (255, 255, 255), (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT - text_rect.height / 2)
        self.screen.blit(text, text_rect)

    def draw_pause(self):
        text = pygame.font.SysFont("monospace", 20).render("PAUSE", True, (255, 255, 255), (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
        self.screen.blit(text, text_rect)
        pygame.display.update(text_rect)

    def detection_eat(self):
        return self.food.position == self.snake.get_head_position()

    def detect_end(self):
        head_x, head_y = self.snake.get_head_position()
        return not (0 < head_x < config.GRID_WIDTH - 1 and 0 < head_y < config.GRID_HEIGHT - 1)

    def reset(self):
        self.snake = Snake(config.SNAKE_START)
        self.score = 0
        self.food = Food()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != Snake.DIRECTION_DOWN:
                    self.snake.direction = Snake.DIRECTION_UP
                elif event.key == pygame.K_DOWN and self.snake.direction != Snake.DIRECTION_UP:
                    self.snake.direction = Snake.DIRECTION_DOWN
                elif event.key == pygame.K_RIGHT and self.snake.direction != Snake.DIRECTION_LEFT:
                    self.snake.direction = Snake.DIRECTION_RIGHT
                elif event.key == pygame.K_LEFT and self.snake.direction != Snake.DIRECTION_RIGHT:
                    self.snake.direction = Snake.DIRECTION_LEFT
                elif event.key == pygame.K_SPACE:
                    self.pause = not self.pause

    def run(self) -> None:
        if self.running:
            return

        self.running = True

        while self.running:
            self.clock.tick(self.game_speed)
            self.handle_keys()
            if self.pause:
                self.draw_pause()
                continue

            if self.detection_eat():
                self.snake.grow()
                self.food = Food()
                self.score += 1

            if not self.snake.move() or self.detect_end():
                self.reset()

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_food()
            self.draw_snake()
            self.screen.blit(self.surface, (0, 0))
            self.draw_score()

            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
