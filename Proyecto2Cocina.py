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
fondo_menu = pygame.image.load("img/fondo.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, (WIDTH, HEIGHT))

fuente_titulo = pygame.font.SysFont(None, 80)
fuente_boton = pygame.font.SysFont(None, 50)
fuente_pequena = pygame.font.SysFont(None, 30)

#--- Crear Chef ------------------------------------------------

class Chef:

    def __init__(self, x, y, color, ruta_imagen):
        self.x = x
        self.y = y
        self.size = 40
        self.size_visual = 110
        self.color = color
        self.inventario = []
        self.direccion = "arriba"  # dirección inicial
        self.imagen_original = pygame.image.load(ruta_imagen)
        self.imagen_original = pygame.transform.scale(self.imagen_original, (self.size_visual, self.size_visual))
        

    def draw(self, screen):

        if self.direccion == "arriba":
            imagen = self.imagen_original 
        elif self.direccion == "abajo":
            imagen = pygame.transform.rotate(self.imagen_original, 180)
        elif self.direccion == "izquierda":
            imagen = pygame.transform.rotate(self.imagen_original, 90)
        elif self.direccion == "derecha":
            imagen = pygame.transform.rotate(self.imagen_original, -90)
        offset = (self.size_visual - self.size) // 2
        screen.blit(imagen, (self.x - offset, self.y - offset))

    def move(self, keys, chef2):#movimiento del chef

        speed = 5
        x = self.x
        y = self.y

        if keys[pygame.K_w]:
            self.y -= speed
            self.direccion = "arriba"

        if keys[pygame.K_s]:
            self.y += speed
            self.direccion = "abajo"
        if keys[pygame.K_a]:
            self.x -= speed
            self.direccion = "izquierda"

        if keys[pygame.K_d]:
            self.x += speed
            self.direccion = "derecha"

        # limites de la pantalla
        self.x = max(0, min(self.x, WIDTH - self.size))
        self.y = max(180, min(self.y, 360))

        if chef2 is not None:
            chef2_rect = chef2.get_rect()
            if self.get_rect().colliderect(chef2_rect):
                self.x = x
                self.y = y

                 

    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

    def agarrar_ingrediente(self, ingrediente, nivel = 1):
        limite = 5 if nivel == 3 else 4
        if len(self.inventario) < limite:
            nuevo = Ingrediente(
                ingrediente.nombre, ingrediente.ruta_imagen if hasattr(ingrediente, 'ruta_imagen') else None,
                ingrediente.ruta_picado if hasattr(ingrediente, 'ruta_picado') else None,
                ingrediente.ruta_cocinado if hasattr(ingrediente, 'ruta_cocinado') else None,
                ingrediente.ruta_frito if hasattr(ingrediente, 'ruta_freido') else None)
            nuevo.imagen = ingrediente.imagen.copy()
            nuevo.imagen_picada = ingrediente.imagen_picada.copy() 
            nuevo.imagen_cocinada = ingrediente.imagen_cocinada.copy()
            nuevo.imagen_frita = ingrediente.imagen_frita.copy()
            self.inventario.append(nuevo)
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
                ingrediente.imagen = ingrediente.imagen_picada
                ingrediente.picado = True  
                ingrediente.nombre = ingrediente.nombre + " picado"
        print("Ingredientes picados")
    
    def cocinar_ingredientes(self):
        for ingrediente in self.inventario:
            if ingrediente.nombre == "Carne":
                ingrediente.imagen = ingrediente.imagen_cocinada
                ingrediente.cocinado = True
                ingrediente.nombre = "Carne cocinada"
        print("Ingredientes cocinados")

    def freir_ingredientes(self):
        for ingrediente in self.inventario:
            if ingrediente.nombre == "Papas":
                ingrediente.imagen = ingrediente.imagen_frita
                ingrediente.frito = True
                ingrediente.nombre = "Papas fritas"
        print("Ingredientes fritos")

    
chef1 = Chef(100,250, (255, 0, 0), "img/chef1.png")
chef2 = Chef(100,300, (0, 0, 255), "img/chef2.png")
chef_activo = chef1

#--- Clases ingredientes ----------------------

class Ingrediente:
    def __init__(self, nombre, ruta_imagen, ruta_picado=None, ruta_cocinada=None, ruta_frita = None):
        self.nombre = nombre
        self.imagen = ruta_imagen
        self.ruta_picado = ruta_picado
        self.ruta_cocinada = ruta_cocinada
        self.ruta_frita = ruta_frita
        if ruta_imagen:
            self.imagen = pygame.image.load(ruta_imagen)
        else:
            self.imagen = None
            
        if ruta_picado:
            self.imagen_picada = pygame.image.load(
                ruta_picado
            )
        else:
            self.imagen_picada = self.imagen

        if ruta_cocinada:
            self.imagen_cocinada = pygame.image.load(
                ruta_cocinada
            )
        else: 
            self.imagen_cocinada = self.imagen
        
        if ruta_frita:
            self.imagen_frita = pygame.image.load(
                ruta_frita
            )
        else: 
            self.imagen_frita = self.imagen
        
        self.picado = False
        self.cocinado = False
        self.frito = False
        

    
ingredientes_faltantes = [
Ingrediente("Lechuga", "img/lechuga.png", "img/lechugapicada.png", None, None),
Ingrediente("Tomate", "img/tomate.png", "img/tomatepicado.png",  None, None),
Ingrediente("Cebolla", "img/cebolla.png", "img/cebollapicada.png", None, None),
Ingrediente("Pan", "img/pan.png", None, None, None),
Ingrediente("Queso", "img/queso.png", None, None, None),
Ingrediente("Carne", "img/carne.png", None, "img/carnecocinada.png", None),
Ingrediente("Papas", "img/papas.png", None, None, "img/papasfritas.png"),
Ingrediente("Gaseosa", "img/gaseosa.png", None, None, None),
Ingrediente("Postre", "img/postre.png", None, None, None)]
    
#-----------------Crear estaciones ------------------------------------

class Estacion:
    def __init__(self, x, y, color, nombre, ingrediente = None, imagen = None, niveles= None):
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
        self.niveles = niveles if niveles is not None else [1, 2, 3]

    def draw(self, screen):

        screen.blit(
            self.imagen,
            (self.x,self.y)
        )


boton_play = pygame.Rect(300, 300, 200, 80)

#-------------------- Estaciones ------------------------------

despensa_lechuga = Estacion( #verde
    230,
    380,
    (0,255,0),
    "Lechuga",
    Ingrediente("Lechuga","img/lechuga.png", "img/lechugapicada.png"),
    "img/cajalechuga.png", niveles=[1,2,3]
)

despensa_tomate = Estacion( #rojo
    120,
    370,
    (255,0,0),
    "Tomate",
    Ingrediente("Tomate","img/tomate.png", "img/tomatepicado.png"),
    "img/cajatomate.png", niveles=[1,2,3]
)

despensa_cebolla = Estacion( #Morado
    10,
    370,
    (140,90,0),
    "Cebolla",
    Ingrediente("Cebolla","img/cebolla.png", "img/cebollapicada.png"),
    "img/cajacebolla.png", niveles=[1,2,3]
)

despensa_queso = Estacion( 
    330,
    370,
    (140,90,0),
    "Queso",
    Ingrediente("Queso","img/queso.png"),
    "img/cajaquesho.png", niveles=[2,3]
)

despensa_carne = Estacion(
650,
    380,
    (0,255,0),
    "Carne",
    Ingrediente("Carne","img/carne.png", None, "img/carnecocinada.png", None),
    "img/refricarne.jpeg", niveles=[2,3]
)

despensa_pan = Estacion(
    430,
    380,
    (255,255,0),
    "Pan",
    Ingrediente("Pan","img/pan.png"),
    "img/cajapan.png", niveles=[2,3]
)
despensa_papas = Estacion(
    540,
    380,
    (255,255,0),
    "Papas",
    Ingrediente("Papas","img/papas.png", None, None, "img/papasfritas.png"),
    "img/cajapapas.png", niveles=[3]
)

basurero = Estacion(
    10,
    95,
    (0,0,0),
    "Basurero",
    None,
    "img/basurero.png", niveles=[1,2,3]
)

tabla_picar = Estacion(
    650,
    380,
    (139,69,19),
    "Tabla",
    None,
    "img/tabla.png", niveles=[1,2,3]
)

cocina = Estacion(
    600,
    100,
    (100,100,100),
    "Cocina",
    None,
    "img/cocina.png", niveles=[2,3]
)

freidora = Estacion(
    540,
    95,
    (255,165,0),
    "Freidora",
    None,
    "img/freidora.png", niveles=[3]
)

refrigeradora = Estacion(
    660,
    100,
    (255,165,0),
    "Refrigeradora",
    None,
    "img/refrigeradora.png", niveles=[3]
)

entrega = Estacion(
    120,
    95,
    (0,0,255),
    "Entrega",
    None,
    "img/bandeja.png", niveles=[1,2,3]
)

estaciones = [
    despensa_lechuga, despensa_tomate, despensa_cebolla, despensa_queso, despensa_carne,despensa_pan, despensa_papas,
    basurero, tabla_picar, cocina, freidora, refrigeradora,entrega
]


#--- Clase Orden ----------------------

class Orden:
    def __init__(self, nivel, pedido, ingredientesNecesarios, requierePicar=False, requiereCocinar=False, requiereFreir=False):
        self.nivel = nivel
        self.pedido = pedido
        self.ingredientesNecesarios = ingredientesNecesarios
        self.requierePicar = requierePicar
        self.requiereCocinar = requiereCocinar
        self.requiereFreir = requiereFreir


    def __str__(self):
        return f"{self.pedido} - ingredientes: {self.ingredientesNecesarios}"

    def verificar(self, inventarioChef):
        for ing_necesario in self.ingredientesNecesarios:
            encontrado = False
            for ing in inventarioChef:
                nombre_base = ing.nombre.replace(" picado", "").replace(" cocinada", "").replace(" fritas", "")
                if nombre_base == ing_necesario:
                    if self.requierePicar and ing_necesario in ["Lechuga", "Tomate", "Cebolla"] and not ing.picado:
                        return False
                    if self.requiereCocinar and ing_necesario == "Carne" and not ing.cocinado:
                        return False
                    if self.requiereFreir and ing_necesario == "Papas" and not ing.frito:
                        return False
                    encontrado = True
                    break
            if not encontrado:
                return False
        return True
    

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
        ]

        extras = [
            "Lechuga",
            "Tomate",
            "Cebolla",
            "Queso"
        ]

        ingredientes += random.sample(
            extras,
            2
        )

        return Orden(
            2,
            "Hamburguesa",
            ingredientes,
            requiereCocinar = True,
            requierePicar = True
        )
    def orden_3():
        ingredientes = [
        "Pan",
        "Carne",
        "Papas",
    ]
        extras1 = [
            "Lechuga",
            "Tomate",
            "Cebolla",
            "Queso"
        ]

        extras2 = [
        "Gaseosa",
        "Postre",
    ]

        ingredientes += random.sample(extras1, 1) + random.sample(extras2,1)

        return Orden(
        3,
        "Combo",
        ingredientes,
        requierePicar = True,
        requiereCocinar=True,
        requiereFreir=True,
    )


