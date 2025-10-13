# src/aircraft.py
import pygame
from src.pathfinding import find_path
import os

# =====================================================
# CLASE BASE: VEHICULO
# =====================================================
class Vehiculo:
    def __init__(self, id_vehiculo, nodo_inicial, nodos, color, capacidad, viajes_max, equipo="rojo"):
        self.id = id_vehiculo
        self.nodos = nodos
        self.nodo_actual = nodo_inicial
        self.pos = list(self.nodos[self.nodo_actual].pos)

        self.color = color
        self.capacidad = capacidad
        self.viajes_restantes = viajes_max
        self.carga = []
        self.estado = "activo"
        self.camino = []
        self.destino = None
        self.velocidad = 2
        self.equipo = equipo
        self.imagen = None  # se asigna en la clase hija

        # Ocupa su nodo inicial
        self.nodos[self.nodo_actual].ocupar(self)

    # =====================================================
    # LÓGICA DE MOVIMIENTO
    # =====================================================
    def planificar_ruta(self, destino_id):
        self.camino = find_path(self.nodo_actual, destino_id, self.nodos)
        if self.camino:
            self.destino = destino_id
            print(f"{self.id} -> ruta planificada: {self.camino}")
        else:
            print(f"{self.id}: No se encontró ruta a {destino_id}")

    def mover(self):
        if not self.camino or self.estado != "activo":
            return

        siguiente_nodo_id = self.camino[0]
        siguiente_nodo = self.nodos[siguiente_nodo_id]

        if siguiente_nodo.ocupado:
            print(f"{self.id}: Nodo {siguiente_nodo_id} ocupado, recalculando ruta...")
            self.planificar_ruta(self.destino)
            return

        dx = siguiente_nodo.pos[0] - self.pos[0]
        dy = siguiente_nodo.pos[1] - self.pos[1]
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia < self.velocidad:
            self.nodos[self.nodo_actual].liberar()
            self.nodo_actual = siguiente_nodo_id
            self.nodos[self.nodo_actual].ocupar(self)
            self.pos = list(self.nodos[self.nodo_actual].pos)
            self.camino.pop(0)
        else:
            self.pos[0] += self.velocidad * dx / distancia
            self.pos[1] += self.velocidad * dy / distancia

    def draw(self, pantalla):
        if self.imagen:
            pantalla.blit(self.imagen, (int(self.pos[0]-15), int(self.pos[1]-15)))
        else:
            pygame.draw.circle(pantalla, self.color, (int(self.pos[0]), int(self.pos[1])), 10)

    def recoger(self, nodo):
        if len(self.carga) >= self.capacidad:
            print(f"{self.id} está lleno.")
            return
        if nodo.tipo in ["recurso", "persona"]:
            self.carga.append(nodo.tipo)
            nodo.liberar()
            print(f"{self.id} recogió {nodo.tipo} en {nodo.id}")

    def destruir(self):
        self.estado = "destruido"
        self.nodos[self.nodo_actual].liberar()
        print(f"{self.id} fue destruido.")


# =====================================================
# CLASES ESPECÍFICAS DE VEHÍCULOS
# =====================================================
class Auto(Vehiculo):
    def __init__(self, id_vehiculo, nodo_inicial, nodos, equipo="rojo"):
        color = (255, 0, 0) if equipo == "rojo" else (0, 0, 255)
        super().__init__(id_vehiculo, nodo_inicial, nodos, color, capacidad=2, viajes_max=1, equipo=equipo)

        # Cargar imagen relativa al archivo aircraft.py
        imagen_path="ImagenesJuego/autoRojo.png"
        ruta_completa_imagen = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", imagen_path))
        imagen_original = pygame.image.load(ruta_completa_imagen).convert_alpha()
        self.imagen = pygame.transform.scale(imagen_original, (32, 32))



class Moto(Vehiculo):
    def __init__(self, id_vehiculo, nodo_inicial, nodos, equipo="rojo"):
        super().__init__(id_vehiculo, nodo_inicial, nodos, color=(255, 150, 0),
                         capacidad=1, viajes_max=1, equipo=equipo)
        # Opcional: cargar imagen de moto si tenés


class Jeep(Vehiculo):
    def __init__(self, id_vehiculo, nodo_inicial, nodos, equipo="rojo"):
        super().__init__(id_vehiculo, nodo_inicial, nodos, color=(0, 255, 0),
                         capacidad=3, viajes_max=2, equipo=equipo)
        # Opcional: cargar imagen de jeep si tenés


class Camion(Vehiculo):
    def __init__(self, id_vehiculo, nodo_inicial, nodos, equipo="rojo"):
        super().__init__(id_vehiculo, nodo_inicial, nodos, color=(255, 255, 255),
                         capacidad=5, viajes_max=3, equipo=equipo)
        # Opcional: cargar imagen de camión si tenés


# =====================================================
# CLASE PERSONA
# =====================================================
class Persona:
    _contador = 0  # contador de personas para generar IDs únicos
    
    def __init__(self, nodo):
        self.id = f"persona_{Persona._contador}"
        Persona._contador += 1
        
        self.nodo = nodo
        self.pos = list(nodo.pos)
        
        ruta_base = os.path.dirname(os.path.dirname(__file__))  # esto te lleva a rescue_simulator/
        ruta_imagen = os.path.join(ruta_base, "ImagenesJuego", "persona.png")        
        self.imagen = pygame.image.load(ruta_imagen).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (70, 40))
        # Sube un nivel al directorio raíz del proyecto


