import pygame
import math
import os

class Auto:
    def __init__(self, nodo_inicio, posiciones, grafo, personas, imagen_path="ImagenesJuego/autoImagen.png", escala=(32, 32)):
        self.nodo_actual = nodo_inicio
        self.pos = list(posiciones[nodo_inicio])
        self.destino = None
        self.velocidad = 2
        self.posiciones = posiciones
        self.grafo = grafo
        self.personas = personas
        self.angulo = 0

        # ✅ Ruta absoluta basada en la ubicación del archivo auto.py
        ruta_completa_imagen = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", imagen_path))
        self.imagen_original = pygame.image.load(ruta_completa_imagen).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen_original, escala)
        self.rect = self.imagen.get_rect(center=self.pos)

    def mover_a(self, nuevo_nodo):
        if nuevo_nodo in self.grafo[self.nodo_actual]:
            self.destino = nuevo_nodo
            print(f"Moviendo de {self.nodo_actual} a {nuevo_nodo}")
        else:
            print(f"No hay conexión directa desde {self.nodo_actual} a {nuevo_nodo}")

    def mover_por_direccion(self, direccion):
        vecinos = self.grafo.get(self.nodo_actual, [])
        if not vecinos:
            return

        x_actual, y_actual = self.posiciones[self.nodo_actual]
        mejor_vecino = None
        mejor_diferencia = float('inf')

        TOLERANCIA_LATERAL = 30  # Cuánto puede desviarse en X o Y (según dirección)

        for vecino in vecinos:
            x, y = self.posiciones[vecino]
            dx = x - x_actual
            dy = y - y_actual

            if direccion == "derecha" and dx > 0 and abs(dy) < TOLERANCIA_LATERAL:
                diff = dx
            elif direccion == "izquierda" and dx < 0 and abs(dy) < TOLERANCIA_LATERAL:
                diff = -dx
            elif direccion == "arriba" and dy < 0 and abs(dx) < TOLERANCIA_LATERAL:
                diff = -dy
            elif direccion == "abajo" and dy > 0 and abs(dx) < TOLERANCIA_LATERAL:
                diff = dy
            else:
                continue  # No cumple con dirección + tolerancia

            if diff < mejor_diferencia:
                mejor_diferencia = diff
                mejor_vecino = vecino

        if mejor_vecino:
            self.mover_a(mejor_vecino)

    def update(self):
        if self.destino:
            objetivo = self.posiciones[self.destino]
            dx = objetivo[0] - self.pos[0]
            dy = objetivo[1] - self.pos[1]
            distancia = math.hypot(dx, dy)

            if distancia > 0:
                # atan2 usa (y, x), Pygame tiene y hacia abajo, por eso invertimos dy
                angulo_radianes = math.atan2(-dy, dx)
                angulo_grados = math.degrees(angulo_radianes)
                # Ajustamos porque la imagen apunta hacia arriba, no a la derecha
                self.angulo = angulo_grados - 90  

            if self.nodo_actual in self.personas and not self.personas[self.nodo_actual]["rescatada"]:
                print(f"🚨 Persona rescatada en nodo {self.nodo_actual}")
                self.personas[self.nodo_actual]["rescatada"] = True

            if distancia < self.velocidad:
                self.pos = list(objetivo)
                self.nodo_actual = self.destino
                self.destino = None
            else:
                self.pos[0] += self.velocidad * dx / distancia
                self.pos[1] += self.velocidad * dy / distancia

        self.rect.center = (int(self.pos[0]), int(self.pos[1]))

    def draw(self, pantalla):
        imagen_rotada = pygame.transform.rotate(self.imagen, self.angulo)
        rect_rotado = imagen_rotada.get_rect(center=self.rect.center)
        pantalla.blit(imagen_rotada, rect_rotado)

        for nodo, datos in self.personas.items():
            if not datos["rescatada"]:
                pos = self.posiciones[nodo]
                pygame.draw.circle(pantalla, (255, 255, 0), pos, 6)
