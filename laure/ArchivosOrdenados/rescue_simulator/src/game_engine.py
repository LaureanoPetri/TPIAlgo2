import pygame
import sys
import os
import json
from typing import Dict, Any
from src.pathfinding import*
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
                "base_red_nodes": [71, 72, 73],
                "base_blue_nodes": [219, 220, 221]
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
        self.mapa.generar_vehiculos()

        # Planificar ruta inicial (primer nodo-persona)
        # Planificación inicial automática para todos los vehículos
        self.objetivos_asignados=[]
        for lista in [self.mapa.vehiculosRojos, self.mapa.vehiculosAzules]:
            for v in lista:
                objetivo = self._buscar_objetivo_disponible(v)
                if objetivo:
                    v.planificar_ruta(objetivo)
                    self.objetivos_asignados.append(objetivo)

                # Visualization
                self.vis = Visualization(self.screen, self.clock, self.FPS)
    def _buscar_objetivo_disponible(self, vehiculo):
        """Devuelve el ID del objetivo más cercano no asignado."""
        candidatos = [
            p.id for p in self.mapa.personas if p.id not in self.objetivos_asignados
        ] + [
            r.id for r in self.mapa.recursos if r.id not in self.objetivos_asignados
        ]

        if not candidatos:
            return None

        mejor_obj = None
        menor_dist = float('inf')

        for obj_id in candidatos:
            camino = find_path(vehiculo.nodo_actual, obj_id, self.mapa.nodos)
            if camino and len(camino) < menor_dist:
                mejor_obj = obj_id
                menor_dist = len(camino)

        return mejor_obj

    # -------------------------
    # LOOP PRINCIPAL
    # -------------------------
    def start(self):
        while self.running:
            # --- EVENTOS BÁSICOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # --- ACTUALIZAR LÓGICA Y MOVIMIENTOS ---
            self._update()

            # --- DIBUJAR TODO ---
            self._draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    # -------------------------
    # LÓGICA / ACTUALIZACIONES
    # -------------------------
    def _update(self):
        # --- Actualización vehículos rojos ---
        for v in self.mapa.vehiculosRojos:
            v.mover()

            # Si el vehículo llegó a destino
            if v.destino and v.nodo_actual == v.destino:
                if v.destino in self.objetivos_asignados:
                    self.objetivos_asignados.remove(v.destino)
                v.destino = None

            nodo_actual = self.mapa.nodos.get(v.nodo_actual)

            # Si hay algo que recoger (persona o recurso)
            if nodo_actual and nodo_actual.tipo in ("persona", "recurso"):
                v.recoger(nodo_actual)

                # Si recogió una persona, la quitamos del mapa
                if nodo_actual.tipo == "persona" and nodo_actual.entidad is None:
                    self.mapa.personas = [p for p in self.mapa.personas if p.id != nodo_actual.id]

                # Al recoger algo, reduce capacidad
                v.capacidad -= 1

                # Si se quedó sin capacidad, vuelve a la base
                if v.capacidad <= 0:
                    v.planificar_ruta(v.base_id)
                    continue  # salta búsqueda de nuevos objetivos hasta que descargue

            # Si todavía tiene capacidad, busca siguiente objetivo disponible
            if v.capacidad > 0 and (v.destino is None or v.destino == v.nodo_actual):
                nuevo_obj = self._buscar_objetivo_disponible(v)
                if nuevo_obj:
                    v.planificar_ruta(nuevo_obj)
                    self.objetivos_asignados.append(nuevo_obj)

        # --- Actualización vehículos azules ---
        for v in self.mapa.vehiculosAzules:
            v.mover()

            nodo_actual = self.mapa.nodos.get(v.nodo_actual)
            if nodo_actual and nodo_actual.tipo in ("persona", "recurso"):
                v.recoger(nodo_actual)

                if nodo_actual.tipo == "persona" and nodo_actual.entidad is None:
                    self.mapa.personas = [p for p in self.mapa.personas if p.id != nodo_actual.id]

                v.capacidad -= 1

                if v.capacidad <= 0:
                    v.planificar_ruta(v.base_id)
                    continue

            if v.capacidad > 0 and (v.destino is None or v.destino == v.nodo_actual):
                nuevo_obj = self._buscar_objetivo_disponible(v)
                if nuevo_obj:
                    v.planificar_ruta(nuevo_obj)
                    self.objetivos_asignados.append(nuevo_obj)

        # --- Actualizar mapa general ---
        self.mapa.actualizar_estado()

    # -------------------------
    # DIBUJADO
    # -------------------------
    def _draw(self):
        self.mapa.draw(self.screen)
        for v in self.mapa.vehiculosAzules:
            v.draw(self.screen)
        
        for v in self.mapa.vehiculosRojos:
            v.draw(self.screen)
        self.vis.draw_hud(self.mapa.vehiculosRojos)
        self.vis.draw_hud(self.mapa.vehiculosAzules)

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
