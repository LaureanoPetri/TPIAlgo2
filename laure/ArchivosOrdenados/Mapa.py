import pygame
import random

class Mapa:
    def __init__(self, datos):
        """
        datos: instancia de DataManager con posiciones, grafo y fondo ya cargados
        """
        datos
        self.posiciones = datos.posiciones
        self.grafo = datos.grafo
        self.personas = datos.personas

        self.recursos = []
        self.minas = []
        self.vehiculos = []

        # Bases fijas
        self.base_roja = ["71", "72", "73"]
        self.base_azul = ["220", "221", "219"]

    # =====================================================
    # DIBUJAR EL MAPA Y SUS COMPONENTES
    # =====================================================
    def mostrar_mapa(self, pantalla, fondo):
        """Dibuja el mapa, las bases, personas y vehículos."""
        
        pantalla.blit(fondo, (0, 0))

        # Bases
        for nodo in self.base_roja:
            pygame.draw.circle(pantalla, (255, 0, 0), self.posiciones[nodo], 12)
        for nodo in self.base_azul:
            pygame.draw.circle(pantalla, (0, 0, 255), self.posiciones[nodo], 12)

        # Personas
        """
        for nodo, info in self.personas.items():
            if not info["rescatada"]:
                pygame.draw.circle(pantalla, (255, 255, 0), self.posiciones[nodo], 6)

        # Vehículos
        for v in self.vehiculos:
            v.draw(pantalla)
        """
    # ==========

