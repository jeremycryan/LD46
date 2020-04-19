import pygame
import constants as c

class Background:
    def __init__(self, game):
        self.age = 0
        self.game = game

    def update(self, dt, events):
        self.age += dt
        pass

    def draw(self, surface):
        pass


class Caves(Background):
    def __init__(self, game):
        super().__init__(game)

        self.load_layers()
        self.upside_down_layers = [pygame.transform.rotate(layer, 180) for layer in self.layers]
        self.layer_factors = [0.2, 0.5, 0.8]
        self.speed = -300
        self.x = 0
        self.alpha = 0
        self.target_alpha = 0

    def load_layers(self):
        rel = "cave"
        self.layer_1 = pygame.image.load(c.image_path(f"{rel}_layer_1.png"))
        self.layer_2 = pygame.image.load(c.image_path(f"{rel}_layer_2.png"))
        self.layer_3 = pygame.image.load(c.image_path(f"{rel}_layer_3.png"))

        self.layers = [self.layer_3, self.layer_2, self.layer_1]


    def fade_in(self):
        self.target_alpha = 150

    def fade_out(self):
        self.target_alpha = 0

    def update(self, dt, events):
        super().update(dt, events)
        self.x += self.speed * dt
        da = self.target_alpha - self.alpha
        if da:
            self.alpha += da/abs(da) * 200 * dt
        if da > 0:
            self.alpha = min(self.target_alpha, self.alpha)
        else:
            self.alpha = max(self.target_alpha, self.alpha)

    def draw(self, surface):
        y = 0
        base = pygame.Surface((self.layers[0].get_width(),
                               self.layers[0].get_height()*2))
        for i, layer in enumerate(self.layers):
            x = int((self.x * self.layer_factors[i]) % c.WINDOW_WIDTH)
            base.blit(layer, (x, y))
            base.blit(layer, (x - layer.get_width(), y))
            low_y = y + layer.get_height()
            low_layer = self.upside_down_layers[i]
            base.blit(low_layer, (x, low_y))
            base.blit(low_layer, (x - low_layer.get_width(), low_y))
        base.set_alpha(self.alpha)
        surface.blit(base, (0, 80))


class Ruins(Caves):

    def fade_in(self):
        self.target_alpha = 120

    def load_layers(self):
        rel = "ruins"
        self.layer_1 = pygame.image.load(c.image_path(f"{rel}_layer_1.png"))
        self.layer_2 = pygame.image.load(c.image_path(f"{rel}_layer_2.png"))
        self.layer_3 = pygame.image.load(c.image_path(f"{rel}_layer_3.png"))

        self.layers = [self.layer_3, self.layer_2, self.layer_1]