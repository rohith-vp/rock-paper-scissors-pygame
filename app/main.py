from Game import Game
from utils import resource_path


game = Game(
    size = (400, 600),
    caption = "Rock Paper Scissors",
    icon_path = resource_path("res/icon.png")
)

game.start_game()
