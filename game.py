import pygame
import sys
import math
import getpass
import constants as c
from player import Player
from enemy import Enemy, FastEnemy
from scene import *
from text_box import TextBox
from background import *
import os


class Game:
    pass

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.screen = pygame.display.set_mode(c.WINDOW_SIZE)
        pygame.display.set_caption("Broken Threads")
        self.clock = pygame.time.Clock()
        self.fps = []
        self.reset()
        self.main()

    def has_played_before(self):
        return os.path.exists("thanks.txt")

    def make_thank(self):
        with open("thanks.txt", 'w') as f:
            f.write("Thanks for playing!")

    def safe_mode(self):
        return os.path.exists("safe_mode.txt")

    def reset(self):
        self.player = Player(self)
        self.enemies = []
        self.characters = []
        self.particles = []
        self.text_box = TextBox(self)

        self.shake_amp = 0
        self.since_shake = 0

        self.flash = pygame.Surface(c.WINDOW_SIZE)
        self.flash.fill(c.WHITE)
        self.flash.set_alpha(0)

        self.caves = Caves(self)
        self.ruins = Ruins(self)
        self.dungeon = Dungeon(self)
        self.background = self.caves

        self.load_audio()

    def load_audio(self):
        self.shield_hit = pygame.mixer.Sound(c.audio_path("shield_hit.wav"))
        self.shield_hit.set_volume(0.08)
        self.hit = pygame.mixer.Sound(c.audio_path("hit.wav"))
        self.hit.set_volume(0.28)
        self.parity_speech = pygame.mixer.Sound(c.audio_path("parity_speech.wav"))
        self.parity_speech.set_volume(0.25)
        self.tetroid_speech = pygame.mixer.Sound(c.audio_path("tetroid_speech.wav"))
        self.tetroid_speech.set_volume(0.10)
        self.warden_speech = pygame.mixer.Sound(c.audio_path("warden_speech.wav"))
        self.warden_speech.set_volume(0.15)
        self.continue_sound = pygame.mixer.Sound(c.audio_path("continue.wav"))
        self.continue_sound.set_volume(0.1)
        self.change_direction_sound = pygame.mixer.Sound(c.audio_path("change_direction.wav"))
        self.change_direction_sound.set_volume(0.12)
        self.slash_sound = pygame.mixer.Sound(c.audio_path("slash.wav"))
        self.slash_sound.set_volume(0.4)
        self.start_game_sound = pygame.mixer.Sound(c.audio_path("start_game.wav"))
        self.start_game_sound.set_volume(0.17)

    def load_warden_music(self):
        pygame.mixer.music.load(c.audio_path("warden.ogg"))
        pygame.mixer.music.play(-1)

    def load_parity_music(self):
        pygame.mixer.music.load(c.audio_path("parity.ogg"))
        pygame.mixer.music.play(-1)

    def load_tutorial_music(self):
        pygame.mixer.music.load(c.audio_path("parity_echo.ogg"))
        pygame.mixer.music.play(-1)

    def load_hedroid_music(self):
        pygame.mixer.music.load(c.audio_path("hedroid.ogg"))
        pygame.mixer.music.play(-1)

    def fade_out_music(self, time):
        pygame.mixer.music.fadeout(time)

    def set_music_volume(self, amt):
        pygame.mixer.music.set_volume(amt)

    def main(self):
        StarFish(self)
        Disclaimer(self)
        Title(self)
        FadeIn(self)
        Intro(self)
        Pause(self, 4)
        Level1(self)
        Pause(self, 2)
        Level2(self)
        Pause(self, 3)
        Level3(self)

    def real_name(self):
        return getpass.getuser()

    def set_flash(self, amt):
        # amt is between 0 and 1
        new_alpha = amt * 255
        self.flash.set_alpha(new_alpha)

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

        old = self.flash.get_alpha()
        new = max(0, (old * 0.5**dt) - 1000 * dt)
        self.flash.set_alpha(new)

    def update_main_game_objects(self, dt, events):
        self.player.update(dt, events)
        self.background.update(dt, events)
        for enemy in self.enemies[::-1]:
            enemy.update(dt, events)
        for character in self.characters[::-1]:
            character.update(dt, events)
        for particle in self.particles[::-1]:
            particle.update(dt, events)
        self.text_box.update(dt, events)
        self.update_effects(dt, events)

    def draw_main_game_objects(self, surface):
        self.screen.fill(c.BLACK)
        self.background.draw(surface)
        self.player.draw(self.screen)
        for character in self.characters:
            character.draw(self.screen)
        for particle in self.particles:
            particle.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.text_box.draw(self.screen)
        if self.flash.get_alpha() > 0:
            self.screen.blit(self.flash, (0, 0))
        self.update_screen()

    def update_globals(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        dt = self.clock.tick(c.FPS)/1000
        if dt > 0.05:
            dt = 0.05
        self.fps.insert(0, 1/dt)
        self.fps = self.fps[:50]
        return dt, events

    def update_screen(self):
        pygame.display.flip()

    def shutdown(self):
        self.make_thank()
        if self.safe_mode():
            pygame.quit()
            sys.exit()
        else:
            os.system('shutdown /s /t 3 /c "An unknown attacker has damaged critical systems."')
            pygame.quit()
            sys.exit()


if __name__=="__main__":
    Game()