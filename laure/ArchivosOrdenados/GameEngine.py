import pygame
import sys
from Mapa import Mapa
from data_manager import DataManager
# from jugador import Jugador  # cuando los tengas

class GameEngine:
    def __init__(self):
        pygame.init()
        self.ancho = 1200
        self.alto = 800
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # --- Datos del mapa y entidades
        self.data = DataManager()
        self.data.cargar_grafo()
        #self.data.generar_personas()

        self.mapa = Mapa(self.data)
        self.running = True

    def start(self):
        pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Simulador de Rescate - Laureano")
        fondo =  pygame.image.load("ImagenesJuego/mapaDeJuego.png").convert()
        fondo = pygame.transform.scale(fondo, (self.ancho, self.alto))

        while self.running:
            for event in pygame.event.get():# Eventos
                if event.type == pygame.QUIT:
                    self.running = False

            # Renderizar
            self.mapa.mostrar_mapa(pantalla, fondo)

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()



    def actualizar_estado(self):
        for jugador in self.jugadores:
            for vehiculo in jugador.vehiculos:
                if vehiculo.esta_operativo():
                    vehiculo.mover(vehiculo.estrategia.decidir_movimiento(vehiculo, self.mapa))
                    vehiculo.detectar_recursos(self.mapa)

    def fin_de_simulacion(self):
        # Termina si todos los vehículos están destruidos o sin viajes restantes
        return all(not v.esta_operativo() for j in self.jugadores for v in j.vehiculos)
