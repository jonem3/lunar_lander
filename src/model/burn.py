#! python
from pygame.sprite import Sprite
import pygame

class Burn(Sprite):
    def __init__(self, lander):
        # Call the parent class (Sprite) constructor
        super(Burn, self).__init__()
        self.rocket_fire = pygame.image.load("../images/fire.png").convert()
        self.lander = lander
        
    def render(self, image_number):
        self.image = pygame.Surface([8, 10]).convert()
        offset = image_number * 8
        self.image.blit (self.rocket_fire, (0, 0), (offset, 0, 8, 10))
        self.rect = self.image.get_rect()
        self.rect.x = self.lander.rect.x + 8
        self.rect.y = self.lander.rect.y + 32
        
