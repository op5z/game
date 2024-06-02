import pygame
import random
from pygame.sprite import Sprite

class Virus(Sprite):
    def __init__(self, vi_game):
        super().__init__()
        self.screen = vi_game.screen
        self.settings = vi_game.settings
        self.image = pygame.image.load("images/virus.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.settings.screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.y_speed = 1.5

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.top > self.settings.screen_height:
            self.rect.y = random.randrange(-100, -40)
            self.rect.x = random.randrange(self.settings.screen_width - self.rect.width)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
