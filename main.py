import pygame
import sys
import os
import json
from auto import*

# Inicializar Pygame
pygame.init()

# --- Configuración general ---
ANCHO, ALTO = 1200, 800
FPS = 60
COLOR_FONDO = (20, 20, 30)
COLOR_JUGADOR = (100, 200, 255)
VELOCIDAD = 5

# Crear ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Proyecto Pygame - Laureano")
# Controlador de FPS
clock = pygame.time.Clock()
# Cargar imagen de fondo
fondo = pygame.image.load("mapaDeJuego.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Escala al tamaño de la ventana
# 🔄 Intentar cargar grafo guardado
if os.path.exists("grafo.json"):
    with open("grafo.json") as f:
        datos = json.load(f)
        posiciones = {k: tuple(v) for k, v in datos["posiciones"].items()}
        grafo = datos["grafo"]
        nodo_id = len(posiciones)  # Para continuar desde la última letra usada
        print(f"Grafo cargado con {len(posiciones)} nodos.")
else:
    print("No se encontró grafo.json, empezando desde cero.")

base_roja = ["71", "72", "73"]
base_azul = ["220", "221", "219"]

import random
# 💡 Crear 10 personas en nodos aleatorios no repetidos
nodos_disponibles = list(posiciones.keys())
personas = {}
for nodo in random.sample(nodos_disponibles, 10):
    personas[nodo] = {"rescatada": False}
# Crear el auto DESPUÉS de generar personas
auto = Auto(nodo_inicio="73", posiciones=posiciones, grafo=grafo, personas=personas)

# --- Bucle principal del juego ---
running = True
while running:
    # 1️⃣ Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                auto.mover_por_direccion("derecha")
            elif event.key == pygame.K_LEFT:
                auto.mover_por_direccion("izquierda")
            elif event.key == pygame.K_UP:
                auto.mover_por_direccion("arriba")
            elif event.key == pygame.K_DOWN:
                auto.mover_por_direccion("abajo")
    

    auto.update()  # 2️⃣ Lógica de actualización
    # 3️⃣ Renderizado
    pantalla.blit(fondo, (0, 0))  # Dibujar imagen en posición (0, 0)
    # Dibujar bases
    for nodo in base_roja:
        pygame.draw.circle(pantalla, (255, 0, 0), posiciones[nodo], 12)  # base roja
    for nodo in base_azul:
        pygame.draw.circle(pantalla, (0, 0, 255), posiciones[nodo], 12)  # base azul
    # Mostrar personas
    for nodo, datos in personas.items():
        if not datos["rescatada"]:
            pos = posiciones[nodo]
            pygame.draw.circle(pantalla, (255, 255, 0), pos, 6)  # amarillo = persona

    auto.draw(pantalla)
    pygame.display.flip()# 4️⃣ Actualizar pantalla
    clock.tick(FPS)# 5️⃣ Controlar FPS


# Salir del juego
pygame.quit()
sys.exit()
