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


class StarFish(Scene):
    def initialize(self):
        self.fish = pygame.image.load(c.image_path("logo.png"))
        self.fish = pygame.transform.scale(self.fish, (self.fish.get_width() * 2, self.fish.get_height() * 2))

    def main(self):
        while True:
            dt, events = self.game.update_globals()
            self.age += dt
            if self.age < 0.4:
                self.fish.set_alpha(self.age * 800)
            elif self.age < 2.0:
                self.fish.set_alpha(255)
            else:
                self.fish.set_alpha(self.fish.get_alpha() - 800 * dt)
            if self.age > 2.8:
                break

            self.game.screen.fill(c.BLACK)
            x = c.WINDOW_WIDTH//2 - self.fish.get_width()//2
            y = c.WINDOW_HEIGHT//2 - self.fish.get_height()//2
            self.game.screen.blit(self.fish, (x, y))
            pygame.display.flip()


class Disclaimer(Scene):
    def initialize(self):
        self.surf = pygame.image.load(c.image_path("disclaimer.png"))
        self.surf = pygame.transform.scale(self.surf, (self.surf.get_width() * 2, self.surf.get_height() * 2))

    def main(self):
        while True:
            dt, events = self.game.update_globals()
            self.age += dt
            if self.age < 0.4:
                self.surf.set_alpha(self.age * 800)
            elif self.age < 5.5:
                self.surf.set_alpha(255)
            else:
                self.surf.set_alpha(self.surf.get_alpha() - 800 * dt)
            if self.age > 6.5:
                break

            self.game.screen.fill(c.BLACK)
            x = c.WINDOW_WIDTH//2 - self.surf.get_width()//2
            y = c.WINDOW_HEIGHT//2 - self.surf.get_height()//2
            self.game.screen.blit(self.surf, (x, y))
            pygame.display.flip()


class Title(Scene):
    def initialize(self):
        self.surf = pygame.image.load(c.image_path("title.png"))

    def main(self):
        while True:
            dt, events = self.game.update_globals()
            self.age += dt
            if self.age < 0.4:
                self.surf.set_alpha(self.age * 800)
            elif self.age < 5.5:
                self.surf.set_alpha(255)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.game.screen.fill(c.BLACK)
            x = c.WINDOW_WIDTH//2 - self.surf.get_width()//2
            y = c.WINDOW_HEIGHT//2 - self.surf.get_height()//2
            self.game.screen.blit(self.surf, (x, y))
            pygame.display.flip()


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
                self.game.text_box.add_line("From r/ the land beyond, /r perhaps?")
                self.game.text_box.add_line("...")
                self.game.text_box.add_line("No matter.")
                self.game.text_box.add_line("As a lost traveler, you must be in need of guidance.")
                self.game.text_box.add_line("You can call me r/ Parity. /r")
                self.game.text_box.add_line("I serve as a peacekeeper of sorts, purging this world of... irregularities.")
                self.game.text_box.add_line("This place is home to many hazards that warrant protection.")
                self.game.text_box.add_line("Let me acquaint you with a single byte of r/ corruption. /r")
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
                self.game.text_box.add_line("You can change its direction with r/ the arrow keys. /r")
                self.phase = 4
            if self.phase == 4 and self.game.text_box.done():
                self.phase = 5
                self.age = 0
                self.game.enemies.append(Enemy(self.game, 4, c.RIGHT))
                self.game.enemies.append(Enemy(self.game, 6, c.LEFT))
            if self.phase == 5 and not len(self.game.enemies):
                self.game.text_box.add_line("I think you're ready to explore this world on your own, young one.")
                self.game.text_box.add_line("Your arrival will not go unnoticed, so be wary.")
                self.game.text_box.add_line("I will observe your actions with interest.")
                self.phase = 6

            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)

            if self.game.text_box.done() and self.phase == 6:
                self.game.characters[0].target_alpha = 0
                break


class Pause(Scene):
    def __init__(self, game, duration):
        self.duration = duration
        super().__init__(game)

    def main(self):
        while True:
            dt, events = self.game.update_globals()
            self.age += dt
            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)
            if self.age > self.duration:
                break


