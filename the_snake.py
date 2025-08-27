from random import choice, randint
from typing import Optional

import pygame

from constants import (BOARD_BACKGROUND_COLOR, BORDER_COLOR,
                       CONTROLS_DIRECTIONS, GRID_HEIGHT, GRID_SIZE, GRID_WIDTH,
                       MIDDLE_POINT, NEW_GAME_BTN, OPPOSITE_DIRECTIONS,
                       PAUSE_ITEMS, POSSIBLE_DIRECTIONS, RIGHT, SCORE_COLOR,
                       SCORE_FONT_IN_GAME, SCORE_FONT_RESULT, SCREEN_HEIGHT,
                       SCREEN_WIDTH, SNAKE_COLOR, SPEED)

pygame.init()

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameState:
    """Класс для отобажения состояния паузы."""

    def __init__(self):
        self.paused = False
        self.running = True
        # Добавить меню при старте.
        # Подключить БД для хранения счета.
        # self.open_menu = False
        self.score = 0
        self.result = None

    def draw(self, screen):
        """Отрисовка паузы, очков после проигрыша."""
        if self.running and not self.paused:
            score_img = SCORE_FONT_IN_GAME.render(
                f'Score: {self.score}', True, (SCORE_COLOR)
            )
            screen.blit(score_img, (10, 10))

        elif not self.running:
            screen.fill(BOARD_BACKGROUND_COLOR)
            img_top, img_mid = (
                SCORE_FONT_RESULT.render
                (value, True, SCORE_COLOR)
                for value in
                ('Your Score', f'{self.result}')
            )
            img_low = NEW_GAME_BTN.render('(press space)', True, SCORE_COLOR)
            screen.blit(img_top, (120, 130))
            screen.blit(img_mid, (280, 210))
            screen.blit(img_low, (260, 300))

        elif self.paused:
            for img, position in PAUSE_ITEMS:
                screen.blit(img, position)

    def is_apple_eaten(self, snake: type[object], apple: type[object]):
        """
        Проверяет, съедено ли яблоко.
        Создает новую рандомную позицию для яблока.
        Считает очки.
        """
        if apple.position in snake.positions:
            snake.length += 1
            apple.randomize_position()
            self.score += 1


class GameObject:
    """Базовый класс игры."""

    def __init__(self):
        self.position = MIDDLE_POINT
        self.body_color = None

    def draw(self):
        """Метод отрисовки объекта."""
        pass

    def draw_cell(self, x: int, y: int, cell_color: tuple[int, int, int],
                  surface, cell_border: Optional[tuple[int, int, int]] = None):
        """
        Закрашивает ячейку и бортик ячейки
        по выбраннам цветам.
        """
        rect = (pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(surface, cell_color, rect)
        if cell_border:
            pygame.draw.rect(surface, cell_border, rect, 1)


class Snake(GameObject):
    """Класс описывающий змейку."""

    def __init__(self, gamestate):
        super().__init__()
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.gamestate = gamestate

    def update_direction(self):
        """
        Присваиает новое направление движения змеи
        если была нажата клавиша в функции handle_keys
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Работает c атрибутом экземпляра класса self.positions."""
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

        # Новая позиция головы змейки
        self.positions.insert(0, (x, y))

        # Проверка на столкновние самой с собой
        if self.positions[0] in self.positions[2:]:
            print('asdg')
            self.reset()

        # Проверка длины змейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змею."""
        # Закрашивает конец змейки, если яблоко не съедено
        if self.last:
            self.draw_cell(
                self.last[0], self.last[1],
                BOARD_BACKGROUND_COLOR, surface
            )

        # Отрисовка всей змейки
        for position in self.positions:
            self.draw_cell(
                position[0], position[1],
                self.body_color, screen, BORDER_COLOR
            )

    def get_head_position(self) -> list[tuple[int, int]]:
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс параметров змейки."""
        self.positions = [self.position]
        self.length = 1
        self.gamestate.result = self.gamestate.score
        self.gamestate.score = 0
        self.gamestate.running = False
        possible_directions = POSSIBLE_DIRECTIONS
        self.direction = choice(possible_directions)
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс описывающий змейку."""

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.body_colors = self._create_colors()
        self.start_position = self.position
        self.tick_counter = 0
        self.color_state = 0

    def _create_colors(self):
        """Создает итератор цветов яблока."""
        body_colors = ((255, value, 0) for value in range(0, 180, 2))
        return body_colors

    def randomize_position(self):
        """Рандомайзер позиции яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовка яблока, для яблока
        достаточно метода базового класса GameObject.
        """
        try:
            if self.start_position != self.position:
                self.body_colors = self._create_colors()
                self.start_position = self.position
            self.draw_cell(
                self.position[0], self.position[1],
                next(self.body_colors), surface, BORDER_COLOR
            )
        except StopIteration:
            self.body_colors = self._create_colors()
            self.randomize_position()


def handle_keys(self, game_state):
    """
    Отслеживание нажатия кнопок направления движения змеи.
    Отслеживание нажатия кнопки выхода из игры.
    """
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif e.type == pygame.KEYDOWN:
            # Eсли во время паузы нажать на клавиши управления
            # игра продложится, а змейка изменит направление
            if e.key in CONTROLS_DIRECTIONS:
                if self.direction != OPPOSITE_DIRECTIONS[e.key]:
                    self.next_direction = CONTROLS_DIRECTIONS[e.key]
                game_state.paused = False
            elif e.key == pygame.K_p:
                game_state.paused = not game_state.paused
            elif e.key == pygame.K_SPACE:
                game_state.running = True

    self.update_direction()
    if not game_state.paused and game_state.running:
        self.move()


def main():
    """Создаем экземпляры змейки и яблока."""
    game_state = GameState()
    snake, apple = Snake(game_state), Apple()
    while True:
        if not game_state.paused and game_state.running:
            clock.tick(SPEED)
            screen.fill(BOARD_BACKGROUND_COLOR)
            game_state.is_apple_eaten(snake, apple)
            snake.draw(screen)
            apple.draw(screen)
        game_state.draw(screen)
        handle_keys(snake, game_state)
        pygame.display.update()


if __name__ == '__main__':
    screen.fill(BOARD_BACKGROUND_COLOR)
    main()
