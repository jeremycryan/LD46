import pygame
import sys
import math
import getpass
import constants as c
from player import Player
from enemy import Enemy, FastEnemy
from scene import *
from text_box import TextBox


class Game:
    pass

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(c.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.reset()
        self.main()

    def reset(self):
        self.player = Player(self)
        self.enemies = []
        self.characters = []
        self.text_box = TextBox(self)

        self.shake_amp = 0
        self.since_shake = 0

    def main(self):
        Intro(self)
        Level1(self)
        Interlude1(self)
        Level2(self)

    def real_name(self):
        return getpass.getuser()

    def shake(self, amt):
        self.since_shake = 0
        self.shake_amp = max(self.shake_amp, amt)

    def xy_transform(self, x, y):
        x += self.shake_amp * math.cos(self.since_shake * 2 * math.pi * 10)
        y += self.shake_amp * math.cos(self.since_shake * 2 * math.pi * 10)
        return int(x), int(y)

    def update_effects(self, dt, events):
        self.since_shake += dt
        self.shake_amp *= 0.1**dt
        self.shake_amp = max(0, self.shake_amp - 15*dt)

    def update_main_game_objects(self, dt, events):
        self.player.update(dt, events)
        for enemy in self.enemies:
            enemy.update(dt, events)
        for character in self.characters:
            character.update(dt, events)
        self.text_box.update(dt, events)
        self.update_effects(dt, events)

    def draw_main_game_objects(self, surface):
        self.screen.fill(c.BLACK)
        self.player.draw(self.screen)
        for character in self.characters:
            character.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.text_box.draw(self.screen)
        self.update_screen()

    def update_globals(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        dt = self.clock.tick(c.FPS)/1000
        return dt, events

    def update_screen(self):
        pygame.display.flip()

    def shutdown(self):
        print("YOUR COMPUTE OFF NOW")
        pygame.quit()
        sys.exit()


if __name__=="__main__":
    Game()