### Juego cocina ###
import random
import time
import os
import sys
import pygame
from pygame.locals import *
pygame.init()


#--- Configuración de la pantalla ------------------------

WIDTH, HEIGHT = 800, 600
Tile_size = 25 # tamano Cuadricula de cocina

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crazy Snack Rush")  

clock = pygame.time.Clock()
FPS = 60
running = True
estado = "menu"

fuente_titulo = pygame.font.SysFont(None, 80)
fuente_boton = pygame.font.SysFont(None, 50)

#--- Crear Chef ------------------------------------------------

class Chef:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = 40
        self.color = color
        self.inventario = []

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.size, self.size)
        )

    def move(self, keys):#movimiento del chef

        speed = 5

        if keys[pygame.K_w]:
            self.y -= speed

        if keys[pygame.K_s]:
            self.y += speed

        if keys[pygame.K_a]:
            self.x -= speed

        if keys[pygame.K_d]:
            self.x += speed

    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

    def agarrar_ingrediente(self, ingrediente):
        if len(self.inventario) < 4:
            self.inventario.append(ingrediente)
            ingredientes = [i.nombre for i in self.inventario]
            print(f"ingredientes actuales {ingredientes}")
        else: 
            print("inventario lleno")    
    

#--- Clases ingredientes ----------------------

class Ingrediente:
    def __init__(self, nombre, ruta_imagen):
        self.nombre = nombre
        self.imagen = pygame.image.load(ruta_imagen)

    
ingredientes_faltantes = [
Ingrediente("Cebolla","img/cebolla.png"),
Ingrediente("Pan","img/pan.png"),
Ingrediente("Queso","img/queso.png"),
Ingrediente("Carne","img/carne.png")]
    
#-----------------Crear estaciones ------------------------------------

class Estacion:
    def __init__(self, x, y, color, nombre, ingrediente = None):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = color
        self.nombre = nombre
        self.ingrediente = ingrediente
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.width, self.height)
        )


chef1 = Chef(100,100, (255, 0, 0))
chef2 = Chef(300,100, (0, 0, 255))
chef_activo = chef1

boton_play = pygame.Rect(300, 300, 200, 80)

#-------------------- Estaciones ------------------------------

despensa_lechuga = Estacion(
    50,
    50,
    (0,255,0),
    "Lechuga",
    Ingrediente("Lechuga","img/lechuga.png")
)

despensa_tomate = Estacion(
    150,
    50,
    (255,0,0),
    "Tomate",
    Ingrediente("Tomate","img/tomate.png")
)

tabla_picar = Estacion(
    150,
    50,
    (139,69,19),
    "Tabla"
)

cocina = Estacion(
    650,
    50,
    (100,100,100),
    "Cocina"
)

freidora = Estacion(
    750,
    50,
    (255,165,0),
    "Freidora"
)

entrega = Estacion(
    350,
    500,
    (0,0,255),
    "Entrega"
)

estaciones = [
    despensa_lechuga, despensa_tomate,
    tabla_picar, cocina, freidora,
    entrega
]

 
#--- Clase Orden ----------------------

class Orden:
    def __init__(self, nivel, pedido, ingredientesNecesarios):
        self.nivel = nivel
        self.pedido = pedido
        self.ingredientesNecesarios = ingredientesNecesarios

    def __str__(self):
        return f"{self.pedido} - ingredientes: {self.ingredientesNecesarios}"

    def verificar(self, inventarioChef):
        ingredientes = [i.nombre for i in inventarioChef]
        return all(ing in ingredientes for ing in self.ingredientesNecesarios)
    

    def agarrar_ingrediente(self, ingrediente):
        if len(self.inventario) < 4:
            self.inventario.append(ingrediente)
            ingredientes = [i.nombre for i in self.inventario]
            print(f"ingredientes actuales {ingredientes}")
        else: 
            print("inventario lleno")    
    

    def orden_hamburguesa():
        base = ["Pan", "Carne"]
        extras = ["Queso", "Tomate", "Lechuga", "Cebolla"]
        agregarextras = random.sample(extras, 2)
        ingredientes = base + agregarextras
        return Orden(2, "Hamburguesa", ingredientes)

