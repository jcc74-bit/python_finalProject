# Program: Pygame Final Project
# Author: Jiaxin Chen
# Purpose: Coding a 2d Game

import pygame

pygame.init()

win = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space War")

walkRight = []
walkLeft = []
bg = pygame.image.load('bg.png')
char = pygame.image.load()

clock = pygame.time.Clock()


pygame.quit()
