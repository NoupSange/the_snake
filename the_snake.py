from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
MIDDLE_POINT = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Базовый класс игры."""

    def __init__(self):
        self.position = MIDDLE_POINT
        self.body_color = None

    def draw(self):
        """Метод отрисовки объекта."""
        pass

class Snake(GameObject):
    """Класс описывающий змейку."""

    def __init__(self):
        super().__init__()
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """"""
        x, y = self.get_head_position()
        dx, dy = self.direction
        x += dx * GRID_SIZE
        y += dy * GRID_SIZE

        # Проверка на выход из зоны видимости экрана
        if x >= SCREEN_WIDTH:
            x = 0
        elif x < 0:
            x = SCREEN_WIDTH - GRID_SIZE
        if y >= SCREEN_HEIGHT:
            y = 0
        elif y < 0:
            y = SCREEN_HEIGHT - GRID_SIZE

        # Проверка на столкновние самой с собой
        if self.positions[0] in self.positions[2:]:
            self.reset()

        # Новая позиция головы змейки
        self.positions.insert(0, (x, y))

        # Проверка длины змейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop() 


    def draw(self, surface):
        """Метод отрисовки змейки."""
        
        # Закрашивает конец змейки, если яблоко не съедено
        if self.last:
            last_rect = pygame.Rect(
            (self.last[0], self.last[1]),
            (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        # Отрисовка всей змейки
        if self.length == 1:
                x, y = self.get_head_position()
                rect = (pygame.Rect(
                    (x, y), (GRID_SIZE, GRID_SIZE)))

                pygame.draw.rect(surface, self.body_color, rect)
                pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        else:
            for position in self.positions:
                rect = (
                    pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
                )
                pygame.draw.rect(surface, self.body_color, rect)
                pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс параметров змейки."""
        self.positions = [self.position]
        self.length = 1
        possible_directions = [RIGHT, LEFT, UP, DOWN]
        self.direction = choice(possible_directions)
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс описывающий змейку."""

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Рандомайзер позиции яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            

def main():
    """Создаем экземпляры змейки и яблока."""
    snake = Snake()
    apple = Apple()
    print(snake.position)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        print('позиция змейки', snake.positions)
        print('позиция яблока', apple.position)
        print(snake.length)
        # проверка съедено ли яблоко
        if apple.position in snake.positions:
            snake.length += 1
            apple.randomize_position()
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()