import math

import pygame
import time

from src.object import Object
import src.ui as ui


class Player(Object):
    def __init__(self, game, position, walk_imgs, jump_imgs, step_frames=(), anim_wait=0.07, name="MERAJ"):
        super(Player, self).__init__(game)

        self.position = pygame.Vector2(position)
        self.img_walk = walk_imgs
        self.img_jump = jump_imgs
        self.name = name

        self.state = "walk"
        self.imgs = self.img_walk
        self.anim_count = 0
        self.anim_wait = anim_wait

        self.vel = [0, 0]
        self.original_y = self.position.y
        self.flipped = False

        self.last_anim_tick = time.time()
        self.base_anim_wait = self.anim_wait  # change this to change animation speed

        self.nametag_x_offset = self.img_walk[0].get_width()/2  # add this to make the nametag x position centered visually
        self.step_frames = step_frames  # the frames of the walk cycle where a footstep sound is played

        # sounds
        self.sound_jump = pygame.mixer.Sound(self.game.audio["jump"])
        self.sound_land = pygame.mixer.Sound(self.game.audio["land"])
        self.sound_walk = pygame.mixer.Sound(self.game.audio["walk"])
        self.sound_knock = pygame.mixer.Sound(self.game.audio["knock"])

        # volumes
        self.sound_walk.set_volume(0.5)

    def update(self):
        keys = pygame.key.get_pressed()
        self.anim_wait = math.inf  # if not moving, dont cycle the animation
        self.flipped = False

        moving = False

        # main movement (left speed, right speed)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.position.x += 3
            self.anim_wait = self.base_anim_wait * 0.8
            moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.position.x -= 3
            self.anim_wait = self.base_anim_wait * 0.8
            self.flipped = True
            moving = True

        if self.position.x > self.game.wn_size[0] - self.get_rect().w + self.camera.position.x:
            self.position.x = self.game.wn_size[0] - self.get_rect().w + self.camera.position.x

        if self.state == "jump":
            self.anim_wait = 0.1  # slow the animation speed down on a jump

        # if up keys are pressed, jump
        if self.state == "walk" and (keys[pygame.K_w] or keys[pygame.K_UP]):
            self.state = "jump"
            self.anim_count = 0  # so jump frames start from 0
            self.vel = [2 if moving else 1, 10]  # boost forward
            self.position.y = self.original_y  # reset y coordinate
            self.sound_jump.play()

    def render(self):
        if self.state == "walk":
            self.imgs = self.img_walk
        elif self.state == "jump":
            self.imgs = self.img_jump

        # wait self.anim_wait seconds before changing animation frame
        if time.time() - self.last_anim_tick > self.anim_wait:
            self.anim_count += 1
            if self.anim_count >= len(self.imgs):
                self.anim_count = 0

            # footstep noise - if the animation frame index is inside the step_frames list, play it
            if self.state == "walk" and self.anim_count in self.step_frames:
                self.sound_walk.play()

            self.last_anim_tick = time.time()


        if self.anim_wait == math.inf:
            self.anim_count = -1

        if self.state == "jump":
            self.position.y -= self.vel[1]
            if self.flipped: self.position.x -= self.vel[0]
            else: self.position.x += self.vel[0]
            self.vel[1] -= 0.5

        if self.position.y > self.original_y:
            self.position.y = self.original_y
            self.state = "walk"
            self.sound_land.play()

        self.camera.blit(pygame.transform.flip(self.imgs[self.anim_count], self.flipped, False), self.position)

        # nametag
        self.camera.rect((30, 30, 30), (self.position.x + self.nametag_x_offset - 40, self.position.y - 30, 80, 25))
        ui.text_world(self.game, self.name, (self.position.x+self.nametag_x_offset+2, self.position.y-24), 13, (255, 255, 255), self.game.config["font"], False, "top-center")

    def get_rect(self):
        return pygame.Rect(*self.position, *self.imgs[0].get_size())

    def get_mask(self):
        return pygame.mask.from_surface(self.imgs[self.anim_count])

    def impact_backwards(self):
        self.state = "jump"
        self.vel = [-6, 10]
        self.anim_count = 0
        self.sound_knock.play()

    def check_enemy_collision(self, enemy):
        rect_my = self.get_rect()
        rect_other = enemy.get_rect()

        if not rect_my.colliderect(rect_other):
            return False

        offset_x = rect_other.x - rect_my.x
        offset_y = rect_other.y - rect_my.y
        overlap = self.get_mask().overlap(enemy.get_mask(), (offset_x, offset_y))
        return overlap
