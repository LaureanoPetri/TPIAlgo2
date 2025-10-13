# src/visualization.py
import pygame
from typing import List

class Visualization:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, fps: int = 60):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.SysFont("Arial", 16)
        self.fps = fps

    def draw_hud(self, vehiculos: List):
        """Dibuja HUD minimalista: FPS y estado de vehículos."""
        # fondo semi-transparente para HUD
        surf = pygame.Surface((300, 100), pygame.SRCALPHA)
        surf.fill((20, 20, 20, 140))
        self.screen.blit(surf, (10, 10))

        # FPS
        fps_text = f"FPS: {int(self.clock.get_fps())}"
        self._draw_text(fps_text, 16, 14, 14)

        # Vehículos
        y = 36
        for v in vehiculos:
            status = f"{v.id} | nodo:{v.nodo_actual} | carga:{len(v.carga)} | estado:{v.estado}"
            self._draw_text(status, 12, 14, y)
            y += 16

    def _draw_text(self, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.SysFont("Arial", size)
        text_surf = font.render(text, True, color)
        self.screen.blit(text_surf, (x, y))
