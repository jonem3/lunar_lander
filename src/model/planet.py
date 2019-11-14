#! python
from pygame.sprite import Sprite
import pygame

class Planet(Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Planet, self).__init__()
        self.surface = pygame.image.load("../images/surface.png").convert()

        self.image = pygame.Surface([800, 100]).convert()
        self.rect = self.image.get_rect()
        
    def render(self):

        self.image.blit (self.surface, (0, 0), (0, 0, 800, 100))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500
        self.mask = pygame.mask.from_surface(self.image)
