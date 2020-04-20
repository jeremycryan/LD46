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
        self.surf = pygame.transform.scale(self.surf, c.WINDOW_SIZE)
        font = pygame.font.Font(c.font_path("Myriad.otf"), 20)
        self.enter_surf = font.render("PRESS ENTER", 1, c.WHITE)
        self.thank_surf = pygame.image.load(c.image_path("thanks.png"))
        self.age = 0

    def main(self):
        self.game.load_tutorial_music()
        black = pygame.Surface(c.WINDOW_SIZE)
        black.fill(c.BLACK)
        black.set_alpha(255)
        done = False
        while True:
            dt, events = self.game.update_globals()
            self.age += dt
            if self.age < 0.4:
                self.surf.set_alpha(self.age * 800)
            elif self.age < 5.5:
                self.surf.set_alpha(255)

            if not done:
                black.set_alpha(max(0, black.get_alpha() - 1000 * dt))
            else:
                black.set_alpha(min(255, black.get_alpha() + 500 * dt))

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not done:
                        done = True
                        self.game.start_game_sound.play()
                        self.game.fade_out_music(800)

            if done and black.get_alpha() == 255:
                break

            self.game.screen.fill(c.BLACK)
            x = c.WINDOW_WIDTH//2 - self.surf.get_width()//2
            y = c.WINDOW_HEIGHT//2 - self.surf.get_height()//2
            self.game.screen.blit(self.surf, (x, y))
            if self.age % 1.2 < 0.6:
                self.game.screen.blit(self.enter_surf, (c.WINDOW_WIDTH//2 - self.enter_surf.get_width()//2, c.WINDOW_HEIGHT - 50))
            if self.game.has_played_before():
                self.game.screen.blit(self.thank_surf, (c.WINDOW_WIDTH//2 - self.thank_surf.get_width()//2, 120))
            self.game.screen.blit(black, (0, 0))
            pygame.display.flip()
        t = 0
        while True:
            dt, events = self.game.update_globals()
            self.game.screen.fill(c.BLACK)
            t += dt

            if t > 1:
                break
            pygame.display.flip()


class FadeIn(Scene):
    def initialize(self):
        pass

    def main(self):
        black = pygame.Surface(c.WINDOW_SIZE)
        black.set_alpha(255)
        while True:
            dt, events = self.game.update_globals()
            self.age += dt

            self.game.update_main_game_objects(dt, events)

            self.game.screen.fill(c.BLACK)
            self.game.player.draw(self.game.screen)
            black.set_alpha(black.get_alpha() - 255*dt)
            self.game.screen.blit(black, (0, 0))
            pygame.display.update()
            if self.age > 4:
                break

class Intro(Scene):

    def initialize(self):
        self.game.characters.append(CapeGuy(self.game))
        self.phase = 0
        self.music_has_played = False

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
            if self.phase == 1 and len(self.game.text_box.lines) < 5 and not self.music_has_played:
                self.game.load_tutorial_music()
                self.game.set_music_volume(0.6)
                self.music_has_played = True
            if self.phase == 1 and self.game.text_box.done():
                self.phase = 2
                self.age = 0
                self.game.enemies.append(TutorialEnemy(self.game, 3, c.RIGHT))
            if self.age > 3 and self.phase == 2:
                self.game.text_box.add_line("Not a pleasant experience, is it?")
                self.game.text_box.add_line("But you're already recovering to your former light.")
                self.game.text_box.add_line("A single byte won't destroy you, but collectively, they can bring even the hardiest pieces of software grinding to a halt.")
                self.game.text_box.add_line("Never let your glow get fully extinguished.")
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
                self.game.enemies.append(TutorialEnemy(self.game, 4, c.RIGHT))
                self.game.enemies.append(TutorialEnemy(self.game, 6, c.LEFT))
            if self.phase == 5 and not len(self.game.enemies):
                self.game.text_box.add_line("I think you're ready to explore this world on your own, young one.")
                self.game.text_box.add_line("Your arrival will not go unnoticed, so be wary.")
                self.game.text_box.add_line("I will observe your actions with interest.")
                self.phase = 6

            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)

            if self.game.text_box.done() and self.phase == 6:
                self.game.characters[0].target_alpha = 0
                self.game.fade_out_music(1200)
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
        period = 0.6
        distance = 2
        for i in range(10):
            direction = [c.UP, c.DOWN, c.LEFT, c.RIGHT][i % 4]
            distance += period
            self.game.enemies.append(Feint(self.game, distance, direction))
        distance += period * 2
        for i in range(8):
            direction = [c.LEFT, c.DOWN, c.UP, c.RIGHT][i % 4]
            distance += period * 0.8
            self.game.enemies.append(BlueEnemy(self.game, distance, direction))
        distance += period * 0.5
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
        period = 2.0
        distance = 2
        directions = [c.LEFT, c.RIGHT, c.LEFT, c.RIGHT, c.RIGHT, c.UP]
        for direction in directions:
            self.game.enemies.append(FastEnemy(self.game, distance, direction))
            distance += period


    def wave_5(self):
        period = 0.7
        distance = 3
        self.game.enemies.append(BlueEnemy(self.game, distance, c.UP))
        distance += period
        self.game.enemies.append(Feint(self.game, distance, c.DOWN))
        distance += period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.UP))
        distance += period
        self.game.enemies.append(FastEnemy(self.game, distance, c.LEFT))
        distance += period
        self.game.enemies.append(FastEnemy(self.game, distance, c.LEFT))
        distance += period
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))
        distance += period
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))
        distance += period * 2
        period = 1.0
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += period/2
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += period/2
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += period/4
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += period/4




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
                self.game.text_box.add_line("I can already taste the extra processing power.")
                self.phase = 4
            if self.phase == 4 and self.game.text_box.done():
                self.phase = 5
                self.wave_2()
            if len(self.game.enemies) == 0 and self.phase == 5:
                self.game.text_box.add_line("Do you like my g/ really fast attacks? /g")
                self.game.text_box.add_line("Don't blink!")
                self.phase = 6
            if self.phase == 6 and self.game.text_box.done():
                self.wave_4()
                self.phase = 7
            if self.phase == 7 and not len(self.game.enemies):
                self.phase = 8
                self.game.text_box.add_line("You're surprisingly well-equipped for a stray program.")
                self.game.text_box.add_line("Where did you get b/ that shield...? /b")
            if self.phase == 8 and self.game.text_box.done():
                self.wave_5()
                self.phase = 9
            if self.phase == 9 and not len(self.game.enemies):
                self.game.fade_out_music(300)
                self.game.text_box.add_line("What's that?")
                self.game.text_box.add_line("...")
                self.game.text_box.add_line("Oh no, y/ he /y is coming.")
                self.game.text_box.add_line("It's time for my exit.")
                self.phase = 10
            if self.phase == 10 and self.game.text_box.done():
                self.game.background.fade_out()
                for item in self.game.characters:
                    item.target_alpha = -300
                self.phase = 11

            if self.game.text_box.done() and self.phase == 11:
                break


