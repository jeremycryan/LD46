import pygame
import constants as c


class TextBox:

    def __init__(self, game):
        self.game = game
        self.lines = []
        self.characters_per_second = 80
        self.advance_arrow = pygame.image.load(c.image_path("advance_arrow.png"))
        self.body_font = pygame.font.Font(c.font_path("Myriad.otf"), 20)
        self.enter_font = pygame.font.Font(c.font_path("Myriad.otf"), 12)
        self.chars = {char:self.body_font.render(char, 0, c.WHITE) for char in c.PRINTABLE_CHARS}
        self.red_chars = {char:self.body_font.render(char, 0, c.RED) for char in c.PRINTABLE_CHARS}
        self.blue_chars = {char:self.body_font.render(char, 0, c.BLUE) for char in c.PRINTABLE_CHARS}
        self.green_chars = {char:self.body_font.render(char, 0, c.GREEN) for char in c.PRINTABLE_CHARS}
        self.yellow_chars = {char:self.body_font.render(char, 0, c.YELLOW) for char in c.PRINTABLE_CHARS}
        self.highlight_chars = {char:self.body_font.render(char, 0, (255, 60, 60)) for char in c.PRINTABLE_CHARS}
        self.width = 500
        self.height = 140
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        self.surf.set_alpha(25)
        self.x = c.WINDOW_WIDTH//2
        self.y = c.WINDOW_HEIGHT - self.height//2 - 50
        self.active_character = None
        self.enter_to_continue = self.enter_font.render("ENTER TO CONTINUE", 0, c.WHITE)
        self.enter_to_continue.set_alpha(100)
        self.most_recent = None

    def done(self):
        return len(self.lines) == 0

    def add_line(self, text, cps=None):
        self.lines.append(Line(self, text, cps=cps))

    def add_prompt(self, options):
        self.lines.append(Prompt(self, options))

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.advance()
        if self.lines:
            self.lines[0].update(dt, events)

    def draw(self, surface):
        fps = int(sum(self.game.fps)/len(self.game.fps))
        fps = self.body_font.render(f"FPS: {fps}", 1, c.WHITE)
        #surface.blit(fps, (5, 5))

        if self.done():
            return
        x, y = self.x - self.width//2, self.y - self.height//2
        surface.blit(self.surf, (x, y))
        if self.lines:
            self.lines[0].draw(surface)
            if self.lines[0].fully_rendered():
                surface.blit(self.enter_to_continue,
                             (c.WINDOW_WIDTH//2 - self.enter_to_continue.get_width()//2,
                              c.WINDOW_HEIGHT - c.BOX_PADDING - 50))

    def advance(self):
        if self.lines and self.lines[0].fully_rendered():
            self.most_recent = self.lines.pop(0)
            self.game.player.move_disabled = False
            # self.game.continue_sound.play()

    def get_character(self):
        for character in self.game.characters:
            if character.target_alpha > 0 or character.alpha > 0:
                return character.name
        return None


class Prompt:

    def __init__(self, box, options):
        self.box = box
        self.options = options
        self.selected = 0
        self.age = 0
        self.answer = None

    def fully_rendered(self):
        return self.answer is not None

    def update(self, dt, events):
        self.age += dt

        self.box.game.player.move_disabled = True

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.selected > 0:
                        self.selected -= 1
                elif event.key == pygame.K_DOWN:
                    if self.selected < len(self.options) - 1:
                        self.selected += 1
                elif event.key == pygame.K_RETURN:
                    self.answer = self.options[self.selected]

    def draw(self, surface):
        x = self.box.x - self.box.width//2
        y = self.box.y - self.box.height//2
        xoff = c.BOX_PADDING * 2
        yoff = c.BOX_PADDING

        for i, option in enumerate(self.options):
            xoff = c.BOX_PADDING * 2
            for char in option:
                csurf = self.box.chars[char]
                if i != self.selected:
                    csurf = csurf.copy()
                    csurf.set_alpha(100)
                surface.blit(csurf, (x + xoff, y + yoff))
                xoff += csurf.get_width()
            yoff += 20

        surface.blit(self.box.advance_arrow,
                     (x + c.BOX_PADDING,
                      y + c.BOX_PADDING + 20 * self.selected))


class Line:

    def __init__(self, box, text, cps = None):
        self.box = box
        self.text = text
        self.visible_chars = 0
        self.age = 0
        self.cps = cps
        self.blep_period = 0.08
        if cps is not None:
            self.blep_period *= self.box.characters_per_second/cps
        self.since_blep = self.blep_period

    def fully_rendered(self):
        return self.visible_chars > len(self.text)

    def update(self, dt, events):
        self.age += dt
        self.since_blep += dt

        if self.since_blep > self.blep_period and not self.fully_rendered():
            self.since_blep -= self.blep_period
            if self.box.get_character() == "Parity":
                self.box.game.parity_speech.play()
            elif self.box.get_character() == "Tetroid":
                self.box.game.tetroid_speech.play()
            elif self.box.get_character() == "Warden":
                self.box.game.warden_speech.play()



        if self.cps != None:
            self.visible_chars += dt * self.cps
        else:
            self.visible_chars += dt * self.box.characters_per_second

    def draw(self, surface):
        to_render = self.text
        words = to_render.split()
        x = self.box.x - self.box.width//2
        y = self.box.y - self.box.height//2
        xoff = c.BOX_PADDING
        yoff = c.BOX_PADDING
        yspace = 22
        drawn = 0
        char_dict = self.box.chars
        for word in words:
            if word == "r/":
                char_dict = self.box.red_chars
                continue
            elif word == "b/":
                char_dict = self.box.blue_chars
                continue
            elif word == "g/":
                char_dict = self.box.green_chars
                continue
            elif word == "y/":
                char_dict = self.box.yellow_chars
                continue
            elif word in ("/r", "/g", "/b", "/y"):
                char_dict = self.box.chars
                continue
            width = 0
            for char in word:
                width += char_dict[char].get_width()
            if xoff + width + c.BOX_PADDING >= self.box.width:
                yoff += yspace
                xoff = c.BOX_PADDING
            for char in word:
                csurf = char_dict[char]
                surface.blit(csurf, (x + xoff, y + yoff))
                drawn += 1
                if drawn > self.visible_chars:
                    break
                xoff += csurf.get_width()
            xoff += self.box.chars[" "].get_width() * 1.5
            drawn += 1
            if drawn > self.visible_chars:
                break

        if self.is_blink():
            surface.blit(self.box.advance_arrow, (x + xoff, y + yoff))

    def is_blink(self):
        blink_per = 1.2
        return self.fully_rendered() and (self.age % blink_per) < blink_per/2