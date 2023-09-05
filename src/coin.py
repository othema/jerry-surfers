from src.object import Object
import pygame


# very similar to Obstacle
class Coin(Object):
    def __init__(self, game, position, surf):

        super(Coin, self).__init__(game)

        self.position = pygame.Vector2(position)
        self.surf = surf

        self.mask = pygame.mask.from_surface(self.surf)

        self.state = "normal"
        self.delete = False
        self.alpha = 255

    def render(self):
        if self.state == "fade":
            self.alpha -= 5
            self.position.y -= 1
            self.surf.set_alpha(self.alpha)

            if self.alpha <= 0:
                self.delete = True

        self.camera.blit(self.surf, self.position)

    def check_collision(self, mask_other, rect_other):
        rect_my = self.get_rect()

        if not rect_my.colliderect(rect_other):
            return False

        offset_x = rect_other.x - rect_my.x
        offset_y = rect_other.y - rect_my.y
        overlap = self.mask.overlap(mask_other, (offset_x, offset_y))

        return overlap

    def get_rect(self):
        return pygame.Rect(*self.position, *self.surf.get_size())

    def get_mask(self):
        return self.mask

    def fade_upwards(self):
        self.state = "fade"
