import pygame
import sys
from juego import EscenaJuego

pygame.init()

ANCHO, ALTO = 1200, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TPI - Laureano")
escena = EscenaJuego(pantalla, ANCHO, ALTO)
clock = pygame.time.Clock()
FPS = 60
running = True
pausa = False

while running:
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            running = False
    escena.manejar_eventos(eventos)
    escena.update()
    escena.draw()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
