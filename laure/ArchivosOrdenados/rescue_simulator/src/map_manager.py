import pygame
import random
import json
import os
from src.aircraft import Auto, Persona  # Clases con imágenes

# =====================================================
# CLASE NODO: UNIDAD BÁSICA DEL MAPA
# =====================================================
class Nodo:
    def __init__(self, id_nodo, pos, adyacentes=None, tipo="normal"):
        self.id = id_nodo
        self.pos = tuple(pos)
        self.adyacentes = adyacentes or []
        self.tipo = tipo
        self.ocupado = False
        self.entidad = None  # Puede ser Auto, Persona, Mina, Recurso, etc.

    def ocupar(self, entidad=None):
        self.ocupado = True
        self.entidad = entidad

    def liberar(self):
        self.ocupado = False
        self.entidad = None
        if self.tipo not in ["base_roja", "base_azul"]:
            self.tipo = "normal"

    def __repr__(self):
        return f"<Nodo {self.id}: tipo={self.tipo}, ocupado={self.ocupado}>"

# =====================================================
# CLASE MAP MANAGER
# =====================================================
class MapManager:
    def __init__(self, config):
        self.config = config

        # --- Cargar grafo ---
        map_path = config.get("map_path", "grafo.json")
        with open(map_path, "r", encoding="utf-8") as f:
            data_manager = json.load(f)


        self.posiciones = data_manager["posiciones"]
        self.grafo = data_manager["grafo"]

        # Crear nodos
        self.nodos = {}
        for id_nodo_str, pos in self.posiciones.items():
            id_nodo = int(id_nodo_str)
            adyacentes = [int(a) for a in self.grafo.get(id_nodo_str, [])]
            self.nodos[id_nodo] = Nodo(id_nodo, pos, adyacentes)

        # --- Fondo ---
        ruta = r"laure\ArchivosOrdenados\rescue_simulator\ImagenesJuego\mapaDeJuego.png"
        self.fondo = pygame.image.load(ruta).convert()

        self.fondo = pygame.transform.scale(self.fondo, (1200, 800))

        # --- Listas de entidades ---
        self.minas = []
        self.recursos = []
        self.personas = []
        self.vehiculos = []

        # --- Bases ---
        self.base_roja = config["base_red_nodes"]
        self.base_azul = config["base_blue_nodes"]

        for nodo_id in self.base_roja:
            if nodo_id in self.nodos:
                self.nodos[nodo_id].tipo = "base_roja"
        for nodo_id in self.base_azul:
            if nodo_id in self.nodos:
                self.nodos[nodo_id].tipo = "base_azul"

    # =====================================================
    # GENERACIÓN ALEATORIA DE ENTIDADES
    # =====================================================
    def generar_minas(self, cantidad=10):
        libres = [n for n in self.nodos.values() if not n.ocupado and n.tipo == "normal"]
        seleccionados = random.sample(libres, cantidad)
        for nodo in seleccionados:
            nodo.tipo = "mina"
            nodo.ocupar("Mina")
            self.minas.append(nodo)
        print(f"{len(self.minas)} minas generadas.")

    def generar_recursos(self, cantidad=20):
        libres = [n for n in self.nodos.values() if not n.ocupado and n.tipo == "normal"]
        seleccionados = random.sample(libres, min(cantidad, len(libres)))
        for nodo in seleccionados:
            nodo.tipo = "recurso"
            nodo.ocupar("Recurso")
            self.recursos.append(nodo)
        print(f"{len(self.recursos)} recursos generados.")

    def generar_personas(self, cantidad=10):
        libres = [n for n in self.nodos.values() if not n.ocupado and n.tipo == "normal"]
        seleccionados = random.sample(libres, min(cantidad, len(libres)))
        for nodo in seleccionados:
            persona = Persona(nodo)
            nodo.tipo = "persona"
            nodo.ocupar(persona)
            self.personas.append(persona)
        print(f"{len(self.personas)} personas generadas.")

    # =====================================================
    # GENERAR VEHÍCULOS
    # =====================================================
    def generar_vehiculos(self, cantidad_rojo=3, cantidad_azul=3):
        # Vehículos rojos
        for i in range(cantidad_rojo):
            nodo_inicial = 73
            auto = Auto(f"AutoR{i+1}", nodo_inicial.id, self.nodos, equipo="rojo")
            nodo_inicial.ocupar(auto)
            self.vehiculos.append(auto)

        # Vehículos azules
        for i in range(cantidad_azul):
            nodo_inicial = random.choice([self.nodos[n] for n in self.base_azul])
            auto = Auto(f"AutoA{i+1}", nodo_inicial.id, self.nodos, equipo="azul")
            nodo_inicial.ocupar(auto)
            self.vehiculos.append(auto)

    # =====================================================
    # DIBUJAR MAPA
    # =====================================================
    def draw(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))

        # Nodos según tipo
        for nodo in self.nodos.values():
            if nodo.tipo == "normal":
                continue  # saltar nodos normales (invisibles)
            color = self._color_por_tipo(nodo.tipo)
            pygame.draw.circle(pantalla, color, nodo.pos, 6)

        # Dibujar personas
        for persona in self.personas:
            pantalla.blit(persona.imagen, (int(persona.pos[0]-35), int(persona.pos[1]-20)))

        # Dibujar vehículos
        for vehiculo in self.vehiculos:
            pantalla.blit(vehiculo.imagen, (int(vehiculo.pos[0]-15), int(vehiculo.pos[1]-15)))

    # =====================================================
    # COLORES DE NODOS
    # =====================================================
    def _color_por_tipo(self, tipo):
        colores = {
            "normal": (0, 0, 0),
            "mina": (128, 0, 0),
            "recurso": (0, 255, 0),
            "persona": (255, 255, 0),
            "base_roja": (255, 0, 0),
            "base_azul": (0, 0, 255)
        }
        return colores.get(tipo, (200, 200, 200))

    # =====================================================
    # ACTUALIZACIÓN DE ESTADO
    # =====================================================
    def actualizar_estado(self):
        for nodo in self.nodos.values():
            if nodo.tipo in ["mina", "recurso", "persona"] and not nodo.ocupado:
                nodo.tipo = "normal"
