import pygame
import constants as c


class Player:

    def __init__(self, game):
        self.game = game
        self.x = c.WINDOW_WIDTH//2
        self.y = c.WINDOW_HEIGHT//2
        self.shield_angle = 0
        self.shield_vis_angle = 0
        self.shield_surf = pygame.image.load(c.image_path("shield.png"))
        self.radius = 20
        self.shield_radius = 50
        self.shield_spread = 90 # in degrees
        self.has_shield = False

    def draw(self, surface):
        x, y = self.game.xy_transform(self.x, self.y)
        pygame.draw.circle(surface, c.WHITE, (x, y), self.radius)
        self.draw_shield(surface)
        pass

    def update_shield(self, dt):
        d = self.shield_angle - self.shield_vis_angle
        d2 = self.shield_angle - self.shield_vis_angle + 360
        d3 = self.shield_angle - self.shield_vis_angle - 360
        true_d = d
        for item in [d2, d3]:
            if abs(item) < abs(true_d):
                true_d = item

        diff = 15*true_d*dt
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
        if not self.has_shield:
            return
        ssurf = pygame.transform.rotate(self.shield_surf, self.shield_vis_angle)
        x = self.x - ssurf.get_width()//2
        y = self.y - ssurf.get_height()//2
        x, y = self.game.xy_transform(x, y)
        surface.blit(ssurf, (x, y))

    def update(self, dt, events):

        for event in events:
            if event.type == pygame.KEYDOWN and self.has_shield:
                if event.key == pygame.K_UP:
                    self.shield_angle = c.UP
                elif event.key == pygame.K_RIGHT:
                    self.shield_angle = c.RIGHT
                elif event.key == pygame.K_LEFT:
                    self.shield_angle = c.LEFT
                elif event.key == pygame.K_DOWN:
                    self.shield_angle = c.DOWN

        self.update_shield(dt)
        self.shield_vis_angle %= 360