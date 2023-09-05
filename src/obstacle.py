from src.object import Object
import pygame


class Obstacle(Object):
    def __init__(self, game, surf, position, x_speed=1, rot_speed=4, size_up=1):
        super(Obstacle, self).__init__(game)

        self.position = pygame.Vector2(position)
        self.surface = pygame.transform.scale(surf, (surf.get_width() * size_up, surf.get_height() * size_up))
        self.x_speed = x_speed
        self.rot_speed = rot_speed

        self.rotation = 0

        self.mask = pygame.mask.from_surface(self.surface)  # allows for pixel perfect collision

        self.state = "normal"
        self.yv = 0
        self.delete = False

    # the animation where the obstacle will fly up and fall off the screen
    def fall_down(self, force=5):
        if self.state == "fall":
            return
        self.state = "fall"
        self.yv = force

    def update(self):
        if self.state == "normal":
            # move and rotate towards the player
            self.position.x -= self.x_speed
            self.rotation += self.rot_speed
        elif self.state == "fall":
            self.yv -= 0.2  # acts as gravity
            self.position.y -= self.yv
            self.rotation -= 5

        # if off the screen, allow obstacle for deletion to save memory and boost fps
        screen_pos = self.position - self.camera.position
        if screen_pos.x < -self.get_rect().w or screen_pos.y > self.game.wn_size[1]:
            self.delete = True

    def get_rect(self):
        return pygame.Rect(*self.position, *self.surface.get_size())

    def check_collision(self, mask_other, rect_other):
        rect_my = self.get_rect()

        if not rect_my.colliderect(rect_other):
            return False

        offset_x = rect_other.x - rect_my.x
        offset_y = rect_other.y - rect_my.y
        overlap = self.mask.overlap(mask_other, (offset_x, offset_y))

        return overlap

    def render(self):
        # pygame rotates from top right, this makes the rotation appear centered
        rotated = pygame.transform.rotate(self.surface, self.rotation)
        new_pos = (self.position.x + self.surface.get_width()/2 - rotated.get_width()/2,
                   self.position.y + self.surface.get_height()/2 - rotated.get_height()/2)
        self.camera.blit(rotated, new_pos)
