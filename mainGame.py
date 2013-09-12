# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *

# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('飞机大战')

# 载入背景图
background = pygame.image.load('resources/image/background.png').convert()

# 设置玩家相关参数
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_pos = [200, 600]
filename = 'resources/image/shoot.png'

planeImg = pygame.image.load(filename)
player = Player(planeImg, player_rect, player_pos)

player_img_index = 0

while 1:
    screen.fill(0)
    screen.blit(background, (0,0))
    screen.blit(player.image[player_img_index], player.rect)
    if player_img_index == 0:
        player_img_index = 1
    else:
        player_img_index = 0
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_w]:
        player.moveUp()
    if key_pressed[K_s]:
        player.moveDown()
    if key_pressed[K_a]:
        player.moveLeft()
    if key_pressed[K_d]:
        player.moveRight()
       
