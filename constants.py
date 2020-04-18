WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

FPS = 60

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
DARK_RED = 100, 0, 0

UNIT_ENEMY_SPEED = 150

PRINTABLE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*(),.<>'\";:+=-_/? "
BOX_PADDING = 25

RIGHT = 0
LEFT = 180
UP = 90
DOWN = 270
DIRECTIONS = (RIGHT, UP, LEFT, DOWN)


def image_path(rel):
    return "assets/images/" + rel


def font_path(rel):
    return "assets/fonts/" + rel