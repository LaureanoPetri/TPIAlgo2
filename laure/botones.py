import pygame
from auto import*
class Boton:
    def __init__(self, x, y, ancho, alto, color_base, texto, fuente, texto_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_base = color_base
        self.color_hover = tuple(min(255, c + 30) for c in color_base)  # Color más claro al pasar el mouse
        self.color_click = tuple(max(0, c - 30) for c in color_base)    # Color más oscuro al hacer clic
        self.color_actual = color_base

        self.texto = texto
        self.fuente = fuente
        self.texto_color = texto_color
        self.texto_surface = fuente.render(texto, True, texto_color)
        self.texto_rect = self.texto_surface.get_rect(center=self.rect.center)

        self.clickeado = False

    def actualizar(self, eventos):
        mouse_pos = pygame.mouse.get_pos()
        mouse_presionado = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_presionado:
                self.color_actual = self.color_click
                self.clickeado = True
            else:
                self.color_actual = self.color_hover
        else:
            self.color_actual = self.color_base

        # Resetea el clic luego de un ciclo
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
                self.clickeado = True

    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color_actual, self.rect, border_radius=8)
        pantalla.blit(self.texto_surface, self.texto_rect)

    def esta_clickeado(self):
        if self.clickeado:
            self.clickeado = False
            return True
        return False
