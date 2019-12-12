# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""


import yaml
import pygame

conf = yaml.load(open("./setting.yaml", "r",encoding='UTF-8'))
SCREEN_WIDTH = conf['display']['W']
SCREEN_HEIGHT = conf['display']['H']

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # 用来存储玩家对象精灵图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]                      # 初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.level = 1                                  # 플레이어 레벨
        self.speed = 4                                  # 初始化玩家速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.img_index = 0                              # 玩家精灵图片索引
        self.is_hit = False                             # 玩家是否被击中
        self.hp = 3                                     # HP 변수 추가
        self.killed = 0                                 # 죽인 적 수
        self.alive = True
        self.player_down_index = 16

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

    def draw(self, screen, shoot_frequency):
        if not self.is_hit:
            screen.blit(self.image[self.img_index], self.rect)
            self.img_index = shoot_frequency // 8
        else:
            self.img_index = self.player_down_index // 8
            screen.blit(self.image[self.img_index], self.rect)
            self.player_down_index += 1
            if self.player_down_index > 47:
                self.alive = False
        self.bullets.draw(screen)


class Enemy(pygame.sprite.Sprite):
    '''
        좌표는 좌측 상단 기준
    '''
    def __init__(self, enemy_img, enemy_down_imgs, init_pos, E_HP):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img                                   # Default image
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs                         # Down 시 image
       self.speed = 2                                           # 이동 속도
       self.HP = 10                                           # HP --> 총알을 맞고 버틸 수 있는 횟수
       self.down_index = 0                                      # 죽은 후 몇 fps간 유지

    def move(self):
        self.rect.top += self.speed

    def down_draw(self, screen):
        screen.blit(self.down_imgs[self.down_index // 2], self.rect)
