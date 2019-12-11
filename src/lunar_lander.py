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
import visualize
pygame.font.init()

background_colour = (0, 0, 0)

blue = (0, 0, 255)
white = (255, 255, 255)
font = None
STAT_FONT = pygame.font.SysFont("arial", 25)
LANDINGS_FONT = pygame.font.SysFont("arial", 15)
message = None
gen = 0
successful_landings = []


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
        # print('bottom left')
        return math.hypot(x2b-x1, y2-y1b)
    elif left and top:
        # print('top left')
        return math.hypot(x2b-x1, y2b-y1)
    elif top and right:
        # print('top right')
        return math.hypot(x2-x1b, y2b-y1)
    elif right and bottom:
        # print('bottom right')
        return math.hypot(x2-x1b, y2-y1b)
    elif left:
        # print('left')
        return x1 - x2b
    elif right:
        # print('right')
        return x2 - x1b
    elif top:
        # print('top')
        return y1 - y2b
    elif bottom:
        # print('bottom')
        return y2 - y1b
    else:  # rectangles intersect
        # print('intersection')
        return 0.
#Below has been changed:


def draw_window(win, landers, planet, score, gen, planet_group, lander_group, landedwell, top_fitness, burn_group, fuel_bar_back, fuel_bar_front, scoreboardgroup, lowest):
    if gen == 0:
        gen = 1

    #for lander in landers:
        #lander.render()

    #for burner in burners:
        #burner.render(image_number)
    planet.render()
    burn_group.draw(win)
    lander_group.draw(win)
    planet_group.draw(win)

    fuel_bar_back.draw(win)
    fuel_bar_front.draw(win)
    scoreboardgroup.draw(win)
    score_label = STAT_FONT.render("Generations: " + str(gen-1), 1, white)
    win.blit(score_label, (10, 10))
    score_label = STAT_FONT.render("No. Alive: " + str(len(landers)), 1, white)
    win.blit(score_label, (10, 60))
    score_label = STAT_FONT.render("Land Well?: "+ str(landedwell), 1, white)
    win.blit(score_label, (10, 110))
    top_fitness_rounded = "%.2f" % top_fitness
    score_label = STAT_FONT.render("Max Score: " + str(top_fitness_rounded), 1, white)
    win.blit(score_label, (10, 160))
    score_label = STAT_FONT.render("Lowest Score: " + str(lowest), 1, white)
    win.blit(score_label, (10, 210))
    for i in range (0, len(successful_landings)):
        landings_label = LANDINGS_FONT.render("Gen " + str(i) + " : " + str(successful_landings[i]), 1, blue)
        win.blit(landings_label, (805, (i*15)))

    pygame.display.update()


