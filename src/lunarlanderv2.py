import pygame
import random
pygame.font.init()

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BCKGRNDCLR = (0,0,0)
FPS = 60.0
GRV = -2.5/fps
INERTDAMP = 1.5/fps
THRUST = 3.0/fps

class Ship:
    #Ship class representing the lunar lander
    IMG = "../images/rocket_new.png"
    MAXFUEL = 1000
    def __init__(self, x, y):
        #Initialise the space ship
        super(Ship, self).__init__()
        self.rect = None
        self.x = 395
        self.y = 600
        self.delta_x = 0
        self.delta_y = 0
        self.img_count = 0
        self.img = self.IMG
        self.fuel = Ship.MAXFUEL
    def fuel_reserves(self):
        #Check if fuel is remaining
        return self.fuel > 0

    def calcVertSpeed(self, thrust, land):
        #Store the current height
        old_y = self.y
        #Fire the boosters
        if thrust and self.fuel_reserves():
            self.delta_y += thrust
            self.fuel -= 1
        self.delta_y += GRV
        self.y += self.delta_y
        #reset y after landing so that rocket does not drift through the floor
        if land:
            self.y = old_y
            land_ok = self.delta_vert > -1
            self.delta_y = 0
            return landed_ok
        if self.y >= 600:
            self.y = 600
            self.delta_y = 0
    def calc_x(self, left, right):
        if left and self.fuel_reserves():
            self.delta_x -= THRUST
            self.fuel -= 1
        elif right and self.fuel_reserves():
            self.delta_x += THRUST
            self.fuel -= 1
        self.x += self.delta_x
        if self.delta_x > 0:
            self.delta_x -= INERTDAMP
        elif self.delta_x < 0:
            self.delta_x += INERTDAMP
        else:
            pass
        if self.x >= 800:
            self.x = 0
        if self.x <= 0:
            self.horiz = 800
    def render(self):
        y = 600 - self.y
        self.image = pygame.Surface([24, 32]).convert()
        self.image.set_colorkey(BCKGRNDCLR)
        self.image.blit(self.img, (0,0), (0,0,24,32))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)


class Planet():
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Planet, self).__init__()
        self.surface = pygame.image.load("../images/surface.png").convert()
        self.rect = None

    def render(self):
        self.image = pygame.Surface([800, 100]).convert()
        self.image.blit(self.surface, (0, 0), (0, 0, 800, 100))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500
        self.mask = pygame.mask.from_surface(self.image)


class Burn():
    def __init__(self, lander):
        # Call the parent class (Sprite) constructor
        super(Burn, self).__init__()
        self.rocket_fire = pygame.image.load("../images/fire.png").convert()
        self.lander = lander

    def render(self, image_number):
        self.image = pygame.Surface([8, 10]).convert()
        offset = image_number * 8
        self.image.blit(self.rocket_fire, (0, 0), (offset, 0, 8, 10))
        self.rect = self.image.get_rect()
        self.rect.x = self.lander.rect.x + 8
        self.rect.y = self.lander.rect.y + 32


def main():
    global font
    global message
    pygame.init()
    pygame.display.set_caption("Lunar Lander Game")
    screen = pygame.display.set_mode((800, 600))

    font = pygame.font.SysFont('Calibri', 25, True, False)

    lander = Lander()
    lander_group = Group()
    lander_group.add(lander)

    burn = Burn(lander)
    burn_group = Group()
    burn_group.add(burn)

    fuel_bar_front = Rectangle(blue)
    fuel_bar_front_group = Group()
    fuel_bar_front_group.add(fuel_bar_front)

    fuel_bar_back = Rectangle(white)
    fuel_bar_back_group = Group()
    fuel_bar_back_group.add(fuel_bar_back)

    planet = Planet()
    planet_group = Group()
    planet_group.add(planet)

    done = False
    pygame.display.update()
    flicker = True
    music = False
    first_frame = True

    landed_ok = None
    # CHANGE THE FILE TYPE BELOW TO PNG TO SEE TRASHY STARS
    background_image = pygame.image.load(r"C:\Users\mattp\Documents\Projects\lunar_lander\images\space.jpg").convert()