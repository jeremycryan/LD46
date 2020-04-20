import pygame
import constants as c
import math
from particle import Spark


class Player:

    def __init__(self, game):
        self.game = game
        self.x = c.WINDOW_WIDTH//2
        self.y = c.WINDOW_HEIGHT//2
        self.shield_angle = 0
        self.shield_vis_angle = 0
        self.shield_surf = pygame.image.load(c.image_path("shield.png")).convert()
        self.shield_bonk = pygame.image.load(c.image_path("shield_bonk.png")).convert()
        self.shield_surf.set_colorkey(c.BLACK)
        self.shield_bonk.set_colorkey(c.BLACK)
        self.shield_surf.set_alpha(0)
        self.shield_bonk.set_alpha(0)
        self.radius = 20
        self.shield_radius = 50
        self.shield_spread = 100 # in degrees
        self.has_shield = False
        self.move_disabled = False

        self.surf = pygame.image.load(c.image_path("player.png")).convert()
        self.surf.set_colorkey(c.BLACK)

        self.bonk_time = 0.08
        self.bonk_timer = self.bonk_time
        self.recoil = 0
        self.age = 0
        self.mortal = False

        self.health = 100
        self.dead = False

    def take_damage(self):
        if not self.mortal:
            self.health = int(max(self.health*0.8, 1))
        else:
            self.health = int(max(self.health - 15, 0))

    def draw(self, surface):
        if self.dead:
            return
        x, y = self.game.xy_transform(self.x, self.y)
        self.surf.set_alpha((220 + 20 * math.sin(self.age * 2)) * (self.health+30)/130)

        r = int((self.radius * 1.2 + 5 * math.sin(self.age * 2)) * (self.health + 50)/120)
        glow = pygame.Surface((r*2, r*2))
        pygame.draw.circle(glow, (200, 255, 215), (r, r), r)
        glow.set_alpha(60 * (self.health/100))
        glow.set_colorkey(c.BLACK)
        surface.blit(glow, (x - glow.get_width()//2, y - glow.get_height()//2))

        r = int((self.radius * 1.6 + 8 * math.sin(self.age * 2)) * (self.health + 50)/120)
        glow = pygame.Surface((r*2, r*2))
        pygame.draw.circle(glow, c.GREEN, (r, r), r)
        glow.set_alpha(30 * (self.health/100))
        glow.set_colorkey(c.BLACK)
        surface.blit(glow, (x - glow.get_width()//2, y - glow.get_height()//2))

        scale = int((self.health+30)/120 * self.surf.get_height())
        surf = pygame.transform.scale(self.surf, (scale, scale))
        surface.blit(surf, (x - surf.get_width()//2, y - surf.get_height()//2))
        self.draw_shield(surface)
        pass

    def die(self):
        self.dead = True
        for i in range(40):
            Spark(self.game, (self.x, self.y), c.WHITE, speed=800)

    def update_shield(self, dt):
        self.recoil *= 0.025**dt
        self.bonk_timer += dt
        d = self.shield_angle - self.shield_vis_angle
        d2 = self.shield_angle - self.shield_vis_angle + 360
        d3 = self.shield_angle - self.shield_vis_angle - 360
        true_d = d
        for item in [d2, d3]:
            if abs(item) < abs(true_d):
                true_d = item

        if self.shield_surf.get_alpha() < 255 and self.has_shield:
            self.shield_surf.set_alpha(min(255, self.shield_surf.get_alpha() + dt * 600))
            self.shield_bonk.set_alpha(self.shield_surf.get_alpha())
        if self.shield_surf.get_alpha() > 0 and not self.has_shield:
            self.shield_surf.set_alpha(max(0, self.shield_surf.get_alpha() - dt * 600))

        diff = 20*true_d*dt
        if true_d > 0:
            diff = min(diff, true_d)
        else:
            diff = max(diff, true_d)
        self.shield_vis_angle += diff

    def is_blocking(self, other):
        if not self.has_shield:
            return False
        a1 = other.direction
        a2 = self.shield_vis_angle
        d = a1 - a2
        d1 = a1 - a2 + 360
        d2 = a1 - a2 - 360
        for item in [d, d1, d2]:
            if abs(item) <= self.shield_spread//2:
                return True
        return False

    def draw_shield(self, surface):
        shield_surf = self.shield_surf if self.bonk_timer > self.bonk_time else self.shield_bonk
        if self.shield_surf.get_alpha() < 0:
            return
        ssurf = pygame.transform.rotate(shield_surf, self.shield_vis_angle)
        x = self.x - ssurf.get_width()//2
        y = self.y - ssurf.get_height()//2
        x, y = self.game.xy_transform(x, y)

        rad = self.shield_vis_angle * math.pi / 180
        xoff = int(self.recoil * -math.cos(rad))
        yoff = int(self.recoil * math.sin(rad))

        surface.blit(ssurf, (x + xoff, y + yoff))

    def update(self, dt, events):

        if self.mortal and self.health == 0:
            self.die()

        if self.health < 100:
            self.health += 7 * dt

        self.age += dt
        old = self.shield_angle
        for event in events:
            if event.type == pygame.KEYDOWN and self.has_shield and not self.dead and not self.move_disabled:
                if event.key == pygame.K_UP:
                    self.shield_angle = c.UP
                elif event.key == pygame.K_RIGHT:
                    self.shield_angle = c.RIGHT
                elif event.key == pygame.K_LEFT:
                    self.shield_angle = c.LEFT
                elif event.key == pygame.K_DOWN:
                    self.shield_angle = c.DOWN
        if self.shield_angle != old:
            self.game.change_direction_sound.play()

        self.update_shield(dt)
        self.shield_vis_angle %= 360