class Level1(Scene):

    def initialize(self):
        self.game.characters.append(Tetroid(self.game))
        self.game.player.has_shield = True
        self.phase = 0

        self.game.text_box.add_line("Why hello, little morsel.")
        self.game.text_box.add_line("Now that r/ she's /r gone, I have you all to myself.")
        self.game.text_box.add_line("Once I've corrupted your core, I can absorb your processing power and bolster my own strength.")
        self.game.text_box.add_line("Do try to flee... it only adds to the fun.")

        self.game.load_hedroid_music()
        self.game.set_music_volume(0.2)

    def wave_1(self):
        self.game.set_music_volume(1.0)
        self.game.background = self.game.caves
        self.game.background.fade_in()
        period = 1.0
        for i in range(4):
            direction = c.DIRECTIONS[i % 4]
            distance = i * period + 3 * period
            self.game.enemies.append(BlueEnemy(self.game, distance, direction))

    def wave_1p5(self):

        period = 0.75
        distance = 1.5
        directions = [c.UP, c.DOWN, c.RIGHT, c.LEFT]
        for i in range(4):
            direction = directions[i]
            self.game.enemies.append(Feint(self.game, distance, direction))
            distance += period * 2

        for i in range(4):
            direction = c.DIRECTIONS[i]
            other_direction = c.DIRECTIONS[(i+2) % 4]
            self.game.enemies.append(BlueEnemy(self.game, distance, direction))
            distance += period * 0.5
            self.game.enemies.append(Feint(self.game, distance, other_direction))
            distance += period * 1.5

    def wave_2(self):
        period = 0.7
        distance = 0
        for i in range(8):
            direction = [c.UP, c.DOWN, c.LEFT, c.RIGHT][i % 4]
            distance = i * period + 4 * period
            self.game.enemies.append(BlueEnemy(self.game, distance, direction))
        self.game.enemies.append(FastEnemy(self.game, distance + 0.5*period, c.LEFT))


    def wave_3(self):
        period = 0.7
        distance = 2
        directions = [c.UP, c.RIGHT, c.DOWN, c.LEFT, c.UP, c.LEFT, c.DOWN, c.RIGHT]
        for i in range(8):
            direction = directions[i]
            distance += period
            ccw = (i % 2 == 0)
            self.game.enemies.append(Spinny(self.game, distance, direction, counterclockwise=ccw))
        distance += period * 2
        for i in range(8):
            direction = directions[i]
            distance += period
            ccw = (i % 2 == 0)
            self.game.enemies.append(Spinny(self.game, distance, direction, counterclockwise=ccw))

        distance += period * 2

        self.game.enemies.append(FastEnemy(self.game, distance + 0.5*period, c.DOWN))
        self.game.enemies.append(FastEnemy(self.game, distance + 0.75 * period, c.DOWN))
        self.game.enemies.append(FastEnemy(self.game, distance + 1 * period, c.DOWN))


    def wave_4(self):
        period = 0.6
        distance = 2
        directions = [c.UP, c.DOWN, c.LEFT, c.RIGHT, c.LEFT, c.RIGHT]
        for direction in directions:
            distance += period
            self.game.enemies.append(Speedy(self.game, distance, direction))

    def main(self):
        while True:
            dt, events = self.game.update_globals()

            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)

            if self.phase == 0 and self.game.text_box.done():
                self.wave_1()
                self.phase = 1
            if self.phase == 1 and not len(self.game.enemies):
                self.game.text_box.add_line("Ah, you come prepared!")
                self.game.text_box.add_line("See if you can handle my more b/ elusive attacks... /b")
                self.phase = 2
            if self.phase == 2 and self.game.text_box.done():
                self.phase = 3
                self.wave_1p5()
            if self.phase == 3 and not len(self.game.enemies):
                self.game.text_box.add_line("That's enough cat and mouse.")
                self.game.text_box.add_line("Let's see you fight for your life!")
                self.phase = 4
            if self.phase == 4 and self.game.text_box.done():
                self.phase = 5
                self.wave_2()
            if len(self.game.enemies) == 0 and self.phase == 5:
                self.game.text_box.add_line("i am defeat")
                self.game.background.fade_out()
                for item in self.game.characters:
                    item.target_alpha = -300
                self.phase = 6
            if self.game.text_box.done() and self.phase == 6:
                self.game.fade_out_music(500)
                break


