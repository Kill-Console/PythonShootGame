# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

class Player(pygame.sprite.Sprite):
    def __init__(self, planeImg, clip_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for i in range(len(clip_rect)):
            self.image.append(planeImg.subsurface(clip_rect[i]).convert_alpha())
        self.rect = clip_rect[0]
        self.rect.topleft = init_pos
        self.speed = 1

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left < 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed
