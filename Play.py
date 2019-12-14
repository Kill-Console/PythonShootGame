# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""
import yaml
import pygame
import random
from sys import exit

from pygame.locals import *

from Game import Game

if __name__ == "__main__":

    # Setting loading
    conf = yaml.load(open("./setting.yaml", "r"))

    # Pygame 기본 설정(Pygame basic setting)
    pygame.init()
    window = pygame.display.set_mode((conf['display']['W'], conf['display']['H']))
    pygame.display.set_caption(conf['title'])
    clock = pygame.time.Clock()

    game = Game(conf, window)
    while True:

        while game.player.alive:
            clock.tick(60)          # 60fps

            game.update()           # 게임 state update
            game.draw()             # UI 렌더링(User Interface renderint)
            game.handleEvent()      # I/O 처리(Input/Output handle process)
        
        game.draw_gameover(game.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                pressed = pygame.key.get_pressed()
                

        pygame.display.update()
