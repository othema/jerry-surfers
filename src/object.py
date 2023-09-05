# base class for (most) things in the game
class Object:
    def __init__(self, game):
        self.game = game
        self.camera = game.camera

    def update(self):
        pass

    def render(self):
        pass
