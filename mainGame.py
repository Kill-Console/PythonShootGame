# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random
import threading

# pylint: disable=no-member

# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SHOOT')

# 게임 음악로드
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 배경 이미지로드
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

while 1:
    # 플레이어 관련 매개 변수 설정
    player_rect = []
    player_rect.append(pygame.Rect(0, 99, 102, 126))        # 플레이어 스프라이트 그림 영역
    player_rect.append(pygame.Rect(165, 360, 102, 126))
    player_rect.append(pygame.Rect(165, 234, 102, 126))     # 플레이어 폭발 스프라이트 그림 영역
    player_rect.append(pygame.Rect(330, 624, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(432, 624, 102, 126))
    player_pos = [200, 600]
    player = Player(plane_img, player_rect, player_pos)

    # 총알 개체에서 사용하는 표면 관련 매개 변수 정의
    bullet_rect = pygame.Rect(1004, 987, 9, 21)
    bullet_img = plane_img.subsurface(bullet_rect)

    # 적 항공기 오브젝트가 사용하는 표면 관련 매개 변수 정의
    enemy1_rect = pygame.Rect(534, 612, 57, 43)
    enemy1_img = plane_img.subsurface(enemy1_rect)
    enemy1_down_imgs = []
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

    enemies1 = pygame.sprite.Group()

    # 파괴 된 스프라이트의 애니메이션을 렌더링하는 데 사용되는 파괴 된 항공기 저장
    enemies_down = pygame.sprite.Group()

    shoot_frequency = 0
    enemy_frequency = 0

    player_down_index = 16

    score = 0

    chapter = 0
    bullet_speed = 20
    enemy_speed = 50

    # 10초에 챕터가 오르고 속도가 변한다.
    def fun_a():
        global chapter
        global bullet_speed
        global enemy_speed
        
        timer = threading.Timer(10,fun_a)
        chapter += 1
        bullet_speed -= 0.2
        enemy_speed -= 1
        timer.daemon=True
        timer.start()

        # 45단계 까지 가능
        if chapter == 45:
            timer.cancel()

    fun_a()

    clock = pygame.time.Clock()

    running = True

    while running:
        # 컨트롤 게임의 최대 프레임 속도는 60입니다.
        clock.tick(45)

        # 총알 및 총알 발사 빈도 제어
        if not player.is_hit:
            if shoot_frequency % bullet_speed == 0:
                bullet_sound.play()
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= bullet_speed:
                shoot_frequency = 0

        # 적 생성
        if enemy_frequency % enemy_speed == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= enemy_speed:
            enemy_frequency = 0

        # 글 머리 기호 이동, 창 범위를 초과하면 삭제
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)

        # 적 비행기를 이동하고 창을 초과하면 삭제
        for enemy in enemies1:
            enemy.move()
            # 플레이어가 맞았는지 확인
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                game_over_sound.play()
                break
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy)

        # 적중 한 적 항공기 오브젝트를 적군 항공기 그룹에 추가하여 파괴 애니메이션을 렌더링합니다.
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)

        # 배경 그리기
        screen.fill(0)
        screen.blit(background, (0, 0))

        # 플레이어 비행기 그리기
        if not player.is_hit:
            screen.blit(player.image[player.img_index], player.rect)
            # 항공기 애니메이션을 만들기 위해 사진 인덱스 변경
            player.img_index = shoot_frequency // 8
        else:
            player.img_index = player_down_index // 8
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 47:
                running = False

        # 충돌 애니메이션 그리기
        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                enemy1_down_sound.play()
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 1000
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1

        # 총알과 적 항공기 그리기
        player.bullets.draw(screen)
        enemies1.draw(screen)

        # 점수 추첨
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 40]
        screen.blit(score_text, text_rect)

        # 챕터 표기
        chapter_font = pygame.font.Font(None, 36)
        chapter_font = chapter_font.render("chapter : " + str(chapter), True, (128, 128, 128))
        text_rect = chapter_font.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(chapter_font, text_rect)

        # 업데이트 화면
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        # 키보드 이벤트 듣기
        key_pressed = pygame.key.get_pressed()
        # 플레이어가 맞으면 효과가 없습니다.
        if not player.is_hit:
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()


    font = pygame.font.Font(None, 48)
    text = font.render('Score: '+ str(score), True, (255, 0, 0))
    text2 = font.render('Press \'space\' to Restart', True, (255, 0, 0))
    text_rect = text.get_rect()
    text2_rect = text2.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    text2_rect.centerx = screen.get_rect().centerx
    text2_rect.centery = screen.get_rect().centery +300
    screen.blit(game_over, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(text2, text2_rect)
    
    while 1:
        a=pygame.key.get_pressed()
        if a[K_SPACE]:
            chapter
            bullet_speed
            enemy_speed
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()