#---------- Niveles ----------------------------------------

PedidosNivel = {
        1: [Orden(1, "Ensalada LT", ["Lechuga", "Tomate"], requierePicar=True),
            Orden(1, "Ensalada LC", ["Lechuga", "Cebolla"], requierePicar=True),
            Orden(1, "Ensalada LTC", ["Lechuga", "Tomate", "Cebolla"], requierePicar=True)],
        2: [Orden.orden_hamburguesa()],
        3: [Orden.orden_3()]}



#-------- Hacer pedidos ---------------------------------------

# Orden pedidos 
Pedidos = pygame.USEREVENT + 1

def timer_pedidos(nivel):
    if nivel == 1:
        tiempo = random.randint(15, 20)
    elif nivel == 2:
        tiempo = random.randint(25, 30)
    else:
        tiempo = random.randint(25, 30)
    
    pygame.time.set_timer(Pedidos, tiempo * 1000)
    return tiempo

nivel_actual = 1
puntaje = 0
pedidos_completados = 0
escenario_actual = 1

def generar_pedido(nivel):
    if nivel == 1:
        return random.choice(PedidosNivel[1])
    elif nivel == 2:
        return random.choice(PedidosNivel[2])
    elif nivel == 3:
        return random.choice(PedidosNivel[3])
    

