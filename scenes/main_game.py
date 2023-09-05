import pygame
import time
from random import randint

import scenes.main_menu as main_menu
from src.scene import Scene
from src.player import Player
from src.enemy import Enemy
import src.tilemap as tilemap
import src.ui as ui
from src.obstacle import Obstacle
from src.helpers import JSON
from src.coin import Coin


def random_obstacle(game, imgs, speed):
    rand = randint(1, 4)  # i dont want a rolling spike so i'm not including it in the random gen
    x, y = randint(game.wn_size[0] + game.camera.position.x + 50, game.wn_size[0] + game.camera.position.x + 300), 482

    if rand == 4:
        new = Obstacle(game, imgs[0][rand], (x, y), speed, rot_speed=speed+3)
    else:
        old_height = imgs[0][rand].get_height()
        size_up = randint(8, 12) / 10
        new_height = old_height * size_up
        y += old_height - new_height
        new = Obstacle(game, imgs[0][rand], (x, y), speed, rot_speed=speed+3, size_up=size_up)

    return new


class GameScene(Scene):
    def __init__(self, game):
        super(GameScene, self).__init__(game)

        self.floor_speed = 2      # increasing floor speed makes it move faster
        self.player_speed = 0.07  # decreasing player speed makes it move faster

        self.jerry_walk = tilemap.parse(pygame.image.load(game.config["jerry_walk_img"]), (16, 22), (48, 66))
        self.jerry_jump = tilemap.parse(pygame.image.load(game.config["jerry_jump_img"]), (16, 24), (48, 72))
        self.tom_walk = tilemap.parse(pygame.image.load(game.config["tom_walk_img"]), (32, 39), (96, 117))
        self.obstacles = tilemap.parse(pygame.image.load(game.config["obstacle_img"]), (16, 16), (48, 48))
        self.coin = self.obstacles[0][5]

        self.player = Player(self.game, (450, 464), self.jerry_walk[0][:7], self.jerry_jump[0], [0, 4], 0.07)
        self.enemy = Enemy(self.game, (150, 413), self.tom_walk[0], speed=2)

        self.enemy.target_to(-100)
        self.enemy_go_back = False
        self.last_enemy_targeted = time.time()

        self.all_obstacles = []
        self.all_coins = []
        self.last_spawned_obstacle = time.time() + 2  # +2 means that you have to wait 2 seconds before object spawning
        self.obstacle_wait = randint(5, 20) / 10

        self.floor_offset = 0

        self.lose_sound = pygame.mixer.Sound(self.game.audio["lose"])

        self.scores = JSON.load("json/scores.json")

        pygame.mixer.music.load(self.game.audio["music2"])
        pygame.mixer.music.play(-1)

        self.background_stripe = pygame.Surface((80, self.game.wn_size[1]))
        pygame.draw.rect(self.background_stripe, (10, 10, 10), (0, 0, 30, self.background_stripe.get_height()))
        pygame.draw.rect(self.background_stripe, (20, 20, 20), (30, 0, 50, self.background_stripe.get_height()))

        self.ground_stripe = pygame.Surface((10, 13))
        pygame.draw.rect(self.ground_stripe, (0, 126, 0), (0, 0, 5, 13))
        pygame.draw.rect(self.ground_stripe, (0, 170, 0), (5, 0, 5, 13))

        self.coin_sound = pygame.mixer.Sound(self.game.audio["coin"])
        self.coin_points = 0

    def update(self):
        self.player.update()
        self.enemy.update()

        if self.player.check_enemy_collision(self.enemy):
            self.lose_sound.play()

            score = int(self.camera.position.x / 100) + self.coin_points
            if self.scores["highscore"] is None:
                self.scores["highscore"] = score
            else:
                self.scores["highscore"] = max(score, self.scores["highscore"])
            self.scores["previous"] = score
            JSON.write(self.scores, "json/scores.json")
            self.game.scene_transition(main_menu.MenuScene)

        player_mask = self.player.get_mask()

        to_remove = []
        for coin in self.all_coins:
            coin.update()

            if coin.check_collision(player_mask, self.player.get_rect()) and coin.state == "normal":
                self.coin_sound.play()
                self.coin_points += 20
                coin.fade_upwards()
                break

            if coin.delete:
                to_remove.append(coin)

        for coin in to_remove:
            self.all_coins.remove(coin)

        to_remove = []
        for obstacle in self.all_obstacles:
            obstacle.update()

            if obstacle.state == "normal":
                if obstacle.check_collision(player_mask, self.player.get_rect()):
                    obstacle.fall_down()
                    self.player.impact_backwards()
                    self.enemy.target_to(self.enemy.target_x + 200)
                    self.enemy_go_back = True
                    self.last_enemy_targeted = time.time()

                if obstacle.check_collision(self.enemy.get_mask(), self.enemy.get_rect()):
                    obstacle.fall_down()

            for other_obstacle in self.all_obstacles:
                if other_obstacle is obstacle:
                    continue

                if obstacle.check_collision(other_obstacle.mask, other_obstacle.get_rect()):
                    obstacle.fall_down()
                    break

            if obstacle.delete:
                to_remove.append(obstacle)

        for obstacle in to_remove:
            self.all_obstacles.remove(obstacle)

        if time.time() - self.last_spawned_obstacle > self.obstacle_wait:
            if randint(0, 10) == 1:  # 1 in x chance:
                # coin
                self.all_coins.append(Coin(self.game, (self.game.wn_size[0] + 200 + self.camera.position.x, 482), self.coin))
            else:
                # obstacle
                self.all_obstacles.append(random_obstacle(self.game, self.obstacles, randint(1, 4)))
            self.last_spawned_obstacle = time.time()
            self.obstacle_wait = randint(2, 20) / 10

        if time.time() - self.last_enemy_targeted > 3 and self.enemy_go_back:
            self.enemy.target_to(-100)
            self.enemy_go_back = False

    def render(self):
        self.wn.fill((0, 0, 0))

        cam_x = self.camera.position[0]

        for x in range(0, self.game.wn_size[0], 100):
            x_ = cam_x + ((x + self.floor_offset*0.1) % self.game.wn_size[0]-80)
            y_ = self.camera.position.y
            self.camera.blit(self.background_stripe, (x_, y_))

        y = 543
        for x in range(5, self.game.wn_size[0]-5, 30):
            x_ = cam_x + ((x+self.floor_offset) % self.game.wn_size[0])
            self.camera.blit(self.ground_stripe, (x_, y))

        self.camera.line((0, 170, 0), (cam_x, 532), (cam_x+self.game.wn_size[0], 532), 5)
        self.camera.line((0, 126, 0), (cam_x, 537), (cam_x+self.game.wn_size[0], 537), 5)
        self.camera.line((0, 126, 0), (cam_x, 560), (cam_x+self.game.wn_size[0], 560), 5)

        self.floor_offset -= self.floor_speed

        self.player.render()
        self.enemy.render()

        for obstacle in self.all_obstacles:
            obstacle.render()

        for coin in self.all_coins:
            coin.render()

        self.camera.position = pygame.Vector2(-self.floor_offset, self.player.position.y * 0.2)
        pygame.draw.rect(self.wn, (0, 0, 0), (0, 0, *self.game.wn_size), 60)

        # all ui elements go here (above the border)

        ui.text_screen(self.game, "SCORE: " + str(int(self.camera.position.x / 100) + self.coin_points), (self.game.wn_size[0]/2, 30), 20, (255, 255, 255), self.game.config["font"], False, "top-center")

        if self.scores["highscore"] is not None:
            ui.text_screen(self.game, "HIGHSCORE: " + str(self.scores["highscore"]), (self.game.wn_size[0]/2, 60), 10, (255, 255, 255), self.game.config["font"], False, "top-center")
