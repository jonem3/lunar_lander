#! python
from pygame.sprite import Sprite
import pygame
black = (0,0,0)
fps = 60.0
gravity = -2.5/fps
inertial_dampners = 1.5/fps
thrust = 3.0/fps


class Lander(Sprite):
    
    max_fuel = 1000
    
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Lander, self).__init__()
        self.rocket = pygame.image.load("../images/rocket_new.png")#.convert()
        self.rect = None
        self.height = 600
        self.horiz = 395
        self.delta_vert = 0
        self.delta_horiz = 0 
        self.fuel = Lander.max_fuel
        #print (str(thrust))
        #print (str(gravity))
        
    def is_fuel_remaining(self):
        return self.fuel > 0
    
    def calculate_vertical_speed(self, thrusting, landed):
        old_height = self.height
        if thrusting and self.is_fuel_remaining():
            self.delta_vert += thrust
            self.fuel -= 1
            #print ("thrusting")
        self.delta_vert += gravity
        self.height += self.delta_vert
        if landed:
            self.height = old_height
            landed_ok = self.delta_vert > -1
            self.delta_vert = 0
            return landed_ok
        if self.height >= 600:
            self.height = 600
            self.delta_vert = 0
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
        if self.delta_horiz > 0:
            self.delta_horiz -= inertial_dampners
        elif self.delta_horiz < 0:
            self.delta_horiz += inertial_dampners
        else:
            pass
        if self.horiz >= 800:
            self.horiz = 10
        if self.horiz <= 0:
            self.horiz = 800

    
    def render(self):
        
        y = 600 - self.height
        self.image = pygame.Surface([24, 32]).convert()
        self.image.set_colorkey(black)
        self.image.blit (self.rocket, (0, 0), (0, 0, 24, 32))
        self.image.set_colorkey((255, 255, 255))        
        self.rect = self.image.get_rect()
        self.rect.x = self.horiz
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        #self.image = pygame.Surface([SuperSprite.SPRITE_DIMENSION, SuperSprite.SPRITE_DIMENSION]).convert()
        #self.image.blit(self.sprite_sheet, (0, 0), (left_side, 0, SuperSprite.SPRITE_DIMENSION, SuperSprite.SPRITE_DIMENSION))
