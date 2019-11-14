#!python
import os
from builtins import len, enumerate

import tkinter
import pygame
from pygame.locals import *
from model.lander import Lander
from model.burn import Burn
from model.planet import Planet
from model.rectangle import Rectangle
# from model.rcs import RCS
from pygame.sprite import Group
import numpy
import time
import math
import neat

background_colour = (0, 0, 0)

blue = (0, 0, 255)
white = (255, 255, 255)
font = None
message = None
gen = 0


def display_message(screen):    
    global message
    global font
    if message is not None:
        score_text = font.render(message , True, white)
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


def rect_distance(rect1, rect2):
    x1, y1 = rect1.topleft
    x1b, y1b = rect1.bottomright
    x2, y2 = rect2.topleft
    x2b, y2b = rect2.bottomright
    left = x2b < x1
    right = x1b < x2
    top = y2b < y1
    bottom = y1b < y2
    if bottom and left:
        print('bottom left')
        return math.hypot(x2b-x1, y2-y1b)
    elif left and top:
        print('top left')
        return math.hypot(x2b-x1, y2b-y1)
    elif top and right:
        print('top right')
        return math.hypot(x2-x1b, y2b-y1)
    elif right and bottom:
        print('bottom right')
        return math.hypot(x2-x1b, y2-y1b)
    elif left:
        print('left')
        return x1 - x2b
    elif right:
        print('right')
        return x2 - x1b
    elif top:
        print('top')
        return y1 - y2b
    elif bottom:
        print('bottom')
        return y2 - y1b
    else:  # rectangles intersect
        print('intersection')
        return 0.
#Below has been changed:


def draw_window(win, landers, planet, score, gen, planet_group, lander_group):
    if gen == 0:
        gen = 1

    for lander in landers:
        lander.render()
    planet.render()
    lander_group.draw(win)
    planet_group.draw(win)

    pygame.display.update()


def eval_genomes(genomes, config):
    global WIN, gen
    WIN = pygame.display.set_mode((800, 600))
    win = WIN
    gen += 1
    nets = []
    landers = []
    ge = []
    planet = Planet()
    planet_group = Group()
    planet_group.add(planet)
    lander_group = Group()
    landed_ok = []
    landed = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        lander = Lander()
        lander_group.add(lander)
        landers.append(lander)
        landed_ok.append(None)
        landed.append(False)
        ge.append(genome)

    score = 0

    clock = pygame.time.Clock()

    running = True
    first_frame = True
    firstish_frame = True
    planet.mask = pygame.mask.from_surface(planet.image)
    planet.rect = planet.image.get_rect()
    while running and len(landers) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                break
        win.fill(background_colour)
        for x, lander in enumerate(landers):
            print(x)
            print("Landed Ok?: " + str(landed_ok[x]))
            print("Fitness: "+ str(ge[x].fitness))
            print("Delta V = "+ str(lander.delta_vert))
            ge[x].fitness += 0.1
            thrust = False
            left = False
            left_rcs = False
            right = False
            right_rcs = False
            landed[x] = False
            if first_frame:
                first_frame = False
            else:
                #lander.rect = lander.image.get_rect()
                #lander.mask = pygame.mask.from_surface(lander.image)

                offset_x = planet.rect.left - lander.rect.left
                offset_y = planet.rect.top - lander.rect.top
                landed[x] = lander.mask.overlap(planet.mask, (offset_x, offset_y)) is not None
                height = rect_distance(planet.rect, lander.rect)

            print(landed[x])
            if landed_ok[x] is None and not firstish_frame:
                output = nets[landers.index(lander)].activate((lander.height, lander.is_fuel_remaining(), offset_y, height, abs(lander.delta_vert)))

                if output[0] > 0.5 and landed_ok[x] is None:
                    thrust = True
                if not landed[x]:
                    status = lander.calculate_vertical_speed(thrust, landed[x])

                output = nets[landers.index(lander)].activate((lander.horiz, lander.is_fuel_remaining(), offset_x, height, abs(lander.delta_horiz)))
                if output[0] > 0.5 and landed_ok[x] is None:
                    left = True
                    rcs = True
                if output[0] < -0.5 and landed_ok[x] is None:
                    right = True
                    rcs = True
                lander.calc_horizontal(left, right)
            else:
                firstish_frame = False
            if landed[x] and landed_ok[x] is None:
                #status = lander.check_if_landed_ok(landed[x])
                landed_ok[x] = status
            if landed_ok[x]:
                ge[x].fitness += 10
                win.fill(0, 255, 0)
            if landed[x] and not landed_ok[x]:
                ge[landers.index(lander)].fitness -= 1
                nets.pop(landers.index(lander))
                ge.pop(landers.index(lander))
                landers.pop(landers.index(lander))
                lander_group.remove(lander)
            if not landed[x] and lander.height < 200:
                if lander.delta_vert < -2:
                    ge[x].fitness -= 1
            if not landed[x] and not lander.is_fuel_remaining():
                ge[x].fitness -= 1

        draw_window(WIN, landers, planet, score, gen, planet_group, lander_group)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)
    print(winner)


if __name__ == '__main__':
    #main()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

