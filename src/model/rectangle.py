#! python
from pygame.sprite import Sprite
import pygame

class Rectangle(Sprite):
    def __init__(self, colour):
        # Call the parent class (Sprite) constructor
        super(Rectangle, self).__init__()
        self.colour = colour
    
    def render(self, x, y, width, height):
        self.image = pygame.Surface([width, height])
        self.image.fill(self.colour)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
