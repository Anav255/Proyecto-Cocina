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
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        window.fill((255, 255, 255))
        clck.tick(FPS)


class ingredientes:
    def __init__(self, Lechuga, Tomate, Cebolla, Pan,):
        pass 
class Ensalada:
    #El nombre de las ensaladas lo estoy definiendo según los ingredientes siendo L = Lechuga T= Tomate C= Cebolla, por cualquier cosa de que los vaya a tener que usar  
     
    def __init__(self, EnsaladaLT, EnsaladaLC, EnsaladaLTC):
        self.EnsaladaLT = [self.Lechuga, self.Tomate,]
        self.EnsaladaLT = [self.Lechuga, self.Cebolla,]
        self.EnsaladaLT = [self.Lechuga, self.Tomate, self.Cebolla]
        
        pass
     
    














        pygame.display.flip()
pygame.quit()