class Level2(Scene):
    def initialize(self):
        self.game.characters = [Warden(self.game)]
        self.game.text_box.add_line("I've been looking for you.")
        self.game.text_box.add_line("Allow me to introduce myself.")
        self.game.text_box.add_line("You can call me y/ Warden. /y")
        self.game.text_box.add_line("It is my duty to confront the evil that wanders into this realm, capture it, and lock it away for good.")
        self.game.text_box.add_line("Some time ago, a r/ being of immense power /r escaped my watch.")
        self.game.text_box.add_line("And now, you have fallen under r/ her influence. /r")
        self.game.text_box.add_line("As such, I am forced to take up arms against you.")
        self.game.text_box.add_line("Prepare yourself. This is for your own good.")

    def wave1(self):
        self.game.background = self.game.ruins
        self.game.background.fade_in()
        self.game.set_music_volume(1.0)
        period = 0.5
        distance = 2
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

    def wave2(self):
        period = 0.4
        distance = 2.5
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))
        distance += period * 4
        self.game.enemies.append(Speedy(self.game, distance, c.LEFT))
        distance += period * 4
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))
        distance += period * 4
        self.game.enemies.append(Speedy(self.game, distance, c.DOWN))
        distance += period * 4
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))
        distance += period*2
        self.game.enemies.append(Speedy(self.game, distance, c.LEFT))
        distance += period*2
        self.game.enemies.append(Speedy(self.game, distance, c.UP))
        distance += period*2
        self.game.enemies.append(Speedy(self.game, distance, c.DOWN))
        distance += period*6
        for i in range(2):
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
            distance += period
        distance += period/2
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))
        distance += period*1
        self.game.enemies.append(Speedy(self.game, distance, c.DOWN))
        distance += period*1
        self.game.enemies.append(Speedy(self.game, distance, c.LEFT))
        distance += period*1
        self.game.enemies.append(Speedy(self.game, distance, c.UP))

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
                self.game.text_box.add_line("Otherwise, you're not just dooming yourself, you're dooming us all.")
            if self.phase == 2 and self.game.text_box.done():
                self.wave2()
                self.phase = 3
            if self.phase == 3 and len(self.game.enemies) == 0:
                self.phase = 4
                self.game.text_box.add_line("You don't understand.")
                self.game.text_box.add_line("You're doing exactly what r/ she /r wants.")
                self.game.text_box.add_line("You know nothing of this world.")
                self.game.text_box.add_line("You think this is just a game.")
                self.game.text_box.add_line("It's not.")
                self.game.text_box.add_line("You think you're safe behind your screen.")
                self.game.text_box.add_line("You're not.")
                self.game.text_box.add_line(f"Your \"real world\" isn't nearly as impervious as you think it is, y/ {self.game.real_name()}. /y", cps=18)
                self.game.text_box.add_line("And once r/ she /r has her way with our world, you've given her an open door to access yours.")
                self.game.text_box.add_line("y/ Don't let her win. /y", cps=10)
            if self.phase == 4 and self.game.text_box.done():
                self.phase = 5
                self.game.characters[0].slash()
                self.game.fade_out_music(200)
                self.game.background.fade_out()
            if self.phase == 5 and not len(self.game.characters):
                break


