#!python
import pygame
from pygame.locals import *
from model.lander import Lander
import time

background_colour = (0, 0, 0)

def main():
    
    pygame.init()
    pygame.display.set_caption("Lunar Lander Re-Created By Matthew Jones And Philip Jones")
    screen = pygame.display.set_mode((800,600))
    lander = Lander()
    lander_group = pygame.sprite.Group()
    lander_group.add (lander)
    
    done = False
    pygame.display.update()
    while not done:
        thrust = False
        left = False
        right = False
        pygame.event.pump()
        keys=pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            done = True
        if keys[K_SPACE] or keys[K_UP]:
            thrust = True
        if keys[K_LEFT]:
            left = True
        if keys[K_RIGHT]:
            right = True
        
        lander.calculate_vertical_speed(thrust)
        lander.calc_horizontal(left, right)
        screen.fill(background_colour)
        lander.render()
        lander_group.draw(screen)
        pygame.display.update()
        time.sleep(0.02)
        
        
if __name__ == '__main__':
    main()
    
