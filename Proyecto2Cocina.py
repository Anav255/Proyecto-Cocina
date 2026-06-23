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
fuente_pequena = pygame.font.SysFont(None, 30)

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

    def picar_ingredientes(self):
        for ingrediente in self.inventario:
            if ingrediente.nombre in [
                "Lechuga",
                "Tomate",
                "Cebolla"
            ]:
                ingrediente.picado = True

        print("Ingredientes picados")
    
chef1 = Chef(100,250, (255, 0, 0))
chef2 = Chef(100,300, (0, 0, 255))
chef_activo = chef1


#--- Clases ingredientes ----------------------

class Ingrediente:
    def __init__(self, nombre, ruta_imagen, ruta_picado=None):
        self.nombre = nombre
        self.imagen = pygame.image.load(ruta_imagen)
        
        if ruta_picado:
            self.imagen_picada = pygame.image.load(
                ruta_picado
            )
        else:
            self.imagen_picada = self.imagen

        self.picado = False
        

    
ingredientes_faltantes = [
Ingrediente("Lechuga","img/lechuga.png", "img/lechugapicada.png"),
Ingrediente("Tomate","img/tomate.png", "img/tomatepicado.png"),
Ingrediente("Cebolla","img/cebolla.png", "img/cebollapicada.png"),
Ingrediente("Pan","img/pan.png", None),
Ingrediente("Queso","img/queso.png", None),
Ingrediente("Carne","img/carne.png", None),
Ingrediente("Papas","img/papas.png", None),
Ingrediente("Postre","img/postre.png", None)]
    
#-----------------Crear estaciones ------------------------------------

class Estacion:
    def __init__(self, x, y, color, nombre, ingrediente = None, imagen = None):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.color = color
        self.nombre = nombre
        self.ingrediente = ingrediente
        self.imagen = pygame.image.load(imagen)
        self.imagen = pygame.transform.scale(
            self.imagen,
            (100,100)
        )
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def draw(self, screen):

        screen.blit(
            self.imagen,
            (self.x,self.y)
        )




boton_play = pygame.Rect(300, 300, 200, 80)

#-------------------- Estaciones ------------------------------

despensa_lechuga = Estacion( #verde
    250,
    380,
    (0,255,0),
    "Lechuga",
    Ingrediente("Lechuga","img/lechuga.png"),
    "img/cajalechuga.png"
)

despensa_tomate = Estacion( #rojo
    130,
    370,
    (255,0,0),
    "Tomate",
    Ingrediente("Tomate","img/tomate.png"),
    "img/cajatomate.png"
)

despensa_cebolla = Estacion( #Morado
    20,
    370,
    (140,90,0),
    "Cebolla",
    Ingrediente("Cebolla","img/cebolla.png"),
    "img/cajacebolla.png"
)

despensa_queso = Estacion( 
    350,
    370,
    (140,90,0),
    "Cebolla",
    Ingrediente("Queso","img/queso.png"),
    "img/cajaquesho.png"
)

despensa_carne = Estacion( #verde
    450,
    380,
    (0,255,0),
    "Carne",
    Ingrediente("Carne","img/carne.png"),
    "img/refricarne.jpeg"
)

tabla_picar = Estacion(
    600,
    380,
    (139,69,19),
    "Tabla",
    None,
    "img/tabla.png"
)

cocina = Estacion(
    350,
    100,
    (100,100,100),
    "Cocina",
    None,
    "img/cocina.png"
)

freidora = Estacion(
    500,
    95,
    (255,165,0),
    "Freidora",
    None,
    "img/freidora.png"
)

refrigeradora = Estacion(
    650,
    110,
    (255,165,0),
    "Refrigeradora",
    None,
    "img/refrigeradora.png"
)

entrega = Estacion(
    130,
    95,
    (0,0,255),
    "Entrega",
    None,
    "img/bandeja.png"
)

