### Juego cocina ###
import pygame
from pygame.locals import *
import time
import random
pygame.init()
# Pantalla juego
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Cocina")   

FPS = 60
running = True

def main(window):
    clck = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        window.fill((255, 255, 255))
        clck.tick(FPS)


        pygame.display.flip()
pygame.quit()