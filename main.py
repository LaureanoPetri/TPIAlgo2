import pygame
import sys
# Inicializar Pygame
pygame.init()
# --- Configuración general ---
ANCHO, ALTO = 1200, 800
FPS = 60
COLOR_FONDO = (20, 20, 30)
COLOR_JUGADOR = (100, 200, 255)
VELOCIDAD = 5
# Crear ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Proyecto Pygame - Laureano")
# Controlador de FPS
clock = pygame.time.Clock()
# --- Jugador ---
jugador = pygame.Rect(100, 100, 50, 50)  # x, y, ancho, alto
# Cargar imagen de fondo
fondo = pygame.image.load("mapaDeJuego.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Escala al tamaño de la ventana

# --- Bucle principal del juego ---
running = True
while running:
    # 1️⃣ Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2️⃣ Lógica de actualización
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador.x -= VELOCIDAD
    if teclas[pygame.K_RIGHT]:
        jugador.x += VELOCIDAD
    if teclas[pygame.K_UP]:
        jugador.y -= VELOCIDAD
    if teclas[pygame.K_DOWN]:
        jugador.y += VELOCIDAD

    # 3️⃣ Renderizado
    pantalla.blit(fondo, (0, 0))  # Dibujar imagen en posición (0, 0)
    pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador)

    # 4️⃣ Actualizar pantalla
    pygame.display.flip()

    # 5️⃣ Controlar FPS
    clock.tick(FPS)

# Salir del juego
pygame.quit()
sys.exit()
