from if3_game.engine import init, Game, Sprite, Layer
from asteroid import GameLayer, RESOLUTION


init(RESOLUTION, "Asteroid")
game = Game()
game.debug = True

bg_layer = Layer()
bg = Sprite("fond.png")
bg_layer.add(bg)

game_layer = GameLayer()

game.add(bg_layer)
game.add(game_layer)
game.run()