estaciones = [
    despensa_lechuga, despensa_tomate, despensa_cebolla, despensa_queso, despensa_carne,
    tabla_picar, cocina, freidora, refrigeradora,
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
        ingredientes = [
            "Pan",
            "Carne",
            "Queso"
        ]

        extras = [
            "Lechuga",
            "Tomate",
            "Cebolla"
        ]

        ingredientes += random.sample(
            extras,
            2
        )

        return Orden(
            2,
            "Hamburguesa",
            ingredientes
        )

#---------- Niveles ----------------------------------------

PedidosNivel = {
        1: [Orden(1, "Ensalada LT", ["Lechuga", "Tomate"]),
            Orden(1, "Ensalada LC", ["Lechuga", "Cebolla"]),
            Orden(1, "Ensalada LTC", ["Lechuga", "Tomate", "Cebolla"])],
        2: [Orden.orden_hamburguesa()]}


#-------- Hacer pedidos ---------------------------------------

# Orden pedidos 
Pedidos = pygame.USEREVENT + 1

def timer_pedidos(nivel):
    if nivel == 1:
        pygame.time.set_timer(Pedidos, 10_000)
    elif nivel == 2:
        pygame.time.set_timer(Pedidos, 20_000)

nivel_actual = 1
puntaje = 0
pedidos_completados = 0
escenario_actual = 1

def generar_pedido(nivel):
    if nivel == 1:

        return random.choice([
            Orden(1, "Ensalada LT", ["Lechuga", "Tomate"]),

            Orden(1, "Ensalada LC", ["Lechuga", "Cebolla"]),

            Orden(1, "Ensalada LTC", ["Lechuga", "Tomate", "Cebolla"])
        ])

        pedido = random.choice(PedidosNivel[1])

    elif nivel == 2:
        return random.choice([
            Orden(2, "Hamburguesa", ["Pan", "Carne", "Queso"]),

            Orden(2, "Hamburguesa Especial", ["Pan", "Carne", "Tomate", "Lechuga"])
        ])
    
    else:
        return random.choice([
            Orden(3, "Combo", ["Pan", "Carne", "Queso", "Papas"])
        ])
        
    


def verificar_nivel():
    global nivel_actual

    if pedidos_completados >=10:
        nivel_actual = 3

    elif pedidos_completados >= 5:
        nivel_actual = 2
    
    cambiar_escenario()

def cambiar_escenario():
    global escenario_actual

    if nivel_actual == 1:
        escenario_actual = 1
    elif nivel_actual == 2:
        escenario_actual = 2
    elif nivel_actual == 3:
        escenario_actual = 3

pedido_actual = generar_pedido(nivel_actual)
tiempo_juego = 120
tiempo_inicio = pygame.time.get_ticks()

def mostrar_inventario(chef, x, y):
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (x, y, 220, 80)
    )

    titulo = fuente_pequena.render(
        "Inventario",
        True,
        (0,0,0)
    )

    screen.blit(
        titulo,
        (x+10,y+5)
    )

    for i, ingrediente in enumerate(chef.inventario):

        if ingrediente.picado:
            imagen_actual = ingrediente.imagen_picada

        else:
            imagen_actual = ingrediente.imagen

        imagen = pygame.transform.scale(
            imagen_actual,
            (45,45)
        )

        screen.blit(
            imagen,
            (
                x+10+(i*50),
                y+30
            )
        )

        

pedido_actual = generar_pedido(nivel_actual)

def dibujar_cocina():#para que cambie el escenario dependiendo del nivel
    if escenario_actual == 1:
        color_piso = (220,220,220)
    elif escenario_actual == 2:
        color_piso(180,180,220)
    else:
        color_piso = (220,180,180)
    
    screen.fill(color_piso)

