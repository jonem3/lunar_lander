#! python
from pygame.sprite import Sprite
import pygame

fps = 200.0
gravity = -2.0/fps
thrust = 3.0/fps

class Lander(Sprite):
    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Lander, self).__init__()
        self.rocket_fire = pygame.image.load("../images/fire.png").convert()
        self.rocket = pygame.image.load("../images/rocket.png").convert()
        
        self.height = 600
        self.horiz = 395
        self.delta_vert = 0
        self.delta_horiz = 0 
        self.fuel = 10000
        #print (str(thrust))
        #print (str(gravity))
        
    def is_fuel_remaining(self):
        return self.fuel > 0
    
    def calculate_vertical_speed(self, thrusting):
        if thrusting and self.is_fuel_remaining():
            self.delta_vert += thrust
            self.fuel -= 1
            #print ("thrusting")
        self.delta_vert += gravity
        self.height += self.delta_vert
        if self.height < 32:
            self.height = 32
            self.delta_vert = 0.0
        #print("height" + str(self.height))
        #print("delta vert" + str(self.delta_vert))
        
    def calc_horizontal(self, left, right):
        if left and self.is_fuel_remaining():
            self.delta_horiz -= thrust
            self.fuel -= 1
        elif right and self.is_fuel_remaining():
            self.delta_horiz += thrust
            self.fuel -= 1
        self.horiz += self.delta_horiz
    
    def render(self):
        
        y = 600 - self.height
        self.image = pygame.Surface([24, 32]).convert()
        self.image.blit (self.rocket, (0, 0), (0, 0, 24, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.horiz
        self.rect.y = y
        #self.image = pygame.Surface([SuperSprite.SPRITE_DIMENSION, SuperSprite.SPRITE_DIMENSION]).convert()
        #self.image.blit(self.sprite_sheet, (0, 0), (left_side, 0, SuperSprite.SPRITE_DIMENSION, SuperSprite.SPRITE_DIMENSION))