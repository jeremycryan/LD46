import pygame
import constants as c
from enemy import *
from character import *


class Scene:
    def __init__(self, game):
        self.game = game
        self.age = 0
        self.initialize()
        self.main()

    def initialize(self):
        pass

    def main(self):
        pass


class Intro(Scene):

    def initialize(self):
        self.game.characters.append(CapeGuy(self.game))
        self.phase = 0

    def main(self):
        while True:
            dt, events = self.game.update_globals()

            self.age += dt
            if self.age > 2 and self.phase == 0:
                self.game.text_box.add_line("What have we here?")
                self.game.text_box.add_line("Few programs venture this deep, but you're of a different sort, aren't you?")
                self.game.text_box.add_line("From *the* *land* *beyond,* perhaps?")
                self.game.text_box.add_line("No matter. As a lost soul, you must be in need of guidance.")
                self.game.text_box.add_line("You can call me *Parity.*")
                self.game.text_box.add_line("I serve as a peacekeeper of sorts, purging this world of... irregularities.")
                self.game.text_box.add_line("Let me acquaint you with a single byte of *corruption.*")
                self.phase = 1
            if self.phase == 1 and self.game.text_box.done():
                self.phase = 2
                self.age = 0
                self.game.enemies.append(Enemy(self.game, 3, c.RIGHT))
            if self.age > 3 and self.phase == 2:
                self.game.text_box.add_line("Not a pleasant experience, is it?")
                self.game.text_box.add_line("A single byte won't destroy you, but collectively, they can bring even the hardiest pieces of software grinding to a halt.")
                self.game.text_box.add_line("Luckily, there is a way to defend yourself, young one.")
                self.phase = 3
            if self.phase == 3 and self.game.text_box.done():
                self.game.player.has_shield = True
                self.game.text_box.add_line("This shield will safeguard you from most threats.")
                self.game.text_box.add_line("You can change its direction with *the* *arrow* *keys.*")
                self.phase = 4
            if self.phase == 4 and self.game.text_box.done():
                self.phase = 5
                self.age = 0
                self.game.enemies.append(Enemy(self.game, 3, c.RIGHT))
                self.game.enemies.append(Enemy(self.game, 4.5, c.LEFT))
            if self.phase == 5 and self.age > 4.5:
                self.game.text_box.add_line("I think you're ready to explore this world on your own, young one.")
                self.game.text_box.add_line("I will observe your actions with great interest.")
                self.phase = 6

            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)

            if self.game.text_box.done() and self.phase == 6:
                self.game.characters[0].target_alpha = 0
                break


class Level1(Scene):

    def initialize(self):
        self.game.characters.append(Tetroid(self.game))
        self.game.player.has_shield = True
        self.phase = 0

        self.game.text_box.add_line("ahhhhhhhhhh murder")

    def wave_1(self):
        for i in range(5):
            direction = c.DIRECTIONS[i % 4]
            distance = i + 3
            self.game.enemies.append(Enemy(self.game, distance, direction))

    def main(self):
        while True:
            dt, events = self.game.update_globals()

            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)

            if self.phase == 0 and self.game.text_box.done():
                self.wave_1()
                self.phase = 1


            if len(self.game.enemies) == 0 and self.phase == 3:
                break

class Interlude1(Scene):

    def initialize(self):
        self.game.text_box.add_line("There's more!")

    def main(self):
        while True:
            dt, events = self.game.update_globals()

            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)

            if self.game.text_box.done():
                break

class Level2(Level1):
    def initialize(self):
        for i in range(5):
            direction = c.DIRECTIONS[i % 4]
            distance = i + 3
            self.game.enemies.append(FastEnemy(self.game, distance, direction))

    def main(self):
        while True:
            dt, events = self.game.update_globals()

            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)

            if len(self.game.enemies) == 0:
                break
