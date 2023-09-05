import pygame
import time

from src.object import Object
import src.ui as ui


# basically jerry
class Enemy(Object):
    def __init__(self, game, position, walk_imgs, anim_wait=0.07, name="TOM", speed=2):
        super(Enemy, self).__init__(game)

        self.position = pygame.Vector2(position)
        self.name = name

        self.imgs = walk_imgs
        self.anim_count = 0
        self.anim_wait = anim_wait

        self.speed = speed

        self.vel = [0, 0]
        self.original_y = self.position.y
        self.flipped = False

        self.last_anim_tick = time.time()
        self.base_anim_wait = self.anim_wait  # change this to change animation speed

        self.nametag_x_offset = self.imgs[0].get_width()/2  # add this to make the nametag x position centered visually

        self.target_x = self.position.x + self.camera.position.x  # note: target_x is on screen_space

    def update(self):
        world_space_target_x = self.camera.position.x + self.target_x  # self.target_x is stored in screen space, convert to world

        reached_target = abs(world_space_target_x - self.position.x) < 20

        if reached_target:
            self.position.x += self.speed
        else:
            if world_space_target_x > self.position.x:
                self.position.x += self.speed * 2
            else:
                self.position.x -= self.speed / 2

    def render(self):
        if time.time() - self.last_anim_tick > self.anim_wait:
            self.anim_count += 1
            if self.anim_count >= len(self.imgs):
                self.anim_count = 0

            self.last_anim_tick = time.time()

        self.camera.blit(pygame.transform.flip(self.imgs[self.anim_count], self.flipped, False), self.position)
        self.camera.rect((30, 30, 30), (self.position.x + self.nametag_x_offset - 40, self.position.y - 30, 80, 25))
        ui.text_world(self.game, self.name, (self.position.x+self.nametag_x_offset+2, self.position.y-24), 13, (255, 255, 255), self.game.config["font"], False, "top-center")

    def get_rect(self):
        return pygame.Rect(*self.position, *self.imgs[0].get_size())

    def get_mask(self):
        return pygame.mask.from_surface(self.imgs[self.anim_count])

    def impact_backwards(self):
        self.vel = [-6, 10]
        self.anim_count = 0

    def target_to(self, x_pos):
        self.target_x = x_pos
