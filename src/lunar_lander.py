#!python
import pygame
from pygame.locals import *
from model.lander import Lander
from model.burn import Burn
from model.planet import Planet
from model.rectangle import Rectangle
from pygame.sprite import Group
import time

background_colour = (0, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

def main():
    
    pygame.init()
    pygame.display.set_caption("Lunar Lander Re-Created By Matthew Jones And Philip Jones")
    screen = pygame.display.set_mode((800,600))
    
    lander = Lander()
    lander_group = Group()
    lander_group.add (lander)
    
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
        
        landed = False
        if first_frame:
            first_frame = False
        else:
            offset_x, offset_y = (planet.rect.left - lander.rect.left), (planet.rect.top - lander.rect.top)
            landed = lander.mask.overlap(planet.mask, (offset_x, offset_y))  != None               
            
        status = lander.calculate_vertical_speed(thrust, landed)
        if landed:
            if status:
                print ("landed")
            else:
                print ("crashed")
            
        lander.calc_horizontal(left, right)
        screen.fill(background_colour)
        lander.render()
        lander_group.draw(screen)
        if thrust and lander.is_fuel_remaining():
            flicker = not flicker
            image_number = 1 if flicker else 0
            burn.render(image_number)
            burn_group.draw(screen)
            if not music:
                pygame.mixer.music.load('../sounds/rocket_sound.mp3')
                pygame.mixer.music.play(-1)
                music = True
        elif music:
            music = False
            pygame.mixer.music.stop()
    
        #draw fuel bar :)
        percent_fuel = float(lander.fuel) / float(Lander.max_fuel) * 100.0
        fuel_bar_back.render(10, 10, 104, 12)
        fuel_bar_back_group.draw(screen)
        fuel_bar_front.render(12,  12,  percent_fuel,  8)
        fuel_bar_front_group.draw(screen)
        
        planet.render()
        planet_group.draw(screen)
        
        pygame.display.update()
        time.sleep(0.018)
        
        
if __name__ == '__main__':
    main()
    