def cambiar_escenario():
    global escenario_actual

    if nivel_actual == 1:
        escenario_actual = 1
    elif nivel_actual == 2:
        escenario_actual = 2
    elif nivel_actual == 3:
        escenario_actual = 3

pedido_actual = generar_pedido(nivel_actual)
tiempo_nivel = {
    1: 30,
    2: 30,
    3: 30
}
tiempo_juego = tiempo_nivel[nivel_actual]

tiempo_inicio = pygame.time.get_ticks()

def mostrar_inventario(chef, x, y, nivel = 1):
    limite = 5 if nivel == 3 else 4
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
mostrar_mensaje_pedido = False
tiempo_mensaje = 0
mostrar_mensaje_cambiar_nivel = False
nivel_completado = 1
tiempo_limite_pedido = timer_pedidos(nivel_actual)
tiempo_inicio_pedido = pygame.time.get_ticks()
mostrar_refri = False

def cargar_escenario():
    if escenario_actual == 1:
        cocina.x = 320
        cocina.y = 100

        freidora.x = 540
        freidora.y = 100

    elif escenario_actual == 2:
        cocina.x = 600
        cocina.y = 100

        entrega.x = 320
        entrega.y = 100

        tabla_picar.x = 100
        tabla_picar.y = 100

    elif escenario_actual == 3:
        cocina.x = 300
        cocina.y = 380

        freidora.x = 500
        freidora.y = 100

        tabla_picar.x = 300
        tabla_picar.x = 100
    for estacion in estaciones:
        estacion.rect.x = estacion.x
        estacion.rect.y = estacion.y