def eval_genomes(genomes, config):
    global WIN, gen
    WIN = pygame.display.set_mode((1000, 600))
    win = WIN
    gen += 1
    nets = []
    landers = []
    burners = []
    ge = []
    planet = Planet()
    planet_group = Group()
    planet_group.add(planet)
    lander_group = Group()

    landed_ok = []
    landed = []
    flicker = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        lander = Lander()
        lander_group.add(lander)
        landers.append(lander)
        landed_ok.append(None)
        landed.append(False)

        flicker.append(True)
        ge.append(genome)
    for i in range(0, len(ge)):
        ge[i].fitness += 100

    score = 0
    landedwell = 0
    clock = pygame.time.Clock()

    running = True
    first_frame = True
    firstish_frame = True
    planet.mask = pygame.mask.from_surface(planet.image)
    planet.rect = planet.image.get_rect()
    scoreboardgroup = Group()
    scoreboard = Rectangle(white)
    scoreboardgroup.add(scoreboard)
    while running and len(landers) > 0:
        scoreboard.render(800, 0, 200, 600)
        burn_group = Group()
        fuel_bar_front_group = Group()
        fuel_bar_back_group = Group()
        burners = []
        #print(burn_group)
        #print(len(burners))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                break
        win.fill(background_colour)
        top_fitness = 0
        lowest_fitness = 1000
        for x, lander in enumerate(landers):
            #burner = burners[x]
            fuel_bar_front = Rectangle(blue)
            fuel_bar_front_group.add(fuel_bar_front)
            fuel_bar_back = Rectangle(white)
            fuel_bar_back_group.add(fuel_bar_back)
            if ge[x].fitness > top_fitness:
                top_fitness = ge[x].fitness
            elif ge[x].fitness < lowest_fitness:
                lowest_fitness = ge[x].fitness
            # print(x)
            # print("Landed Ok?: " + str(landed_ok[x]))
            # print("Fitness: "+ str(ge[x].fitness))
            # print("Delta V = "+ str(lander.delta_vert))
            #ge[x].fitness += 0.1
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

                #offset_x = planet.rect.left - lander.rect.left
                #offset_y = planet.rect.top - lander.rect.top
                #landed[x] = lander.mask.overlap(planet.mask, (offset_x, offset_y)) is not None
                offset_x, offset_y = (planet.rect.left - lander.rect.left), (planet.rect.top - lander.rect.top)
                landed[x] = lander.mask.overlap(planet.mask, (offset_x, offset_y)) != None
                # print("Is this landed?:", landed[x])
                height = rect_distance(planet.rect, lander.rect)

            # print(landed[x])
            if landed_ok[x] is None and not firstish_frame:
                output = nets[landers.index(lander)].activate((offset_x, lander.horiz, lander.height, lander.fuel, offset_y, height, abs(lander.delta_vert), abs(lander.delta_horiz)))

                if output[0] > 0.5 and landed_ok[x] is None:
                    thrust = True
                #if not landed[x]:
                    #status = lander.calculate_vertical_speed(thrust, landed[x])

                #output = nets[landers.index(lander)].activate((lander.horiz, lander.fuel, offset_x, height, abs(lander.delta_horiz)))
                if output[1] > 0.5 and landed_ok[x] is None:
                    left = True
                    rcs = True
                if output[1] < -0.5 and landed_ok[x] is None:
                    right = True
                    rcs = True
                lander.calc_horizontal(left, right)
                status = lander.calculate_vertical_speed(thrust, landed[x])
            else:
                firstish_frame = False
            if not landed[x] and lander.height < 200:
                if lander.delta_vert < -2:
                    ge[x].fitness -= 0.2
            if lander.height < 200 and lander.delta_horiz < -1 or lander.delta_horiz > 1:
                ge[x].fitness -= 0.2

            if not landed[x] and not lander.is_fuel_remaining():
                ge[x].fitness -= 0.2
            if landed[x] and landed_ok[x] is not True:
                # print("Checking land quality")
                landed_ok[x] = status
                # print(landed_ok[x])
            if landed_ok[x]:
                ge[x].fitness += 50
                #win.fill(0, 255, 0)
            lander.render()
            if not landed[x] and lander.is_fuel_remaining() and thrust:
                burner = Burn(lander)
                burners.append(burner)
                burn_group.add(burner)
                flicker[x] = not flicker[x]
                image_number = 1 if flicker[x] else 0
                burner.render(image_number)
                #burn_group.draw(win)
                #burners.pop(burner)
            percent_fuel = float(lander.fuel) / float(Lander.max_fuel) * 42
            if percent_fuel > 0:
                fuel_bar_back.render((lander.horiz - 10), (600-(lander.height + 14)), 44, 10)
                fuel_bar_front.render((lander.horiz - 8), (600-(lander.height + 13)), percent_fuel, 8)
            else:
                fuel_bar_front.kill()
                fuel_bar_back.kill()
            if landed[x] and not landed_ok[x]:
                ge[landers.index(lander)].fitness -= 5
                nets.pop(landers.index(lander))
                ge.pop(landers.index(lander))
                del landed_ok[x]
                # landed_ok.remove(x)
                #burners.pop(landers.index(lander))
                #del burners[landers.index(lander)]
                burn_group.remove(burner)
                #burner.kill()
                #print (burn_group)
                landers.pop(landers.index(lander))
                lander_group.remove(lander)
            elif landed_ok[x]:
                landedwell += 1
                ge[landers.index(lander)].fitness += 10
                nets.pop(landers.index(lander))
                ge.pop(landers.index(lander))
                del landed_ok[x]

                #burner.kill()
                landers.pop(landers.index(lander))

            #burn_group.remove(burner)






        draw_window(WIN, landers, planet, score, gen, planet_group, lander_group, landedwell, top_fitness, burn_group, fuel_bar_back_group, fuel_bar_front_group,scoreboardgroup, lowest_fitness)
    successful_landings.append(landedwell)
    print("Number that landed: ", landedwell)



def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)
    # print(winner)


if __name__ == '__main__':
    #main()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

