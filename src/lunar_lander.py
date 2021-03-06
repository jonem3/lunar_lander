#!python
import tkinter
import pygame
from pygame.locals import *
from model.lander import Lander
from model.burn import Burn
from model.planet import Planet
from model.rectangle import Rectangle
#from model.rcs import RCS
from pygame.sprite import Group
import numpy
import time

background_colour = (0, 0, 0)

blue = (0, 0, 255)
white = (255, 255, 255)
font = None
message = None

def display_message(screen):    
    global message
    global font
    if message is not None:
        score_text = font.render( message , True, white)
        screen.blit(score_text, [130, 10 ])
        
def play_sound(sound_file,  looping = False):
    play_value = -1 if looping else 0
    pygame.mixer.music.stop()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(play_value)

def crashed_message():
    global message
    message = "Oh no! You Crashed."
    play_sound('../sounds/explosion.mp3')
    
def landed_message():    
    global message
    message = "Well done! You've landed!"
    
def main():
    global font
    global message
    pygame.init()
    pygame.display.set_caption("Lunar Lander Game")
    screen = pygame.display.set_mode((800,600))
    
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
    #CHANGE THE FILE TYPE BELOW TO PNG TO SEE TRASHY STARS
    background_image = pygame.image.load(r"C:\Users\mattp\Documents\Projects\lunar_lander\images\space.jpg").convert()
    while not done:
        #DISABLE THE BELOW SETTINGS FOR THE BACKGROUND TO CHANGE BACK
        #TO PURE COLOUR
        screen.blit(background_image, [0, 0])
        thrust = False
        left = False
        right = False
        left_rcs = False
        right_rcs = False
        pygame.event.pump()
        keys=pygame.key.get_pressed()
        if landed_ok is None:
            if keys[K_SPACE] or keys[K_UP]:
                thrust = True
            if keys[K_LEFT]:
                left = True
                rcs = True
            if keys[K_RIGHT]:
                right = True
                rcs = True
        
        landed = False
        if first_frame:
            first_frame = False
        else:
            offset_x, offset_y = (planet.rect.left - lander.rect.left), (planet.rect.top - lander.rect.top)
            landed = lander.mask.overlap(planet.mask, (offset_x, offset_y))  != None               
            
        status = lander.calculate_vertical_speed(thrust, landed)
        if landed and landed_ok is None:
            landed_ok = status
            if landed_ok:
                landed_message()
            else:
                crashed_message()
                
        if not landed and lander.height < 200:
            if lander.delta_vert < -2:
                message = "Almost there!  TOO FAST!"
            else:
                message = "Almost there! Slow down for a soft landing"
        #else:
            #distance = (lander.height)/10
            #message = ("DISTANCE TO GROUND = " + str(distance) + "M")
        lander.calc_horizontal(left, right)
        #ENABLE BELOW SETTING FOR THE SILLY STARS TO DISAPPEAR
        #screen.fill(background_colour)
        lander.render()
        lander_group.draw(screen)
        if not landed and thrust and lander.is_fuel_remaining():
            flicker = not flicker
            image_number = 1 if flicker else 0
            burn.render(image_number)
            burn_group.draw(screen)
            if not music:
                play_sound('../sounds/rocket_sound.mp3',  True)
                music = True
        '''
        if not landed and right_rcs and lander.is_fuel_remaining():
            rcs.render_right(image_number)
            
        elif music and not landed:
            music = False
            pygame.mixer.music.stop()
        '''
        #draw fuel bar :)
        percent_fuel = float(lander.fuel) / float(Lander.max_fuel) * 100.0
        fuel_bar_back.render(10, 10, 104, 12)
        fuel_bar_back_group.draw(screen)
        fuel_bar_front.render(12,  12,  percent_fuel,  8)
        fuel_bar_front_group.draw(screen)
        
        planet.render()
        planet_group.draw(screen)
        
        display_message(screen)
        
        pygame.display.update()
        time.sleep(0.015)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        
if __name__ == '__main__':
    main()
    