PedidosNivel = {
        1: [Orden(1, "Ensalada LT", ["Lechuga", "Tomate"]),
            Orden(1, "Ensalada LC", ["Lechuga", "Cebolla"]),
            Orden(1, "Ensalada LTC", ["Lechuga", "Tomate", "Cebolla"])],
        2: [Orden.orden_hamburguesa()]}

# Orden pedidos 
Pedidos = pygame.USEREVENT + 1

def timer_pedidos(nivel):
    if nivel == 1:
        pygame.time.set_timer(Pedidos, 10_000)
    elif nivel == 2:
        pygame.time.set_timer(Pedidos, 20_000)

nivel_actual = 1
def generar_pedido(nivel):
    if nivel == 1:
        pedido = random.choice(PedidosNivel[1])
    elif nivel == 2:
        pedido = PedidosNivel[2]
    
    print(f"Pedido actual: {pedido} ")
    return pedido

pedido_actual = generar_pedido(nivel_actual)

#------------ Ciclo principal ---------------------------------

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if estado ==  "menu":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if boton_play.collidepoint(event.pos):
                    estado = "juego"
                    timer_pedidos(nivel_actual)
        
        if event.type == Pedidos:
            if estado == "juego":
                pedido_actual = generar_pedido(nivel_actual)
        
        if event.type == pygame.KEYDOWN:#cuando se presiona
            if event.key == pygame.K_TAB:#si la tecla que se presiona es TAB
                if chef_activo == chef1:#revisa el chef actual es chef1 y se cambia
                    chef_activo = chef2
                else:
                    chef_activo = chef1#Si no es chef1, entonces significa que es chef2: se cambia a chef1.
           
            if event.key == pygame.K_e: #Esta parte lo que hace es que el juego reacciona si el chef toca la letra e cerca de una estación
                for estacion in estaciones:
                    if chef_activo.get_rect().colliderect(estacion.rect):
                        print(f"Estacion actual: {estacion.nombre}")

                        if estacion.nombre == "Entrega":
                            print(f"Necesitas: {pedido_actual.ingredientesNecesarios}")
                            if pedido_actual.verificar(chef_activo.inventario):
                                print("Pedido actual entregado")
                                chef_activo.inventario.clear()
                                pedido_actual = generar_pedido(nivel_actual)
                                tiempo_ultimo_pedido = pygame.time.get_ticks()
                            else:
                                print("Pedido incorrecto")
                                chef_activo.inventario.clear()

                        elif estacion.ingrediente:
                            chef_activo.agarrar_ingrediente(estacion.ingrediente)
                            break
    screen.fill((255,255,255))

    if estado == "menu": #lo que ensena si esta en el menu
        titulo = fuente_titulo.render(
            "CRAZY SNACK RUSH",
            True,
            (0,0,0)
        )

        texto_play = fuente_boton.render(
            "PLAY",
            True,
            (255,255,255)
        )

        pygame.draw.rect(
            screen,
            (0,150,0),
            boton_play
        )

        screen.blit(titulo, (120,150))
        screen.blit(texto_play, (355,325))

    if estado == "juego":#lo que ensena si esta en el juego

        for fila in range(0, HEIGHT, Tile_size):
            for columna in range(0, WIDTH, Tile_size):

                if ((fila // Tile_size) + (columna // Tile_size)) % 2 == 0:

                    color = (225, 225, 225)

                else:
                    color = (40,40,40)

                pygame.draw.rect(
                    screen,
                    color,
                    (columna, fila, Tile_size, Tile_size)
                )

        pygame.draw.rect(
            screen,
            (120,80,40),
            (0,50,WIDTH,50)
        )

        #Ensenar estaciones en la cuadricula
        despensa_lechuga.draw(screen)
        despensa_tomate.draw(screen)
        tabla_picar.draw(screen)
        cocina.draw(screen)
        freidora.draw(screen)
        entrega.draw(screen)

        #ensenar ambor chefs dentro de cuadricula
        chef1.draw(screen)
        chef2.draw(screen)

        keys = pygame.key.get_pressed()
        chef_activo.move(keys)

        chef_rect = chef_activo.get_rect()

        for estacion in estaciones:
            if chef_rect.colliderect(estacion.rect):
                texto = fuente_boton.render(
                    "E",
                    True,
                    (255,0,0)
                )
                screen.blit(
                    texto,
                    (
                        estacion.x + 15,
                        estacion.y - 40
                    )
                )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()