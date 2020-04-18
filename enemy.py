import pygame
import constants as c

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

    def update(self, dt, events):
        if self.distance < self.game.player.shield_radius and self.before_shield:
            if self.game.player.is_blocking(self):
                self.destroy()
            else:
                self.before_shield = False
        self.distance -= dt * self.speed
        if self.distance < self.kill_distance:
            self.damage_player()

    def draw(self, surface):
        rad = (self.direction) * math.pi / 180
        xoff = self.distance * math.cos(rad)
        yoff = -self.distance * math.sin(rad)
        x = int(self.game.player.x + xoff)
        y = int(self.game.player.y + yoff)
        x, y = self.game.xy_transform(x, y)
        pygame.draw.circle(surface, self.color, (x, y), 9)

    def damage_player(self):
        print("BOOM")
        self.game.shake(10)
        self.destroy()

    def destroy(self):
        self.game.shake(3)
        self.game.enemies.remove(self)


class FastEnemy(Enemy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed *= 3
        self.distance *= 3
        self.color = c.GREEN