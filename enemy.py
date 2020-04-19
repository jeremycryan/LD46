import pygame
import constants as c

import math
from particle import *

import random
import math


class Enemy:

    def __init__(self, game, distance, direction):
        # distance given in time until player hit
        self.game = game
        self.distance = int(distance * c.UNIT_ENEMY_SPEED)
        self.direction = direction
        self.speed = c.UNIT_ENEMY_SPEED
        self.kill_distance = 10
        self.before_shield = True
        self.color = c.RED
        self.since_drop = 0
        self.drop_period = 0.07
        self.age = 0
        self.shine = 1.0

    def update(self, dt, events):
        self.since_drop += dt
        self.age += dt
        while self.since_drop > self.drop_period:
            self.since_drop -= self.drop_period
            x, y = self.get_xy()
            if x < -200 or y < -200 or x > c.WINDOW_WIDTH + 200 or y > c.WINDOW_HEIGHT + 200:
                continue
            for i in range(8):
                Spark(self.game, (x, y), c.WHITE)
            offsets = [-15, 0, 15] if self.direction%360 in (c.LEFT, c.RIGHT) else [-8, 0, 8]
            num = random.choice([1, 2, 3])
            while num > 0:
                if self.direction%360 in (c.LEFT, c.RIGHT):
                    n = random.choice(offsets)
                    offsets.remove(n)
                    y += n
                else:
                    n = random.choice(offsets)
                    offsets.remove(n)
                    x += n
                Bit(self.game, (x, y), self.color)
                num -= 1

        if self.distance < self.game.player.shield_radius and self.before_shield:
            if self.game.player.is_blocking(self):
                self.destroy()
                self.game.shield_hit.play()
            else:
                self.before_shield = False
        self.distance -= dt * self.speed
        if self.distance < self.kill_distance and not self.before_shield:
            self.damage_player()

        self.shine = 1.0 + math.sin(self.age * 12) * math.sin(self.age * 20) * 0.4

    def get_xy(self):
        rad = (self.direction) * math.pi / 180
        xoff = self.distance * math.cos(rad)
        yoff = -self.distance * math.sin(rad)
        x = int(self.game.player.x + xoff)
        y = int(self.game.player.y + yoff)
        return x, y

    def draw(self, surface):
        x, y = self.get_xy()
        x, y = self.jitter(x, y)
        x, y = self.game.xy_transform(x, y)

        if x < -200 or x > c.WINDOW_WIDTH + 200 or y < -200 or y > c.WINDOW_HEIGHT + 200:
            return

        lighter = [min(255, item + 50) for item in self.color]
        glow_rad = int(25 * self.shine)
        glow = pygame.Surface((glow_rad * 2, glow_rad * 2))
        pygame.draw.circle(glow, self.color, (glow_rad, glow_rad), glow_rad)
        glow.set_colorkey(c.BLACK)
        glow.set_alpha(100 * self.shine)
        surface.blit(glow, (x - glow_rad, y - glow_rad))

        pygame.draw.circle(surface, lighter, (x, y), int(7 + 2 * self.shine))
        pygame.draw.circle(surface, c.WHITE, (x, y), int(3 + 2 * self.shine))

    def damage_player(self):
        self.game.shake(16)
        self.game.set_flash(0.5)
        self.destroy()
        self.game.hit.play()

    def jitter(self, x, y):
        speed = 1.2
        amp = 4
        amt_x = math.sin(self.age * 8 * speed) * math.sin(self.age * 20 * speed) * amp
        amt_y = math.sin(self.age * 10 * speed) * math.sin(self.age * 16 * speed) * amp
        return(amt_x + x, amt_y + y)

    def destroy(self):
        if not self in self.game.enemies:
            return
        self.game.shake(4)
        self.game.enemies.remove(self)
        for i in range(20):
            Spark(self.game, self.get_xy(), self.color, width=6, speed=500, fade=1200)
            Spark(self.game, self.get_xy(), c.WHITE, width=4, speed=500, fade=1200)


class RedEnemy(Enemy):
    def __init__(self, game, distance, direction):
        super().__init__(game, distance, direction)
        self.speed *= 0.7
        self.distance *= 0.7
        self.drop_period /= 0.7


class BlueEnemy(Enemy):
    def __init__(self, game, distance, direction):
        super().__init__(game, distance, direction)
        self.color = c.RED


class FastEnemy(Enemy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed *= 4
        self.distance *= 4
        self.drop_period /= 4
        self.color = c.GREEN


class Spinny(Enemy):
    def __init__(self, *args, **kwargs):
        self.ccw = False
        if "counterclockwise" in kwargs:
            if kwargs["counterclockwise"]:
                self.ccw = True
            del(kwargs["counterclockwise"])
        super().__init__(*args, **kwargs)
        self.color = c.YELLOW

    def get_xy(self):
        sign = -1 if self.ccw else 1
        rad = (self.direction) * math.pi / 180 + sign*(self.distance/300) ** 2
        xoff = self.distance * math.cos(rad)
        yoff = -self.distance * math.sin(rad)
        x = int(self.game.player.x + xoff)
        y = int(self.game.player.y + yoff)
        return x, y


class Feint(Enemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = c.BLUE
        self.speed *= 4
        self.distance *= 4
        self.drop_period /= 4
        self.gap = 120
        self.pause_distance = 500

    def get_xy(self):
        if self.distance < self.gap:
            visible_distance = self.distance
        elif self.distance > self.gap + self.pause_distance:
            visible_distance = self.distance - self.pause_distance
        else:
            visible_distance = self.gap
        rad = (self.direction) * math.pi / 180
        xoff = visible_distance * math.cos(rad)
        yoff = -visible_distance * math.sin(rad)
        x = int(self.game.player.x + xoff)
        y = int(self.game.player.y + yoff)
        return x, y


class Speedy(Enemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed *= 8
        self.distance *= 8
        self.drop_period /= 12
        self.color = c.PURPLE
        self.has_burst = False

    def update(self, dt, events):
        super().update(dt, events)

        if self.distance < 1.0 * self.speed and self.has_burst == False:
            self.has_burst = True
            SpeedyFlash(self.game, self.direction)