def cargar_escenario():
    if escenario_actual == 1:
        cocina.x = 350
        cocina.y = 100

        freidora.x = 500
        freidora.y = 100

    elif escenario_actual == 2:
        cocina.x = 100
        cocina.y = 100

        freidora.x = 600
        freidora.y = 100

        tabla_picar.x = 400
        tabla_picar.y = 300

    elif escenario_actual == 3:
        cocina.x = 300
        cocina.y = 250

        freidora.x = 500
        freidora.y = 250


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

                            if pedido_actual.verficar(chef_activo.inventario):
                                

                            print(f"Necesitas: {pedido_actual.ingredientesNecesarios}")
                            if pedido_actual.verificar(chef_activo.inventario):

                                print("Pedido actual entregado")

                                puntaje += 100
                                pedidos_completados += 1

                                verificar_nivel()

                                chef_activo.inventario.clear()
                                pedido_actual = generar_pedido(nivel_actual)
                                
                            else:
                                print("Pedido incorrecto")
                                chef_activo.inventario.clear()

                        elif estacion.ingrediente:
                            chef_activo.agarrar_ingrediente(estacion.ingrediente)
                            break
                        elif estacion.nombre == "Tabla":
                            chef_activo.picar_ingredientes()

    dibujar_cocina()

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
        cargar_escenario()

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
            

        #Encimera cafe - mostrador arriba
        pygame.draw.rect(
            screen,
            (150,80,40),
            (0,120,WIDTH,60)
        )
        #Encimera cafe - mostrador abajo
        pygame.draw.rect(
            screen,
            (150,80,40),
            (0,400,WIDTH,60)
        )


        #--- Caja pedidos ---
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (20,10,350,100)
        )

        titulo = fuente_pequena.render(
            pedido_actual.pedido,
            True,
            (0,0,0)
        )

        texto_nombre = fuente_pequena.render(
            pedido_actual.pedido,
            True,
            (0,0,0)
        )

        screen.blit(
            texto_nombre,
            (30,15)
        )

        for i, nombre in enumerate(
            pedido_actual.ingredientesNecesarios
        ):
            for ingrediente in ingredientes_faltantes:
                if ingrediente.nombre == nombre:

                    imagen = pygame.transform.scale(
                        ingrediente.imagen,
                        (45,45)
                    )
                    
                    screen.blit(
                        imagen,
                        (
                            40+(i*50),
                            50
                        )
                    )

        texto_nivel = fuente_boton.render(
            f"Nivel {nivel_actual}",
            True,
            (0,0,255)
        )

        texto_puntos = fuente_boton.render(
            f"Puntos {puntaje}",
            True,
            (0,150,0)
        )
        

        for i, ingrediente in enumerate(chef_activo.inventario):

            texto_ing = pygame.font.SysFont(
                None,
                30
            ).render(
                ingrediente.nombre,
                True,
                (0,0,0)
            )
            screen.blit(
                texto_ing,
                (
                    180 + i * 120,
                    45
                )
            )

        #--- caja nivel ---
        pygame.draw.rect(
            screen,
            (255,255,255),
            (400,10,150,70)
        )

        screen.blit(
            texto_nivel,
            (420,25)
        )

        #--- caja puntos ---
        pygame.draw.rect(
            screen,
            (255,255,255),
            (620,10,150,70)
        )

        screen.blit(
            texto_puntos,
            (635,25)
        )


        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (350, HEIGHT-90, 100, 80)
        )

        tiempo_pasado = (
            pygame.time.get_ticks()-tiempo_inicio
        )//1000

        tiempo_restante = tiempo_juego - tiempo_pasado

        texto_tiempo = fuente_pequena.render(
            f"{tiempo_restante}s",
            True,
            (0,0,0)
        )
        screen.blit(
            texto_tiempo,
            (375, HEIGHT-55)
        )

        #Ensenar estaciones en la cuadricula
        despensa_lechuga.draw(screen)
        despensa_tomate.draw(screen)
        despensa_cebolla.draw(screen)
        despensa_queso.draw(screen)
        despensa_carne.draw(screen)
        tabla_picar.draw(screen)
        cocina.draw(screen)
        refrigeradora.draw(screen)
        freidora.draw(screen)
        entrega.draw(screen)

        #ensenar ambor chefs dentro de cuadricula
        chef1.draw(screen)
        chef2.draw(screen)

        keys = pygame.key.get_pressed()
        chef_activo.move(keys)
        
        #Muestra inventarios en pantalla
        mostrar_inventario(
            chef1,
            20,
            HEIGHT-90
        )

        mostrar_inventario(
            chef2,
            WIDTH-240,
            HEIGHT-90
        )

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