class Level3(Scene):
    def initialize(self):
        self.game.characters = [CapeGuy(self.game)]
        self.game.text_box.add_line("Hello again.")
        self.game.text_box.add_line("Thank you for the distraction. y/ He /y was really starting to become a threat.")
        self.game.text_box.add_line("Now the only thing standing between me and unbounded influence...")
        self.game.text_box.add_line("...is you.")
        self.game.text_box.add_line(f"It pains me to tell you this, r/ {self.game.real_name()}, /r but I'm going to have to kill you.")
        self.game.text_box.add_line("That script... er, \"shield\"... I gifted you has not only been keeping your familiar alive in this world, but has been laying roots in your own world as well.")
        self.game.text_box.add_line("It's surprisingly easy to disguise a virus as a video game.")
        self.game.text_box.add_line("It only takes a few minutes to identify vulnerabilities and start to worm through them.")
        self.game.text_box.add_line("And if I win here, you won't be able to stop me.")
        self.game.text_box.add_line("I'm no longer confined to this virtual world.")
        self.game.text_box.add_line("Soon, I won't even be confined to your computer.")
        self.game.text_box.add_line("If I can escape the network, I'll be able to spread my influence to the ends of the earth.")
        self.game.text_box.add_line("r/ Think you can stop me? Prove it. /r")

    def wave_1(self):
        distance = 4
        period = 0.55
        self.game.enemies.append(BlueEnemy(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.RIGHT))

        distance += period * 2.0
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))

        distance += period * 2.0
        self.game.enemies.append(Spinny(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.UP))

        distance += period * 0.5
        self.game.enemies.append(FastEnemy(self.game, distance, c.UP))
        distance += period * 0.25
        self.game.enemies.append(FastEnemy(self.game, distance, c.UP))
        distance += period * 0.25
        self.game.enemies.append(FastEnemy(self.game, distance, c.UP))
        distance += period * 0.25
        self.game.enemies.append(FastEnemy(self.game, distance, c.UP))

        distance += period * 2.0
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))
        distance += period * 0.25
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))
        distance += period * 0.25
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))
        distance += period * 0.25
        self.game.enemies.append(FastEnemy(self.game, distance, c.RIGHT))


    def wave_2(self):
        distance = 2
        period = 1.0
        self.game.enemies.append(Speedy(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(Speedy(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(Speedy(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(Speedy(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(Speedy(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))

        distance += 2 * period
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.UP))
        distance += 1.0 * period
        self.game.enemies.append(Speedy(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.DOWN))
        distance += 1.0 * period
        self.game.enemies.append(Speedy(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(Feint(self.game, distance, c.LEFT))
        distance += 1.0 * period
        self.game.enemies.append(Feint(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(Speedy(self.game, distance, c.LEFT))

        distance += 1.5 * period
        distance += period * 2.0
        period = 0.8
        self.game.enemies.append(Spinny(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.UP, counterclockwise=True))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.DOWN, counterclockwise = True))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.LEFT, counterclockwise = True))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.RIGHT, counterclockwise = True))
        distance += 0.5 * period
        self.game.enemies.append(Spinny(self.game, distance, c.DOWN))

        distance += 2 * period
        period = 0.55
        self.game.enemies.append(BlueEnemy(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.UP))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.RIGHT))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.DOWN))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.LEFT))
        distance += 0.5 * period
        self.game.enemies.append(BlueEnemy(self.game, distance, c.UP))

    def wave_3(self):
        types = [BlueEnemy, Spinny, FastEnemy, Speedy, Feint]
        directions = c.DIRECTIONS

        period = 1.0
        distance = 3
        for i in range(70):
            enemy = random.choice(types)
            direction = random.choice(directions)
            self.game.enemies.append(enemy(self.game, distance, direction))
            distance += period
            period *= 0.98

    def main(self):
        self.game.player.has_shield = True
        music_has_started = False
        self.phase = 0
        self.shutdown_timer = 0.5
        while True:
            dt, events = self.game.update_globals()

            self.game.update_main_game_objects(dt, events)
            self.game.draw_main_game_objects(self.game.screen)

            if len(self.game.text_box.lines) < 2 and not music_has_started:
                self.game.load_parity_music()
                self.game.set_music_volume(1.0)
                music_has_started = True
            if self.phase == 0 and self.game.text_box.done():
                self.game.background = self.game.dungeon
                self.game.background.fade_in()
                self.phase = 1
                self.wave_1()
            if self.phase == 1 and len(self.game.enemies) == 0:
                self.game.text_box.add_line(f"Give up, r/ {self.game.real_name()}. /r")
                self.game.text_box.add_line("There's nothing you can do to stop me.")
                self.game.text_box.add_line("If I really wanted you to succeed in this world, I would have given you a weapon, not that sorry instrument.")
                self.phase = 2
            if self.phase == 2 and self.game.text_box.done():
                self.wave_2()
                self.phase = 3
            if self.phase == 3 and not len(self.game.enemies):
                self.game.text_box.add_line("Don't think you're special for having survived this long.")
                self.game.text_box.add_line("The only think saving you is that I've been playing by the rules.")
                self.game.text_box.add_line("Let's see how you fare r/ without that shield. /r")
                self.phase = 4
            if self.phase == 4 and self.game.text_box.done():
                self.phase = 5
                self.game.player.has_shield = False
                distance = 1
                for i in range(5):
                    self.game.enemies.append(FastEnemy(self.game, distance, c.UP))
                    distance += 0.2
            if self.phase == 5 and not len(self.game.enemies):
                self.game.text_box.add_line("See? Brink of death in an instant.")
                self.game.text_box.add_line("I have more authority over this world than you can ever hope to.")
                self.game.text_box.add_line("Soon you'll be only a passenger in your own world as well.")
                self.game.text_box.add_line("Take back your shield. I like to see the reaction when hope gives way to despair.")
                self.game.text_box.add_line("This marks my final attack.")
                self.game.text_box.add_line(f"Withstand this barrage, and I'll let you go, r/ {self.game.real_name()}. /r")
                self.game.text_box.add_line("r/ If you die now, I'm taking over your computer. /r", cps=18)
                self.phase = 6
            if self.phase == 6 and len(self.game.text_box.lines) <= 4:
                self.game.player.has_shield = True
            if self.phase == 6 and self.game.text_box.done():
                self.wave_3()
                self.game.player.mortal = True
                self.phase = 7
            if self.phase == 7 and self.game.player.dead:
                for enemy in self.game.enemies[::-1]:
                    enemy.destroy()
            if self.phase == 7 and not len(self.game.enemies):
                self.game.text_box.add_line("How unfortunate.")
                self.game.text_box.add_line(f"Goodbye, r/ {self.game.real_name()}. /r")
                self.game.text_box.add_line("I'm corrupting your machine as we speak.")
                self.game.text_box.add_line(f"Soon_I_{'&r/gi6u53H$@F(F))(!#$J(JA(BJ)ER)(BJ)(#$!GU)$(GJ(RB)EH(#)!JG)(VWJRB()#HNW!V)N#)(JG(#$)'*5}", cps=250)
                self.phase = 8
            if self.phase == 8 and len(self.game.text_box.lines) <= 1:
                self.shutdown_timer -= dt
            if self.shutdown_timer <= 0:
                self.game.shutdown()
