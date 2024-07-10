import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image, rects, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for rect in rects:
            self.image.append(image.subsurface(rect).convert_alpha())
        self.rect = rects[0]
        self.rect.topleft = pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.is_hit = False
        self.img_index = 0
        self.is_invincible = False
        self.invincibility_timer = 0

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.bottom < 600:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.right < 480:
            self.rect.left += self.speed

    def update(self):
        if self.is_invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.is_invincible = False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, down_images, pos, speed=2, points=100, behavior='straight'):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.down_images = down_images
        self.down_index = 0
        self.speed = speed
        self.points = points
        self.behavior = behavior

    def move(self):
        if self.behavior == 'straight':
            self.rect.top += self.speed
        elif self.behavior == 'zigzag':
            self.rect.top += self.speed
            self.rect.left += self.speed if self.rect.top % 20 < 10 else -self.speed

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, pos, effect):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.effect = effect
        self.speed = 2

    def move(self):
        self.rect.top += self.speed

class Boss(pygame.sprite.Sprite):
    def __init__(self, image, down_images, pos, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.down_images = down_images
        self.down_index = 0
        self.health = health
        self.speed = 1

    def move(self):
        self.rect.top += self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            