#------------ Ciclo principal ---------------------------------

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if estado ==  "menu":  
            screen.blit(fondo_menu, (0, 0))

            if event.type == pygame.MOUSEBUTTONDOWN:

                if boton_play.collidepoint(event.pos):
                    estado = "juego"
                    mostrar_mensaje_cambiar_nivel = False
                    tiempo_inicio = pygame.time.get_ticks()
                    nivel_actual = 1
                    puntaje = 0
                    pedidos_completados = 0
                    escenario_actual = 1
                    tiempo_juego = tiempo_nivel[1]
                    pedido_actual = generar_pedido(nivel_actual)
                    tiempo_limite_pedido = timer_pedidos(nivel_actual)
                    tiempo_inicio_pedido = pygame.time.get_ticks()
                    chef1.inventario.clear()
                    chef2.inventario.clear()
                    timer_pedidos(nivel_actual)
        
        if event.type == Pedidos:
            if estado == "juego":
                pedido_actual = generar_pedido(nivel_actual)
                tiempo_limite_pedido = timer_pedidos(nivel_actual)
                tiempo_inicio_pedido = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN:#cuando se presiona
            if mostrar_refri: 
                if event.key == pygame.K_1:
                    fresco = next((i for i in ingredientes_faltantes if i.nombre == "Gaseosa"), None)
                    if fresco:
                        chef_activo.agarrar_ingrediente(fresco, nivel_actual)
                        mostrar_refri = False
                elif event.key == pygame.K_2:
                    postre = next((i for i in ingredientes_faltantes if i.nombre == "Postre"), None)
                    if postre:
                        chef_activo.agarrar_ingrediente(postre, nivel_actual)
                    mostrar_refri = False
                continue

            if mostrar_mensaje_cambiar_nivel:
                if event.key == pygame.K_c:  # continuar al siguiente nivel
                    mostrar_mensaje_cambiar_nivel = False
                    if nivel_actual < 3:
                        nivel_actual += 1
                        tiempo_inicio = pygame.time.get_ticks()
                        tiempo_juego = tiempo_nivel[nivel_actual]
                        pedido_actual = generar_pedido(nivel_actual)
                        tiempo_limite_pedido = timer_pedidos(nivel_actual)
                        tiempo_inicio_pedido = pygame.time.get_ticks()
                        timer_pedidos(nivel_actual)
                        cambiar_escenario()
                    else: 
                        nivel_actual = 1
                        puntaje = 0
                        pedidos_completados = 0
                        escenario_actual = 1
                        tiempo_juego = tiempo_nivel[1]
                        pedido_actual = generar_pedido(1)
                        tiempo_limite_pedido = timer_pedidos(1)
                        tiempo_inicio_pedido = pygame.time.get_ticks()      
                        chef1.inventario.clear()
                        chef2.inventario.clear()
                        estado = "menu"
                elif event.key == pygame.K_q:  # Salir
                    estado = "menu"
                    mostrar_mensaje_cambiar_nivel = False
                    nivel_actual = 1
                    puntaje = 0
                    pedidos_completados = 0
                    escenario_actual = 1
                    tiempo_juego = tiempo_nivel[1]
                    pedido_actual = generar_pedido(nivel_actual)
                    tiempo_limite_pedido = timer_pedidos(nivel_actual)
                    tiempo_inicio_pedido = pygame.time.get_ticks()
                    chef1.inventario.clear()
                    chef2.inventario.clear()
                continue

            if event.key == pygame.K_TAB:#si la tecla que se presiona es TAB
                if chef_activo == chef1:#revisa el chef actual es chef1 y se cambia
                    chef_activo = chef2
                else:
                    chef_activo = chef1#Si no es chef1, entonces significa que es chef2: se cambia a chef1.
           
            if event.key == pygame.K_e: #Esta parte lo que hace es que el juego reacciona si el chef toca la letra e cerca de una estación
                for estacion in estaciones:
                    if nivel_actual in estacion.niveles:
                        if chef_activo.get_rect().colliderect(estacion.rect):
                            print(f"Estacion actual: {estacion.nombre}")

                            if estacion.nombre == "Entrega":

                                if pedido_actual.verificar(chef_activo.inventario):
                                    print(f"Necesitas: {pedido_actual.ingredientesNecesarios}")

                                if pedido_actual.verificar(chef_activo.inventario):
                                    print("Pedido actual entregado")

                                    puntaje += 100
                                    pedidos_completados += 1

                                    chef_activo.inventario.clear()
                                    pedido_actual = generar_pedido(nivel_actual)
                                    tiempo_limite_pedido = timer_pedidos(nivel_actual)
                                    tiempo_inicio_pedido = pygame.time.get_ticks()
                                
                                else:
                                    print("Pedido incorrecto")
                                    chef_activo.inventario.clear()
                                    mostrar_mensaje_pedido = True              
                                    tiempo_mensaje = 60

                            elif estacion.nombre == "Basurero":
                                if chef_activo.inventario:
                                    chef_activo.inventario.clear()
                                    print("Inventario vaciado en el basurero")
                                else:
                                    print("Inventario vacío, no hay nada que tirar")
                            elif estacion.nombre == "Cocina":
                                chef_activo.cocinar_ingredientes()

                            elif estacion.nombre == "Freidora":
                                chef_activo.freir_ingredientes()

                            elif estacion.ingrediente:
                                chef_activo.agarrar_ingrediente(estacion.ingrediente, nivel_actual)
                        
                            elif estacion.nombre == "Tabla":
                                chef_activo.picar_ingredientes()

                            elif estacion.nombre == "Refrigeradora":
                                print("Abriendo refrigeradora")
                                mostrar_refri = True


                            break

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
                    if escenario_actual == 1:
                        color = (225, 225, 225)
                    elif escenario_actual == 2:
                        color = (180, 180, 220)
                    else:
                        color = (220, 180, 180)
                else:
                    color = (40, 40, 40)
                    pygame.draw.rect(screen, color, (columna, fila, Tile_size, Tile_size))

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
        tiempo_pasado_pedido = (pygame.time.get_ticks() - tiempo_inicio_pedido) // 1000
        tiempo_restante_pedido = max(0, tiempo_limite_pedido - tiempo_pasado_pedido)
        ancho_barra = int((tiempo_restante_pedido / tiempo_limite_pedido) * 340)
        color_barra = (0, 200, 0) if tiempo_restante_pedido > 10 else (255, 0, 0)

        pygame.draw.rect(screen, color_barra, (20, 100, ancho_barra, 10))
        
        #Para los pedidos que requieren de otra acción
        for i, nombre in enumerate(pedido_actual.ingredientesNecesarios):

            for ingrediente in ingredientes_faltantes:
                if ingrediente.nombre == nombre:
                    if pedido_actual.requierePicar and nombre in ["Lechuga", "Tomate", "Cebolla"]:
                        imagen = pygame.transform.scale(ingrediente.imagen_picada, (45, 45))
                    elif pedido_actual.requiereCocinar and nombre == "Carne":
                        imagen = pygame.transform.scale(ingrediente.imagen_cocinada, (45, 45))
                    elif pedido_actual.requiereFreir and nombre == "Papas":
                        imagen = pygame.transform.scale(ingrediente.imagen_frita, (45, 45))
                    else:
                        imagen = pygame.transform.scale(ingrediente.imagen, (45, 45))

                    screen.blit(
                        imagen,
                        (
                            40+(i*50),
                            50
                        )
                    )
                    break

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
            (590,10,200,70)
        )

        screen.blit(
            texto_puntos,
            (600,25)
        )


        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (350, HEIGHT-90, 100, 80)
        )

        if not mostrar_mensaje_cambiar_nivel:
            tiempo_pasado = (pygame.time.get_ticks()-tiempo_inicio)//1000
            tiempo_restante = max(0, tiempo_juego - tiempo_pasado)

        if tiempo_restante <= 0 and not mostrar_mensaje_cambiar_nivel:
            if nivel_actual < 3:
                nivel_completado = nivel_actual
                mostrar_mensaje_cambiar_nivel = True
                pygame.time.set_timer(Pedidos, 0)
            else:
                nivel_completado = 3
                mostrar_mensaje_cambiar_nivel = True
                pygame.time.set_timer(Pedidos, 0)

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
        for estacion in estaciones:
            if nivel_actual in estacion.niveles:
                estacion.draw(screen)

        #ensenar ambor chefs dentro de cuadricula
        chef1.draw(screen)
        chef2.draw(screen)

        keys = pygame.key.get_pressed()
        chef_opuesto = chef2 if chef_activo == chef1 else chef1
        chef_activo.move(keys, chef_opuesto)
                   

        #Muestra inventarios en pantalla
        mostrar_inventario(
            chef1,
            20,
            HEIGHT-90,
            nivel_actual
        )

        mostrar_inventario(
            chef2,
            WIDTH-240,
            HEIGHT-90,
            nivel_actual
        )

        chef_rect = chef_activo.get_rect()

        for estacion in estaciones:
            if nivel_actual in estacion.niveles:
                if chef_rect.colliderect(estacion.rect):
                    texto = fuente_boton.render("E",True,(255,0,0))
                    screen.blit(texto, (estacion.x + 15, estacion.y - 40))
        # Mostrar refri 
        if mostrar_refri:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            pygame.draw.rect(screen, (50, 100, 200), (WIDTH//2 - 150, HEIGHT//2 - 80, 300, 160), border_radius=10)

            fuente = pygame.font.SysFont("Arial", 24, bold=True)
            titulo_ref = fuente.render("Refrigeradora", True, (255, 255, 255))
            screen.blit(titulo_ref, (WIDTH//2 - titulo_ref.get_width()//2, HEIGHT//2 - 65))

            texto_1 = fuente.render("1 - Gaseosa", True, (255, 255, 255))
            texto_2 = fuente.render("2 - Postre", True, (255, 255, 255))

            screen.blit(texto_1, (WIDTH//2 - texto_1.get_width()//2, HEIGHT//2 - 20))
            screen.blit(texto_2, (WIDTH//2 - texto_2.get_width()//2, HEIGHT//2 + 20))

        # Mostrar mensaje emergente cuando el pedido es incorrecto
        if mostrar_mensaje_pedido:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen,(150, 50, 50), (WIDTH//2 - 150, HEIGHT//2 - 50, 300, 100), border_radius=10)
            fuente = pygame.font.SysFont("Arial", 28, bold=True)
            texto = fuente.render("Pedido incorrecto", True, (255, 255, 255))
            screen.blit(texto, (WIDTH//2 - texto.get_width()//2, HEIGHT//2 - texto.get_height()//2))

        # El tiempo que dura en aparecer el mensaje
            tiempo_mensaje -= 1
            if tiempo_mensaje <= 0:
                mostrar_mensaje_pedido = False
        
        # Mensaje emergente para cambiar de nivel o salir del juego
        if mostrar_mensaje_cambiar_nivel:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
    
            pygame.draw.rect(screen, (50, 100, 150), (WIDTH//2 - 200, HEIGHT//2 - 100, 400, 200), border_radius=15)
    
            fuente = pygame.font.SysFont("Arial", 28, bold=True)

            if nivel_completado == 3:
                texto_nivel = fuente.render("Juego completado", True, (255, 255, 255))
                texto_opciones = fuente.render("C - Volver al menu    Q - Salir", True, (255, 255, 255))
            else:
                texto_nivel = fuente.render(f"Nivel {nivel_completado} completado", True, (255, 255, 255))
                texto_opciones = fuente.render("C - Continuar    Q - Salir", True, (255, 255, 255))
                texto_puntos = fuente.render(f"Puntos: {puntaje}", True, (255, 255, 0))

            screen.blit(texto_nivel,   (WIDTH//2 - texto_nivel.get_width()//2,   HEIGHT//2 - 70))
            screen.blit(texto_puntos,  (WIDTH//2 - texto_puntos.get_width()//2,  HEIGHT//2 - 20))
            screen.blit(texto_opciones,(WIDTH//2 - texto_opciones.get_width()//2,HEIGHT//2 + 40))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()