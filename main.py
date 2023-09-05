import pygame  # import pygame module
import sys  # import sys module for exiting the game

from src.helpers import JSON  # go to the src/ folder and import class JSON from helpers.py
from src.camera import Camera
import src.ui as ui

# scenes
from scenes.main_menu import MenuScene


# main controller game and game loop
class Game:
    def __init__(self, scene=None):
        pygame.init()

        self.config = JSON.load("json/config.json")
        self.audio = JSON.load("json/audio.json")

        self.wn_size = self.config["window_size"]
        self.fps = self.config["fps"]

        self.wn = pygame.display.set_mode(self.wn_size)
        pygame.display.set_caption(self.config["window_caption"])

        self.camera = None  # Object.camera is assigned to Game.camera - but Game.camera doesn't exist yet
        self.camera = Camera(self)

        self.events = []
        self.clock = pygame.time.Clock()

        if scene is None:
            self.scene = None
        else:
            self.scene = scene(self)

        self.delta_time = 0
        self.debug = False

        # can be accessed from any object to determine when a click has been initiated and released
        self.input = {
            "mouse_was_released": False,
            "mouse_was_pressed": False
        }

        self._was_mouse = False

    # main game loop (event registering, update, render)
    def run(self):
        while True:
            self.delta_time = self.clock.tick(self.fps) / 1000

            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    self.debug = not self.debug

            self.update()
            self.render()

            pygame.display.update()

    def update(self):
        if self.scene is None: return
        self.scene.update()

        mouse = pygame.mouse.get_pressed(3)[0]  # left mouse
        self.input["mouse_was_pressed"] = mouse and not self._was_mouse
        self.input["mouse_was_released"] = not mouse and self._was_mouse
        self._was_mouse = mouse

    def render(self):
        self.wn.fill((0, 0, 0))
        if self.scene is None: return
        self.scene.render()

        if self.debug:
            ui.text_screen(self, "FPS: " + str(round(self.clock.get_fps())), (10, 10), 20, (255, 255, 255))
            ui.text_screen(self, "DELTA: " + str(round(self.clock.get_time())) + "ms", (10, 25), 20, (255, 255, 255))
            ui.text_screen(self, "SCENE: " + type(self.scene).__name__, (10, 40), 20, (255, 255, 255))
        else:
            ui.text_screen(self, "TAB for debug", (10, 10), 20, (58, 48, 41))

    def scene_transition(self, scene):  # allows optional scene transitions in the future
        self.scene = scene(self)

    # call when you want the game to exit
    def exit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":  # if you run the script directly (not an import)
    g = Game(MenuScene)
    g.run()
