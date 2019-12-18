import random
import pygame

from EntityType import *
from pygame.locals import *

        

class Game():
    def __init__(self, conf, screen):
        # Basic settings
        self.conf = conf
        self.screen =  screen
        self.load_image()
        self.load_music()
        self.boss_level=1
        self.boss_state=False
        
        # Objects
        self.player = self.setPlayer()
        self.enemies = pygame.sprite.Group()
        self.enemies_down = pygame.sprite.Group()
        self.setEnemy()
        self.boss = self.setBoss()

        self.score = 0
        self.score2 = 0
        self.EHP = 2                                         # 새로 생긴 적의 HP --> 난이도 조절 parameter
        self.shoot_frequency = 0
        self.enemy_frequency = 0


    # BGM 및 효과음 로딩 & 재생
    def load_music(self): 
        sounds = self.conf['sounds']
        self.bullet_sound = pygame.mixer.Sound(sounds['bullet'])
        self.enemy_down_sound = pygame.mixer.Sound(sounds['E_down'])
        self.game_over_sound = pygame.mixer.Sound(sounds['gameover'])
        
        self.bullet_sound.set_volume(0.3)                       # volume : 0 ~ 1 사이의 값 
        self.enemy_down_sound.set_volume(0.3)
        self.game_over_sound.set_volume(0.3)
        
        pygame.mixer.music.load(sounds['bgm'])
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25)


    # 게임에 필요한 이미지 로딩
    def load_image(self):
        imgs = self.conf['images']              
        self.background_img = pygame.image.load(imgs['background']).convert()
        self.gameover_img = pygame.image.load(imgs['gameover'])
        self.player_img = pygame.image.load(imgs['player'])
        bullet_rect = pygame.Rect(1004, 987, 9, 21)
        self.bullet_img = self.player_img.subsurface(bullet_rect)
        bbullet_rect = pygame.Rect(69,78,9,21)
        self.bbullet_img = self.player_img.subsurface(bbullet_rect)

    # Player 정보 setting 및 객체 생성
    def setPlayer(self):
        player_rect = []
        player_rect.append(pygame.Rect(0, 99, 102, 126))        # default
        player_rect.append(pygame.Rect(165, 360, 102, 126))     # default
        player_rect.append(pygame.Rect(165, 234, 102, 126))     # 총 맞은 이미지
        player_rect.append(pygame.Rect(330, 624, 102, 126))
        player_rect.append(pygame.Rect(330, 498, 102, 126))
        player_rect.append(pygame.Rect(432, 624, 102, 126))
        player_pos = [200, 600]
        return Player(self.player_img, player_rect, player_pos)


    # Enemy 정보 setting
    def setEnemy(self):
        self.enemy_rect = pygame.Rect(534, 612, 57, 43)
        self.enemy_img = self.player_img.subsurface(self.enemy_rect)
        self.enemy_down_imgs = []
        self.enemy_down_imgs.append(self.player_img.subsurface(pygame.Rect(267, 347, 57, 43)))
        self.enemy_down_imgs.append(self.player_img.subsurface(pygame.Rect(873, 697, 57, 43)))
        self.enemy_down_imgs.append(self.player_img.subsurface(pygame.Rect(267, 296, 57, 43)))
        self.enemy_down_imgs.append(self.player_img.subsurface(pygame.Rect(930, 697, 57, 43)))

