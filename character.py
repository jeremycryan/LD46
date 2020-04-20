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
        if self.alpha <= 0:
            return
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
        if self.alpha <= -200:
            return
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
        self.slashing = False
        self.slash_timer = 0

        self.left = pygame.image.load(c.image_path("warden_left.png")).convert()
        self.left.set_colorkey(c.BLACK)
        self.left.set_alpha(255)
        self.right = pygame.image.load(c.image_path("warden_right.png")).convert()
        self.right.set_colorkey(c.BLACK)
        self.right.set_alpha(255)

    def draw(self, surface):
        if self.alpha <= -200:
            return

        size = self.sprite.size()
        x, y = self.game.xy_transform(self.x, self.y)
        self.sprite.set_position((x - size[0]//2, y - size[1]//2))
        yoff = math.sin(self.age * 1.6) * 5
        self.halberd.set_position((x - size[0]//2, y - size[1]//2 + yoff))
        if not self.slashing:
            self.sprite.draw(surface, self.alpha)
            self.halberd.draw(surface, self.alpha + 200)
        else:
            width = 4
            yoff = max(0, ((self.slash_timer - 2.0) * 40)) ** 2
            alpha = min(255, 255 - (self.slash_timer - 2.0) * 800)

            lx = x - width//2 - size[0]//2
            rx = lx + self.left.get_width() + width
            ly = y - size[1]//2 + yoff
            ry = y - size[1]//2 - yoff
            self.left.set_alpha(alpha)
            self.right.set_alpha(alpha)
            if alpha > 0:
                surface.blit(self.left, (lx, ly))
                surface.blit(self.right, (rx, ry))
            else:
                self.game.characters.remove(self)

    def update(self, dt, events):
        self.sprite.update(dt)
        if not self.slashing:
            self.age += dt
        else:
            self.slash_timer += dt

        da = self.target_alpha - self.alpha
        if da >= 0:
            self.alpha = min(self.alpha + da * dt, self.target_alpha)
        else:
            self.alpha = max(self.alpha + da * dt, self.target_alpha)

    def slash(self):
        self.game.slash_sound.play()
        self.game.shake(15)
        self.slashing = True
        self.game.set_flash(0.5)