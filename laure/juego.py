# escena_juego.py
import pygame
import json
import os
import random
from auto import Auto
from botones import Boton

class EscenaJuego:
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.fondo = pygame.image.load("ImagenesJuego/mapaDeJuego.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ancho, alto))

        # Cargar grafo
        if os.path.exists("laure/grafo.json"):
            with open("laure/grafo.json") as f:
                datos = json.load(f)
                self.posiciones = {k: tuple(v) for k, v in datos["posiciones"].items()}
                self.grafo = datos["grafo"]
                print(f"Grafo cargado con {len(self.posiciones)} nodos.")
        else:
            print("No se encontró grafo.json, empezando desde cero.")
            self.posiciones = {}
            self.grafo = {}

        self.base_roja = ["71", "72", "73"]
        self.base_azul = ["220", "221", "219"]
        self.personas = {}
        self.crear_personas()
        self.auto = Auto("73", self.posiciones, self.grafo, self.personas)

        self.fuente = pygame.font.SysFont("Arial", 24)
        self.boton_pausa = Boton(615, alto - 47, 120, 40, (220, 20, 60), "Pausa", self.fuente)
        self.boton_guardar = Boton(740, alto - 47, 160, 40, (34, 139, 34), "Guardar", self.fuente)

        self.pausa = False

    def crear_personas(self):
        nodos = list(self.posiciones.keys())
        for nodo in random.sample(nodos, 10):
            self.personas[nodo] = {"rescatada": False}

    def manejar_eventos(self, eventos):
        self.boton_pausa.actualizar(eventos)
        self.boton_guardar.actualizar(eventos)

        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_pausa.rect.collidepoint(event.pos):
                    self.pausa = not self.pausa
                    print("Pausa activada:", self.pausa)
                elif self.boton_guardar.rect.collidepoint(event.pos):
                    self.guardar_partida()

            if not self.pausa:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.auto.mover_por_direccion("derecha")
                    elif event.key == pygame.K_LEFT:
                        self.auto.mover_por_direccion("izquierda")
                    elif event.key == pygame.K_UP:
                        self.auto.mover_por_direccion("arriba")
                    elif event.key == pygame.K_DOWN:
                        self.auto.mover_por_direccion("abajo")

    def update(self):
        if not self.pausa:
            self.auto.update()
  

    def draw(self):
        self.pantalla.blit(self.fondo, (0, 0))

        # Bases
        for nodo in self.base_roja:
            pygame.draw.circle(self.pantalla, (255, 0, 0), self.posiciones[nodo], 12)
        for nodo in self.base_azul:
            pygame.draw.circle(self.pantalla, (0, 0, 255), self.posiciones[nodo], 12)

        # Personas
        for nodo, datos in self.personas.items():
            if not datos["rescatada"]:
                pygame.draw.circle(self.pantalla, (255, 255, 0), self.posiciones[nodo], 6)

        # Botones
        self.boton_pausa.draw(self.pantalla)
        self.boton_guardar.draw(self.pantalla)

        # Auto
        self.auto.draw(self.pantalla)

    def guardar_partida(self):
        data = {
            "personas": self.personas,
            "auto": {
                "nodo_actual": self.auto.nodo_actual,
                "pos": self.auto.pos
            }
        }
        with open("laure/partida_guardada.json", "w") as f:
            json.dump(data, f, indent=4)
        print("💾 Partida guardada.")
