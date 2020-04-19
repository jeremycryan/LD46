import pygame
import constants as c
import random
import math



class Particle:

    def __init__(self, game, position):
        self.x, self.y = position
        if self.x > c.WINDOW_WIDTH + 200 or self.x < -200 or self.y > c.WINDOW_HEIGHT + 200 or self.y < -200:
            return
        game.particles.append(self)
        self.game = game

    def update(self, dt, events):
        pass

    def draw(self, surface):
        pass

    def destroy(self):
        if self in self.game.particles:
            self.game.particles.remove(self)


class Bit(Particle):

    surfs = []

    def __init__(self, game, position, color=c.WHITE):
        super().__init__(game, position)
        self.alpha = 255

        self.body_font = pygame.font.Font(c.font_path("Myriad.otf"), 12)
        char = random.choice(["0", "1"])
        self.surf = self.body_font.render(char, 0, color).convert()

    def update(self, dt, events):
        self.alpha -= 400 * dt
        if self.alpha <= 0:
            self.destroy()

        if self.x < -200 or self.x > c.WINDOW_WIDTH + 200:
            self.destroy()
        if self.y < -200 or self.y > c.WINDOW_HEIGHT + 200:
            self.destroy()

    def draw(self, surface):
        x, y = self.game.xy_transform(self.x, self.y)
        x -= self.surf.get_width()//2
        y -= self.surf.get_height()//2
        self.surf.set_alpha(self.alpha)
        surface.blit(self.surf, (x, y))


class Spark(Particle):

    def __init__(self, game, position, color=c.WHITE, width=3, speed=100, fade=600):
        super().__init__(game, position)
        self.alpha = 255
        self.direction = random.random() * 360
        self.speed = random.random() * speed
        self.width = width
        self.surf = pygame.Surface((width, width))
        self.surf.fill(color)
        self.fade = fade

    def update(self, dt, events):
        self.alpha -= self.fade * dt
        if self.alpha <= 0:
            self.destroy()

        self.x += self.speed * dt * math.cos(self.direction * math.pi/180)
        self.y += -self.speed * dt * math.sin(self.direction * math.pi/180)

    def draw(self, surface):
        x, y = self.game.xy_transform(self.x, self.y)
        x -= self.surf.get_width()//2
        y -= self.surf.get_height()//2
        self.surf.set_alpha(self.alpha)
        surface.blit(self.surf, (x, y))


class SpeedyFlash(Particle):

    def __init__(self, game, direction, duration = 0.2):
        y = c.WINDOW_HEIGHT//2
        x = c.WINDOW_WIDTH//2
        if direction == c.LEFT:
            x = 0
        elif direction == c.RIGHT:
            x = c.WINDOW_WIDTH
        elif direction == c.UP:
            y = 0
        elif direction == c.DOWN:
            y = c.WINDOW_HEIGHT
        super().__init__(game, (x, y))
        self.age = 0
        self.duration = duration
        self.radius = 40
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(self.surf, c.PURPLE, (self.radius, self.radius), self.radius)
        self.surf.set_colorkey(c.BLACK)


    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt
        if self.age > self.duration:
            self.destroy()
        else:
            prop = (self.duration - self.age)/self.duration
            self.surf.set_alpha(prop * 150)
            self.radius = (1 - prop) * 100 + 40

    def draw(self, surface):
        prev_alpha = self.surf.get_alpha()
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(self.surf, c.PURPLE, (int(self.radius), int(self.radius)), int(self.radius))
        self.surf.set_colorkey(c.BLACK)
        self.surf.set_alpha(prev_alpha)

        x, y = self.game.xy_transform(self.x, self.y)
        x -= self.surf.get_width()//2
        y -= self.surf.get_height()//2
        surface.blit(self.surf, (x, y))