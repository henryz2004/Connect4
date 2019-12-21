import pygame
import pygame.gfxdraw


class GFXDisc:

    def __init__(self, color, anim):

        self.color = color
        self.anim = anim

    def draw(self, screen, r=50):

        pygame.gfxdraw.aacircle(screen, int(self.anim.pos[0]), int(self.anim.pos[1]), r, self.color)
        pygame.gfxdraw.filled_circle(screen, int(self.anim.pos[0]), int(self.anim.pos[1]), r, self.color)