class Level2(Scene):
    def initialize(self):
        self.game.characters = [Warden(self.game)]
        self.game.text_box.add_line("At last, we meet.")
        self.game.text_box.add_line("Allow me to introduce myself.")
        self.game.text_box.add_line("You can call me y/ Warden. /y")
        self.game.text_box.add_line("It is my duty to confront the evil that wanders into this realm, capture it, and lock it away for good.")
        self.game.text_box.add_line("Some time ago, a r/ being of immense power /r escaped my watch.")
        self.game.text_box.add_line("And now, you have fallen under her influence.")
        self.game.text_box.add_line("As such, I am forced to take up arms against you.")
        self.game.text_box.add_line("Prepare yourself. This is for your own good.")

    def wave1(self):
        self.game.background = self.game.ruins
        self.game.background.fade_in()
        self.game.set_music_volume(1.0)
        period = 0.5
        distance = 1
        self.game.enemies.append(FastEnemy(self.game, distance, c.LEFT))
        distance += 0.25*period
        self.game.enemies.append(FastEnemy(self.game, distance, c.LEFT))
        distance += 0.25 * period
        self.game.enemies.append(FastEnemy(self.game, distance, c.LEFT))
        distance += 1.0 * period
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))
        distance += 0.25*period
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))
        distance += 0.25 * period
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))
        distance += 5 * period

        directions = [c.UP, c.RIGHT, c.LEFT, c.DOWN, c.UP, c.LEFT, c.DOWN, c.UP]
        for i in range(8):
            direction = directions[i]
            distance += period
            ccw = (i % 2 == 0)
            self.game.enemies.append(Spinny(self.game, distance, direction, counterclockwise=ccw))
        distance += period * 2
        for i in range(8):
            direction = directions[i]
            distance += period
            ccw = (i % 2 == 0)
            self.game.enemies.append(Spinny(self.game, distance, direction, counterclockwise=ccw))

        distance += 0.5 * period
        self.game.enemies.append(FastEnemy(self.game, distance, c.DOWN))
        distance += 0.25*period
        self.game.enemies.append(FastEnemy(self.game, distance, c.DOWN))
        distance += 0.25 * period
        self.game.enemies.append(FastEnemy(self.game, distance, c.DOWN))
        distance += 1.5 * period

        self.game.enemies.append(Speedy(self.game, distance, c.LEFT))
        distance += period
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))
        distance += period
        self.game.enemies.append(Speedy(self.game, distance, c.UP))
        distance += period
        self.game.enemies.append(Speedy(self.game, distance, c.DOWN))
        distance += period
        self.game.enemies.append(Speedy(self.game, distance, c.LEFT))
        distance += period*1.5
        self.game.enemies.append(RedEnemy(self.game, distance, c.RIGHT))


    def wave2(self):
        period = 0.4
        distance = 2
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))
        distance += period*2
        self.game.enemies.append(FastEnemy(self.game, distance, c.LEFT))
        distance += period*8
        self.game.enemies.append(BlueEnemy(self.game, distance, c.RIGHT))
        distance += period
        self.game.enemies.append(Spinny(self.game, distance, c.LEFT))
        distance += period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.UP))
        distance += period
        self.game.enemies.append(Spinny(self.game, distance, c.RIGHT))
        distance += period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.LEFT))
        distance += period
        self.game.enemies.append(Spinny(self.game, distance, c.DOWN))
        distance += period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.DOWN))
        distance += period
        self.game.enemies.append(Spinny(self.game, distance, c.UP))

    def main(self):
        self.phase = 0
        self.game.player.has_shield = True
        music_has_started = False
        while True:
            dt, events = self.game.update_globals()

            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)

            if len(self.game.text_box.lines) < 7 and not music_has_started:
                self.game.load_warden_music()
                self.game.set_music_volume(0.15)
                music_has_started = True

            if self.game.text_box.done() and self.phase == 0:
                self.phase = 1
                self.wave1()
            if self.phase == 1 and len(self.game.enemies) == 0:
                self.phase = 2
                self.game.text_box.add_line("Your defeat is inevitable.")
                self.game.text_box.add_line("y/ Accept it. /y")
            if self.phase == 2 and self.game.text_box.done():
                self.wave2()
                self.phase = 3
            if self.phase == 3 and len(self.game.enemies) == 0:
                self.phase = 4
                self.game.text_box.add_line("You don't understand.")
                self.game.text_box.add_line("You're doing exactly what r/ she /r wants.")
                self.game.text_box.add_line("You know nothing of this world.")
                self.game.text_box.add_line("You think this is just a game. It's not.")
                self.game.text_box.add_line("You think you're safe behind your screen. You're not.")
                self.game.text_box.add_line(f"Your \"real world\" isn't nearly as impervious as you think it is, y/ {self.game.real_name()}. /y", cps=18)
                self.game.text_box.add_line("And once r/ she /r has her way with our world, you've given her an open door to access yours.")
                self.game.text_box.add_line("y/ STAND DOWN. /y", cps=10)



class Level4(Scene):
    pass