##### Boss 정보 setting
    def setBoss(self):
        self.boss_rect = pygame.Rect(162,750,169,247)
        self.boss_img = self.player_img.subsurface(self.boss_rect)
        self.boss_down_imgs = []
        self.boss_down_imgs.append(self.player_img.subsurface(pygame.Rect(0,480,169,247)))
        self.boss_down_imgs.append(self.player_img.subsurface(pygame.Rect(0,230,169,247)))
        self.boss_down_imgs.append(self.player_img.subsurface(pygame.Rect(840,750,169,247)))
        boss_pos = [150,20]
        return Boss(self.boss_img, self.boss_rect, boss_pos,self.boss_level)
    
        
    def update(self):
        '''
            전체 게임 핵심 로직
        '''
        # Bullet 생성 --> while문을 15번 돌 때마다 생성
        if not self.player.is_hit:
            if self.shoot_frequency % 15 == 0:
                self.bullet_sound.play()
                self.player.shoot(self.bullet_img)
            self.shoot_frequency += 1
            if self.shoot_frequency >= 15:
                self.shoot_frequency = 0
        # bBullet 생성(when boss exist)
        if self.boss_state==True:
            if self.shoot_frequency % 100 == 0:
                self.bullet_sound.play()
                self.boss.shoot(self.bbullet_img)
            self.shoot_frequency += 1
            if self.shoot_frequency >= 15:
                self.shoot_frequency = 0
    
        # Enemy 생성 --> while문을 50번 돌 때마다 생성
        if self.enemy_frequency % 50 == 0:
            enemy_pos = [random.randint(0, self.conf['display']['W'] - self.enemy_rect.width), 0]
            enemy = Enemy(self.enemy_img, self.enemy_down_imgs, enemy_pos, self.EHP)
            self.enemies.add(enemy)
        self.enemy_frequency += 1
        if self.enemy_frequency >= 100:
            self.enemy_frequency = 0

        #boss 생성 --> 50000점마다 생성
        if self.score2 > 50000 and self.boss_state==False:
            self.score2-=50000
            self.boss_level+=1
            boss_pos = [random.randint(0, self.conf['display']['W'] - self.boss_rect.width), 0]
            boss = Boss(self.boss_img, self.boss_down_imgs, boss_pos, self.boss_level)        
            self.boss_state=True
        
        # Bullet 처리 : 총알이 화면을 벗어나면 총알 삭제
        for bullet in self.player.bullets:
            bullet.move()
            if pygame.sprite.collide_circle(bullet, self.boss) and self.boss_state==True:
                self.boss.HP-=1
                self.player.bullets.remove(bullet)
            if bullet.rect.bottom < 0:
                self.player.bullets.remove(bullet)
    

        # bBullet 처리 : 총알이 화면을 벗어나면 총알 삭제
        for bbullet in self.boss.bbullets:
            bbullet.move()
         #플레이어와 보스 총알의 충돌 감지
            if pygame.sprite.collide_circle(bbullet, self.player):
                self.enemies.remove(bbullet)
                self.player.is_hit = True
                self.game_over_sound.play()
                break
            if bbullet.rect.top > SCREEN_HEIGHT:
                self.boss.bbullets.remove(bbullet)
        
        # Enemy 처리
        for enemy in self.enemies:
            enemy.move()
            # 플레이어와 적의 충돌 감지
            if pygame.sprite.collide_circle(enemy, self.player):
                self.enemies_down.add(enemy)
                self.enemies.remove(enemy)
                self.player.is_hit = True
                self.game_over_sound.play()
                break
            if pygame.sprite.collide_circle(enemy, self.player):
                self.enemies_down.add(enemy)
                self.enemies.remove(enemy)
                self.player.is_hit = True
                self.game_over_sound.play()
                break

            
            # 적이 화면을 벗어나면 적을 삭제
            if enemy.rect.top > self.conf['display']['H']:
                self.enemies.remove(enemy)

        #보스와 플레이어의 충돌 감지
        if pygame.sprite.collide_circle(self.boss, self.player) and boss_state==True:
            self.boss.remove
            self.player.is_hit = True
            self.game_over_sound.play()
            
        # Player의 총알 맞은 enemies 처리
        cur_enemies_down = pygame.sprite.groupcollide(self.enemies, self.player.bullets, 1, 1)
        for enemy_down in cur_enemies_down:
            self.enemies_down.add(enemy_down)

        #적이 죽을 때 경험치 1 획득, 2^(플레이어 레벨)이 레벨업 조건(현재 상한 없음)
        for enemy_down in self.enemies_down: 
            enemy_down.HP -= 1
            if enemy_down.HP == 0:
                self.enemy_down_sound.play()
            if enemy_down.down_index >= 7:
                self.enemies_down.remove(enemy_down)
                self.score += 1000
                self.score2 +=2000
                self.player.killed+=1
                continue
            enemy_down.down_index += 1
        
        # Player 레벨 조절
        if self.player.killed>=2**self.player.level:
            self.player.level += 1
            self.player.killed -= 2**self.player.level
            self.player.speed += 1 


    def draw(self):
        screen = self.screen
        player = self.player
        boss = self.boss

        # Background
        screen.fill(0)
        screen.blit(self.background_img, (0, 0))
        
        # Entities
        self.player.draw(self.screen, self.shoot_frequency)
        if self.boss_state==True:
            self.boss.draw(self.screen)
        for enemy_down in self.enemies_down: 
            enemy_down.down_draw(screen)
        self.enemies.draw(screen)

        # 점수 표기
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(self.score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # 게임 스크린 업데이트
        pygame.display.update()


    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # 종료 버튼
                pygame.mixer_music.stop()
                exit()

        key_pressed = pygame.key.get_pressed()
        if not self.player.is_hit:
            if key_pressed[K_LEFT] or key_pressed[K_a]:
                self.player.moveLeft()
            if key_pressed[K_RIGHT] or key_pressed[K_d]:
                self.player.moveRight()
            if key_pressed[K_UP] or key_pressed[K_w]:
                self.player.moveUp()
            if key_pressed[K_DOWN] or key_pressed[K_s]:
                self.player.moveDown()

    def draw_gameover(self, screen):
        font = pygame.font.Font(None, 48)
        text = font.render('Score: '+ str(self.score), True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 24
        screen.blit(self.gameover_img, (0, 0))
        screen.blit(text, text_rect)
