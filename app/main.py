from Game import Game
import os


game = Game(
    size = (400, 600),
    caption = "Rock Paper Scissors",
    icon_path = os.path.join("res", "icon.png")
)

game.start_game()
