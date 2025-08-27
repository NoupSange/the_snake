import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT

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
POSSIBLE_DIRECTIONS = (RIGHT, LEFT, UP, DOWN)

CONTROLS_DIRECTIONS = {K_UP: UP, K_DOWN: DOWN, K_LEFT: LEFT, K_RIGHT: RIGHT}

OPPOSITE_DIRECTIONS = {K_UP: DOWN, K_DOWN: UP, K_LEFT: RIGHT, K_RIGHT: LEFT}

# Подготовка к отрисовке шрифтов
SCORE_FONT_IN_GAME, SCORE_FONT_RESULT, NEW_GAME_BTN = (
    pygame.font.SysFont('asimovian', x) for x in (30, 80, 20)
)

PAUSE_FONTS = tuple(
    pygame.font.SysFont('asimovian', x) for x in (100, 50)
)

# Рендеры статических изображений шрифтов для паузы
PAUSE_ITEMS = (
    (PAUSE_FONTS[0].render('Pause...', True, (255, 140, 0)),
     (170, 160)),
    (PAUSE_FONTS[1].render('Press any key', True, (255, 215, 0)),
     (230, 270)),
)

# Цвет границы ячейки
BORDER_COLOR = (17, 36, 28)

SNAKE_COLOR = (49, 102, 80)

SCORE_COLOR = (255, 255, 255)

BOARD_BACKGROUND_COLOR = (33, 33, 33)

# Скорость движения змейки:
SPEED = 20
