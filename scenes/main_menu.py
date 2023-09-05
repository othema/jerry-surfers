from src.scene import Scene
from scenes.main_game import GameScene
import src.ui as ui
import pygame
from src.helpers import JSON


class MenuScene(Scene):
    def __init__(self, game):
        super(MenuScene, self).__init__(game)

        pygame.mixer.music.load(self.game.audio["intro"])
        pygame.mixer.music.queue(self.game.audio["music1"])
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)

        self.scores = JSON.load("json/scores.json")

    def render(self):
        x = self.game.wn_size[0] / 2
        f = self.game.config["font"]

        ui.text_screen(self.game, self.game.config["window_caption"].upper(), (x, 150), 40, color=(255, 255, 255), align="center-center", font=f)
        b_play = ui.button(self.wn, "PLAY", (x, 360), 20, width=100, align="center-center", font=f, bg_color=(255, 111, 0), bg_color_hover=(235, 91, 0))
        b_quit = ui.button(self.wn, "QUIT", (x, 400), 20, width=100, align="center-center", font=f)

        if self.game.input["mouse_was_released"]:
            if b_play:
                pygame.mixer.music.fadeout(200)
                self.game.scene_transition(GameScene)
            elif b_quit:
                self.game.exit()

        poses = [
            [(40, 40), (self.game.wn_size[0]-40, 40)],
            [(self.game.wn_size[0]-40, 40), (self.game.wn_size[0]-40, self.game.wn_size[1]-40)],
            [(self.game.wn_size[0]-40, self.game.wn_size[1]-40), (40, self.game.wn_size[1]-40)],
            [(40, self.game.wn_size[1]-40), (40, 40)]
        ]

        for pos in poses:
            # 22, 0, 132
            # 49, 60, 198

            pygame.draw.line(self.wn, (0, 126, 0), (pos[0][0], pos[0][1]+5), (pos[1][0], pos[1][1]+5), 5)
            pygame.draw.line(self.wn, (0, 170, 0), *pos, 5)

        if self.scores["previous"] is not None:
            ui.text_screen(self.game, "PREVIOUS: " + str(self.scores["previous"]),  (self.game.wn_size[0]/2, self.game.wn_size[1]-85), 15, (255, 255, 255), f, False, "top-center")
        if self.scores["highscore"] is not None:
            ui.text_screen(self.game, "HIGHSCORE: " + str(self.scores["highscore"]),  (self.game.wn_size[0]/2, self.game.wn_size[1]-65), 15, (255, 255, 255), f, False, "top-center")
