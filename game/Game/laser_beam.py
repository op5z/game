import pygame
from pygame.sprite import Sprite

class LaserBeam(Sprite):
    def __init__(self, vi_game):
        super().__init__()
        self.screen = vi_game.screen
        self.settings = vi_game.settings
        self.color = self.settings.laser_beam_color
        self.rect = pygame.Rect(0, 0, self.settings.laser_beam_width, self.settings.laser_beam_height)
        self.rect.midtop = vi_game.robot.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.laser_beam_speed
        self.rect.y = self.y

    def draw_laser_beam(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
