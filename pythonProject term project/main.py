# Program: Pygame Final Project
# Author: Jiaxin Chen
# Purpose: Coding a 2d Game

import pygame
pygame.init()
import random
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1200
screen_height = 700
img_sz = (75, 50)
bullet_sz = (30, 20)

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

hit = pygame.mixer.Sound('lazergunhitsound.mp3')
gun = pygame.mixer.Sound('lazergunsound.mp3')
song = pygame.mixer.Sound('themesound.mp3')


rows = 4
cols = 11

aliencd = 800
lstalienshot = pygame.time.get_ticks()

red = (255, 0, 0)
green = (0, 255, 0)

bg = pygame.image.load('bg.png')
song.play()

def draw_bg():
    win.blit(bg, (0, 0))

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__()
        self.image = pygame.image.load('person_ship.png')
        self.image = pygame.transform.scale(self.image, img_sz)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        speed = 8
        cooldown = 500

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            gun.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        self.mask = pygame.mask.from_surface(self.image)

        pygame.draw.rect(win, red, (self.rect.x, self.rect.bottom + 10, self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(win, green, (self.rect.x, self.rect.bottom + 10, int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bullet1.png')
        self.image = pygame.transform.scale(self.image, bullet_sz)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            hit.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("alien" + str(random.randint(1, 8)) + ".png")
        self.image = pygame.transform.scale(self.image, img_sz)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 100:
            self.move_direction *= -1
            self.move_counter = 0

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('AlienBullet.png')
        self.image = pygame.transform.scale(self.image, bullet_sz)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 8
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.images = []  # Fixed the list initialization
        for num in range(1, 9):
            img = pygame.image.load(f"exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (120, 120))
            self.images.append(img)  # Fixed the append method
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        expspeed = 3
        self.counter += 1
        if self.counter >= expspeed and self.index < len(self.images) - 1:  # Fixed the indexing error
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= expspeed:
            self.kill()

spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

def create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)

create_aliens()

spaceship = Spaceship(int(screen_width // 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

run = True
while run:
    clock.tick(fps)

    draw_bg()

    time_now = pygame.time.get_ticks()
    if time_now - lstalienshot > aliencd and len(alien_bullet_group) < 7 and len(alien_group) > 0:
        if alien_group.sprites():
            attackalien = random.choice(alien_group.sprites())
            alien_bullet = AlienBullet(attackalien.rect.centerx, attackalien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            lstalienshot = time_now

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    spaceship.update()
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()
    explosion_group.update()

    spaceship_group.draw(win)
    bullet_group.draw(win)
    alien_group.draw(win)
    alien_bullet_group.draw(win)
    explosion_group.draw(win)

    pygame.display.update()

pygame.quit()
