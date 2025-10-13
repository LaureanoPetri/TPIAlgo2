import pygame
import sys
import os
import json
from typing import Dict, Any

from src.map_manager import MapManager
from src.aircraft import Auto, Moto, Jeep, Camion
from src.visualization import Visualization

class GameEngine:
    def __init__(self, config: Dict[str, Any] | None = None):
        script_dir = os.path.dirname(os.path.abspath(__file__))  # ruta de src/

        if config is None:
            # Config default
            config = {
                "screen_width": 1200,
                "screen_height": 800,
                "fps": 60,
                "map_path": os.path.join(script_dir, "grafo.json"),
                "num_minas": 10,
                "num_recursos": 20,
                "num_personas": 10,
                "base_red_nodes": ["71", "72", "73"],
                "base_blue_nodes": ["219", "220", "221"]
            }
        self.config = config

        # Inicializar Pygame
        pygame.init()
        self.ancho = config["screen_width"]
        self.alto = config["screen_height"]
        self.screen = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Simulador de Rescate - Laureano")
        self.clock = pygame.time.Clock()
        self.FPS = config.get("fps", 60)
        self.running = True

        # MapManager
        self.mapa = MapManager(config)
        self.mapa.generar_minas(config.get("num_minas", 10))
        self.mapa.generar_recursos(config.get("num_recursos", 20))
        self.mapa.generar_personas(config.get("num_personas", 10))

        # Vehículos demo
        self.vehiculos = []
        base_init = next(iter(self.mapa.base_roja), next(iter(self.mapa.nodos.keys())))
        self.vehiculos.append(Auto("auto_1", base_init, self.mapa.nodos))
        self.vehiculos.append(Moto("moto_1", base_init, self.mapa.nodos))
        self.vehiculos.append(Jeep("jeep_1", base_init, self.mapa.nodos))
        self.vehiculos.append(Camion("camion_1", base_init, self.mapa.nodos))

        # Planificar ruta inicial (primer nodo-persona)
        if self.mapa.personas:
            persona_node = self.mapa.personas[0].id
            for v in self.vehiculos:
                if isinstance(v, Auto):
                    v.planificar_ruta(persona_node)
                    break

        # Visualization
        self.vis = Visualization(self.screen, self.clock, self.FPS)

    # -------------------------
    # LOOP PRINCIPAL
    # -------------------------
    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    nodo_click = self._nodo_mas_cercano(event.pos)
                    if nodo_click:
                        for v in self.vehiculos:
                            if v.estado == "activo":
                                v.planificar_ruta(nodo_click)
                                break

            self._update()
            self._draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    # -------------------------
    # LÓGICA / ACTUALIZACIONES
    # -------------------------
    def _update(self):
        for v in self.vehiculos:
            v.mover()
            nodo_actual = self.mapa.nodos.get(v.nodo_actual)
            if nodo_actual and nodo_actual.tipo in ("persona", "recurso"):
                v.recoger(nodo_actual)
                if nodo_actual.tipo == "persona" and nodo_actual.entidad is None:
                    self.mapa.personas = [p for p in self.mapa.personas if p.id != nodo_actual.id]

        self.mapa.actualizar_estado()

    # -------------------------
    # DIBUJADO
    # -------------------------
    def _draw(self):
        self.mapa.draw(self.screen)
        for v in self.vehiculos:
            v.draw(self.screen)
        self.vis.draw_hud(self.vehiculos)

    # -------------------------
    # UTIL
    # -------------------------
    def _nodo_mas_cercano(self, pos):
        x, y = pos
        mejor = None
        mejor_dist = float("inf")
        for nodo in self.mapa.nodos.values():
            dx = nodo.pos[0] - x
            dy = nodo.pos[1] - y
            d = dx*dx + dy*dy
            if d < mejor_dist:
                mejor_dist = d
                mejor = nodo.id
        return mejor
