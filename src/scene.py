from src.object import Object


# base class for all scenes
class Scene(Object):
    def __init__(self, game):
        super(Scene, self).__init__(game)

        self.camera = game.camera
        self.wn = game.wn
