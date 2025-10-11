import json
import os
import random
import pygame
"""Clase encargada de la carga, guardado y gestión de datos del juego."""
class DataManager:
    def __init__(self, ruta_base="laure"):
        self.ruta_base = ruta_base
        self.path_grafo = os.path.join(ruta_base, "grafo.json")
        self.path_partidas = os.path.join(ruta_base, "partidasGuardadas")

        self.posiciones = {}
        self.grafo = {}
        self.personas = {}

        # Crear carpetas si no existen
        os.makedirs(self.ruta_base, exist_ok=True)
        os.makedirs(self.path_partidas, exist_ok=True)

    # ========================
    # CARGA DE MAPA / GRAFO
    # ========================
    def cargar_grafo(self) -> None:
        """Carga el grafo y las posiciones desde el archivo JSON."""
        if os.path.exists(self.path_grafo):
            with open(self.path_grafo, "r") as f:
                datos = json.load(f)
                self.posiciones = {k: tuple(v) for k, v in datos["posiciones"].items()}
                self.grafo = datos["grafo"]
            print(f" Grafo cargado con {len(self.posiciones)} nodos.")
        else:
            print(" No se encontró grafo.json. Iniciando sin mapa.")
            self.posiciones, self.grafo = {}, {}

    # ========================
    # GESTIÓN DE PERSONAS
    # ========================
    def generar_personas(self, cantidad: int = 10) -> dict:
        """Genera una cantidad de personas en nodos aleatorios del mapa."""
        if not self.posiciones:
            print("No hay posiciones cargadas para generar personas.")
            return {}

        nodos = list(self.posiciones.keys())
        self.personas = {n: {"rescatada": False} for n in random.sample(nodos, cantidad)}
        print(f"👥 {cantidad} personas generadas.")
        return self.personas

    # ========================
    # GUARDAR / CARGAR PARTIDAS
    # ========================
    def guardar_partida(self, datos: dict, nombre: str) -> None:
        """Guarda una partida en formato JSON."""
        ruta = os.path.join(self.path_partidas, f"{nombre}.json")
        with open(ruta, "w") as f:
            json.dump(datos, f, indent=4)
        print(f"Partida guardada en: {ruta}")

    def abrir_partida(self, nombre: str) -> dict | None:
        """Abre una partida guardada y devuelve su contenido."""
        ruta = os.path.join(self.path_partidas, f"{nombre}.json")
        if os.path.exists(ruta):
            with open(ruta, "r") as f:
                datos = json.load(f)
            print(f"Partida '{nombre}' cargada.")
            return datos
        else:
            print(f"No existe la partida '{nombre}'.")
            return None

    def listar_partidas(self) -> list[str]:
        """Lista todas las partidas disponibles."""
        partidas = [
            os.path.splitext(f)[0]
            for f in os.listdir(self.path_partidas)
            if f.endswith(".json")
        ]
        if not partidas:
            print("No hay partidas guardadas aún.")
        else:
            print("Partidas disponibles:")
            for i, nombre in enumerate(partidas, start=1):
                print(f"  {i}. {nombre}")
        return partidas
