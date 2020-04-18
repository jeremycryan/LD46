import pygame
import constants as c


class TextBox:

    def __init__(self, game):
        self.game = game
        self.lines = []
        self.characters_per_second = 80
        self.advance_arrow = pygame.image.load(c.image_path("advance_arrow.png"))
        self.body_font = pygame.font.Font(c.font_path("Myriad.otf"), 20)
        self.chars = {char:self.body_font.render(char, 1, c.WHITE) for char in c.PRINTABLE_CHARS}
        self.highlight_chars = {char:self.body_font.render(char, 1, (255, 60, 60)) for char in c.PRINTABLE_CHARS}
        self.width = 500
        self.height = 140
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((40, 40, 40))
        self.x = c.WINDOW_WIDTH//2
        self.y = c.WINDOW_HEIGHT - self.height//2 - 50
        self.active_character = None

    def done(self):
        return len(self.lines) == 0

    def add_line(self, text):
        self.lines.append(Line(self, text))

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.advance()
        if self.lines:
            self.lines[0].update(dt, events)

    def draw(self, surface):
        if self.done():
            return
        x, y = self.x - self.width//2, self.y - self.height//2
        surface.blit(self.surf, (x, y))
        if self.lines:
            self.lines[0].draw(surface)

    def advance(self):
        if self.lines and self.lines[0].fully_rendered():
            self.lines.pop(0)


class Line:

    def __init__(self, box, text):
        self.box = box
        self.text = text
        self.visible_chars = 0
        self.age = 0

    def fully_rendered(self):
        return self.visible_chars > len(self.text)

    def update(self, dt, events):
        self.age += dt
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
        for word in words:
            char_dict = self.box.chars
            if word[0] == word[-1] and word[0] == "*":
                char_dict = self.box.highlight_chars
                word = word.strip("*")
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
            xoff += self.box.chars[" "].get_width()
            drawn += 1
            if drawn > self.visible_chars:
                break

        blink_per = 1.2
        if self.fully_rendered() and (self.age % blink_per) < blink_per/2:
            surface.blit(self.box.advance_arrow, (x + xoff, y + yoff))