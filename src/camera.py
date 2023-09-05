import pygame

from src.object import Object


# only one camera, created by Game() instance
class Camera(Object):
    def __init__(self, game, position=(0, 0)):
        super(Camera, self).__init__(game)

        self.position = pygame.Vector2(position)

        self.size = game.wn_size
        self.surf = pygame.Surface(self.size)

    def render(self):
        self.game.wn.fill((0, 0, 0))
        self.game.wn.blit(self.surf, (0, 0))

    # given a world space coordinate, convert it to a screen space coordinate
    def _adjust(self, position):
        return position[0] - self.position[0], position[1] - self.position[1]

    def blit(self, surf, position):
        adjust = self._adjust(position)
        self.game.wn.blit(surf, adjust)

    # return whether a rect is currently visible on screen
    def in_canvas(self, rect):
        pos = rect.x, rect.y
        dim = rect.w, rect.h
        return self.position.x < pos[0] + dim[0] < self.position.x + self.size[0] + dim[0]\
               and self.position.y < pos[1] + dim[1] < self.position.y + self.size[1] + dim[1]

    # draw a rect to the screen
    def rect(self, color, rect, border_radius=0):
        rect = pygame.Rect(rect)

        adjust = self._adjust((rect.x, rect.y))
        new_rect = pygame.Rect(*adjust, rect.w, rect.h)
        pygame.draw.rect(self.game.wn, color, new_rect, border_radius=border_radius)

    # draw a line to the screen
    def line(self, color, start, end, thickness=1):
        adjust_start = self._adjust(start)  # first point, adjusted (converted to screen space)
        adjust_end = self._adjust(end)  # second point, adjusted
        pygame.draw.line(self.game.wn, color, adjust_start, adjust_end, thickness)
