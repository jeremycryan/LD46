from sprite_tools import Sprite, SpriteSheet
import constants as c
import math
import pygame


class Character:

    def __init__(self, game):
        self.sprite = None
        self.game = game
        pass

    def update(self, dt, events):
        pass

    def draw(self, surface):
        raise NotImplementedError()


class CapeGuy(Character):
    def __init__(self, game):
        super().__init__(game)
        self.sprite = Sprite(3, colorkey=c.BLACK)
        idle = SpriteSheet(c.image_path("evil_guy_placeholder.png"), (1, 1), 1)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")
        self.name = "Parity"

        self.x = c.WINDOW_WIDTH//2
        self.y = 125
        self.yoff = 0
        self.age = 0
        self.alpha = 0
        self.target_alpha = 255

    def update(self, dt, events):
        self.sprite.update(dt)
        self.age += dt
        self.yoff = math.sin(self.age * 1) * 12

        da = self.target_alpha - self.alpha
        if da >= 0:
            self.alpha = min(self.alpha + da * dt, self.target_alpha)
        else:
            self.alpha = max(self.alpha + da * dt, self.target_alpha)

    def draw(self, surface):
        size = self.sprite.size()
        x, y = self.game.xy_transform(self.x, self.y)
        self.sprite.set_position((x - size[0]//2, y + self.yoff - size[1]//2))
        self.sprite.draw(surface, self.alpha)


class Tetroid(Character):
    def __init__(self, game):
        super().__init__(game)
        self.body = pygame.image.load(c.image_path("tetroid.png")).convert()
        self.hands = pygame.image.load(c.image_path("tetroid_hands.png")).convert()
        self.body.set_colorkey(c.BLACK)
        self.hands.set_colorkey(c.BLACK)

        self.x = c.WINDOW_WIDTH//2
        self.y = 125
        self.yoff = 0
        self.age = 0
        self.alpha = -130
        self.target_alpha = 255
        self.name = "Tetroid"

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt
        self.yoff = math.sin(self.age * 1) * 12

        da = self.target_alpha - self.alpha
        if da >= 0:
            self.alpha = min(self.alpha + da * dt, self.target_alpha)
        else:
            self.alpha = max(self.alpha + da * dt, self.target_alpha)

    def draw(self, surface):
        x, y = self.game.xy_transform(self.x, self.y)
        x -= self.body.get_width()//2
        y -= self.body.get_height()//2
        body_off = math.sin(self.age * 1.8) * 12
        hands_off = math.sin(self.age * 1.8 - math.pi / 4) * 16
        self.body.set_alpha(self.alpha)
        self.hands.set_alpha(self.alpha + 130)
        surface.blit(self.body, (x, y + body_off))
        surface.blit(self.hands, (x, y + hands_off))


class Warden(Character):

    def __init__(self, game):
        super().__init__(game)
        self.sprite = Sprite(3, colorkey=c.BLACK)
        self.halberd = Sprite(3, colorkey=c.BLACK)
        idle = SpriteSheet(c.image_path("warden.png"), (1, 1), 1)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")

        idle = SpriteSheet(c.image_path("halberd.png"), (1, 1), 1)
        self.halberd.add_animation({"Idle": idle})
        self.halberd.start_animation("Idle")

        self.x = c.WINDOW_WIDTH // 2
        self.y = 125
        self.age = 0
        self.alpha = -200
        self.target_alpha = 255
        self.name = "Warden"

    def draw(self, surface):
        size = self.sprite.size()
        x, y = self.game.xy_transform(self.x, self.y)
        self.sprite.set_position((x - size[0]//2, y - size[1]//2))
        yoff = math.sin(self.age * 1.6) * 5
        self.halberd.set_position((x - size[0]//2, y - size[1]//2 + yoff))
        self.sprite.draw(surface, self.alpha)
        self.halberd.draw(surface, self.alpha + 200)

    def update(self, dt, events):
        self.sprite.update(dt)
        self.age += dt

        da = self.target_alpha - self.alpha
        if da >= 0:
            self.alpha = min(self.alpha + da * dt, self.target_alpha)
        else:
            self.alpha = max(self.alpha + da * dt, self.target_alpha)

