WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

FPS = 70

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 80, 80
GREEN = 80, 255, 120
BLUE = 50, 140, 255
YELLOW = 255, 190, 60
PURPLE = 140, 40, 255
DARK_RED = 100, 0, 0

UNIT_ENEMY_SPEED = 200

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


def audio_path(rel):
    return "assets/audio/" + rel


def meta_path(rel):
    return "assets/meta/" + rel