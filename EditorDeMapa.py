import pygame
import sys
import json
import os

pygame.init()

ANCHO, ALTO = 1200, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Editor de caminos")

fondo = pygame.image.load("mapaDeJuego.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# ⚙️ Datos del grafo
posiciones = {}  # {'A': (x, y)}
grafo = {}       # {'A': ['B', 'C']}
seleccionados = []  # Para seleccionar 2 nodos y unirlos
nodo_id = 0

posiciones = {}
grafo = {}
nodo_id = 0

# 🔄 Intentar cargar grafo guardado
if os.path.exists("grafo.json"):
    with open("grafo.json") as f:
        datos = json.load(f)
        posiciones = {k: tuple(v) for k, v in datos["posiciones"].items()}
        grafo = datos["grafo"]
        # nodo_id es el siguiente número más grande + 1
        if posiciones:
            nodo_id = max(int(k) for k in posiciones.keys()) + 1
        else:
            nodo_id = 0
        print(f"Grafo cargado con {len(posiciones)} nodos.")
else:
    print("No se encontró grafo.json, empezando desde cero.")
    nodo_id = 0
# 🕹️ Modo editor: click para agregar nodos o conexiones
modo_agregar_nodos = True

font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()

def dibujar():
    pantalla.blit(fondo, (0, 0))

    # Dibujar conexiones (calles)
    for nodo, vecinos in grafo.items():
        for vecino in vecinos:
            pygame.draw.line(pantalla, (120, 120, 120), posiciones[nodo], posiciones[vecino], 3)

    # Dibujar nodos (esquinas)
    for nodo, pos in posiciones.items():
        pygame.draw.circle(pantalla, (255, 0, 0), pos, 8)
        texto = font.render(nodo, True, (255, 255, 255))
        pantalla.blit(texto, (pos[0] + 10, pos[1]))

    pygame.display.flip()

running = True
while running:
    clock.tick(60)
    dibujar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                with open("grafo.json", "w") as f:
                    json.dump({"posiciones": posiciones, "grafo": grafo}, f)
                print("✅ Grafo guardado con tecla S")

        # Tecla DELETE: eliminar nodo seleccionado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                if seleccionados:
                    nodo_a_eliminar = seleccionados[-1]
                    print(f"Eliminando nodo: {nodo_a_eliminar}")

                    # 1. Eliminar de posiciones y grafo
                    posiciones.pop(nodo_a_eliminar, None)
                    grafo.pop(nodo_a_eliminar, None)

                    # 2. Eliminar conexiones desde otros nodos
                    for vecinos in grafo.values():
                        if nodo_a_eliminar in vecinos:
                            vecinos.remove(nodo_a_eliminar)

                    seleccionados.clear()

        # 🎯 Clic izquierdo para agregar nodo o seleccionar
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()

            if modo_agregar_nodos:
                nombre = str(nodo_id)  # 'A', 'B', 'C', ...
                posiciones[nombre] = (x, y)
                grafo[nombre] = []
                nodo_id += 1
            else:
                # Seleccionar nodo para conexión
                for nombre, pos in posiciones.items():
                    dist = ((x - pos[0])**2 + (y - pos[1])**2)**0.5
                    if dist < 10:
                        seleccionados.append(nombre)
                        break

                # Si hay 2 seleccionados, conectar
                if len(seleccionados) == 2:
                    a, b = seleccionados
                    if b not in grafo[a]:
                        grafo[a].append(b)
                    if a not in grafo[b]:
                        grafo[b].append(a)
                    seleccionados.clear()

        # 🔁 Clic derecho para cambiar modo
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            modo_agregar_nodos = not modo_agregar_nodos
            print("Modo agregar nodos:", modo_agregar_nodos)

# Guardar grafo como JSON (crea o actualiza)
try:
    with open("grafo.json", "w") as f:
        json.dump({
            "posiciones": {k: list(v) for k, v in posiciones.items()},
            "grafo": grafo
        }, f)
    print("✅ Grafo guardado en grafo.json")
except Exception as e:
    print("❌ Error al guardar el grafo:", e)

pygame.quit()
sys.exit()
